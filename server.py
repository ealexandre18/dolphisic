import os
import sys

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        os.environ[key.strip()] = val.strip()
        except Exception:
            pass

load_env()
import sqlite3
import hashlib
import json
import re
import secrets
import time
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

# ANSI Colors for premium logging
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')
DEBUG_LOG_FILE = None
SENSITIVE_KEYS = ('password', 'pass', 'mot_de_passe', 'token', 'secret', 'api_key', 'apikey')
SESSION_COOKIE_NAME = 'dolphisic_session'
SESSION_COOKIE_MAX_AGE = 60 * 60 * 12


def strip_ansi(value):
    return ANSI_RE.sub('', str(value))


def redact_text(value):
    text = str(value)
    pattern = re.compile(r'(?i)\b(password|pass|mot_de_passe|token|secret|api[_-]?key)\s*[:=]\s*("[^"]*"|\'[^\']*\'|[^\s,}]+)')
    return pattern.sub(lambda match: f"{match.group(1)}=********", text)


def redact_payload(value):
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            key_text = str(key).lower()
            if any(sensitive in key_text for sensitive in SENSITIVE_KEYS):
                redacted[key] = '********'
            else:
                redacted[key] = redact_payload(item)
        return redacted
    if isinstance(value, (list, tuple)):
        return type(value)(redact_payload(item) for item in value)
    return value


def write_log(category, message, color=Colors.RESET):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = redact_text(message)
    console_line = f"[{timestamp}] {color}[{category}]{Colors.RESET} {message}"
    print(console_line, flush=True)

    if DEBUG_LOG_FILE:
        file_line = strip_ansi(console_line)
        try:
            with open(DEBUG_LOG_FILE, 'a', encoding='utf-8') as log_file:
                log_file.write(file_line + '\n')
        except Exception:
            pass

# Initialize ANSI support on Windows CMD/PowerShell if needed
if sys.platform == 'win32':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        # Fallback to os.system('') which also enables VT processing in cmd
        os.system('')

def log_db(message):
    write_log('DATABASE', message, Colors.CYAN)

def log_ui(message):
    write_log('UI', message, Colors.GREEN)

def log_logic(message):
    write_log('LOGIC', message, Colors.MAGENTA)

# Resolve the directory of server.py using its absolute path.
# This works regardless of the working directory when Python is launched.
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
# Change cwd to SERVER_DIR so SQLite relative paths always resolve correctly.
os.chdir(SERVER_DIR)

if os.environ.get('DOLPHISIC_DEBUG') == '1':
    logs_dir = os.path.join(SERVER_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    DEBUG_LOG_FILE = os.path.join(logs_dir, f"dolphisic-debug-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    write_log('DEBUG', f"Debug log file: {DEBUG_LOG_FILE}", Colors.BLUE)

app = Flask(
    __name__,
    static_folder=os.path.join(SERVER_DIR, 'dist'),
    static_url_path=''
)
# Enable CORS for frontend development server
CORS(app)

# Settings file for notifications
BASE_DIR = SERVER_DIR
SETTINGS_FILE = os.path.join(BASE_DIR, "notification_settings.json")

DEFAULT_NOTIFICATION_SETTINGS = {
    "global_notification_enabled": False,
    "notify_exceeded": True,
    "notify_approaching": True,
    "email_notif": ""
}

# Path to the compiled React frontend
DIST_DIR = os.path.join(SERVER_DIR, 'dist')


def calculate_next_key_date(date_str):
    if not date_str:
        return None
    try:
        # date_str is YYYY-MM-DD
        parts = date_str.split('-')
        if len(parts) == 3:
            year = int(parts[0]) + 2
            month = int(parts[1])
            day = int(parts[2])
            # Handle leap year
            if month == 2 and day == 29:
                is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
                if not is_leap:
                    day = 28
            return f"{year:04d}-{month:02d}-{day:02d}"
    except Exception:
        pass
    return None


# Resolve database and folders paths
BASE_DIR = SERVER_DIR
DB_SDIS = os.path.join(BASE_DIR, "sdis04.db")
DB_CARTO = os.path.join(BASE_DIR, "carto_sdis04.db")
DOCS_DIR = os.path.join(BASE_DIR, "documents_pylones")

# Ensure documents folder exists
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

app.config['UPLOAD_FOLDER'] = DOCS_DIR
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limits

def init_db():
    conn = sqlite3.connect(DB_SDIS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            type_materiel TEXT,
            etat TEXT NOT NULL,
            statut TEXT NOT NULL DEFAULT 'Disponible',
            modele TEXT,
            num_serie TEXT,
            cis TEXT,
            pocsag TEXT,
            rfgi TEXT,
            identifiant TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER NOT NULL,
            emprunteur TEXT NOT NULL,
            date_debut TEXT NOT NULL,
            date_fin TEXT NOT NULL,
            date_rendu TEXT,
            changement_etat TEXT,
            FOREIGN KEY(stock_id) REFERENCES stock(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_hidden_devices (
            device_id INTEGER PRIMARY KEY,
            hidden_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notification_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            enabled INTEGER DEFAULT 0,
            global_enabled INTEGER DEFAULT 0,
            notify_j_minus_1 INTEGER DEFAULT 0,
            notify_j INTEGER DEFAULT 0
        )
    """)
    # Migration to add enabled column if it doesn't exist
    try:
        cur.execute("ALTER TABLE notification_emails ADD COLUMN enabled INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Drop table if it has the old foreign key constraint to avoid operational error
    try:
        schema_info = cur.execute("SELECT sql FROM sqlite_master WHERE name='notification_email_devices'").fetchone()
        if schema_info and "REFERENCES parc" in schema_info[0]:
            cur.execute("DROP TABLE IF EXISTS notification_email_devices")
    except Exception:
        pass

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notification_email_devices (
            email_id INTEGER,
            device_id INTEGER,
            PRIMARY KEY (email_id, device_id),
            FOREIGN KEY (email_id) REFERENCES notification_emails (id) ON DELETE CASCADE
        )
    """)
    # Migration to add new columns if they don't exist
    for col in ["modele", "num_serie", "cis", "pocsag", "rfgi", "identifiant"]:
        try:
            cur.execute(f"ALTER TABLE stock ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass

    # Dedicated demonstration centre. Data remains visible in inventory/search,
    # but aggregate and operational endpoints explicitly exclude it.
    centre_columns = {row[1] for row in cur.execute("PRAGMA table_info(centres)").fetchall()}
    if 'cis' in centre_columns:
        if 'comptage' in centre_columns:
            cur.execute("""
                INSERT INTO centres (cis, comptage)
                SELECT 'TEST', '0'
                WHERE NOT EXISTS (SELECT 1 FROM centres WHERE UPPER(TRIM(cis)) = 'TEST')
            """)
        else:
            cur.execute("""
                INSERT INTO centres (cis)
                SELECT 'TEST'
                WHERE NOT EXISTS (SELECT 1 FROM centres WHERE UPPER(TRIM(cis)) = 'TEST')
            """)

    test_devices = [
        ('TEST-CRYPT-001', 'TPH700', '2022-01-10', '2024-01-10'),
        ('TEST-CRYPT-002', 'TPH700', '2022-02-14', '2024-02-14'),
        ('TEST-CRYPT-003', 'TPH700', '2022-03-18', '2024-03-18'),
        ('TEST-CRYPT-004', 'TPH700', '2022-04-22', '2024-04-22'),
        ('TEST-CRYPT-005', 'TPH700', '2022-05-26', '2024-05-26'),
        ('TEST-CRYPT-006', 'TPH700', '2022-06-30', '2024-06-30'),
        ('TEST-CRYPT-007', 'TPH700', '2022-07-04', '2024-07-04'),
        ('TEST-CRYPT-008', 'TPH700', '2022-08-08', '2024-08-08'),
        ('TEST-CRYPT-009', 'TPH700', '2022-09-12', '2024-09-12'),
        ('TEST-CRYPT-010', 'TPH700', '2022-10-16', '2024-10-16'),
    ]
    for serial, model, last_key_date, next_key_date in test_devices:
        cur.execute("""
            INSERT INTO parc
                (cis, modele, num_serie, affectation, version_logiciel,
                 observation, date_maj_cle, date_cle_a_faire, date_prog)
            SELECT 'TEST', ?, ?, 'APPAREIL TEST', 'TEST',
                   'Donnée de démonstration isolée', ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM parc WHERE UPPER(TRIM(num_serie)) = UPPER(TRIM(?))
            )
        """, (model, serial, last_key_date, next_key_date, last_key_date, serial))

    # Dynamic test devices for notifications verification
    from datetime import timedelta
    today_str = datetime.now().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_str = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d") # 2 years ago

    notif_test_devices = [
        ('TEST-EXP-TODAY', 'TPH700', yesterday_str, today_str, 'test-today@sdis04.fr', 1),
        ('TEST-EXP-TOMORROW-1', 'TPH700', yesterday_str, tomorrow_str, 'test-tomorrow@sdis04.fr', 1),
        ('TEST-EXP-TOMORROW-2', 'TPH700', yesterday_str, tomorrow_str, 'test-tomorrow@sdis04.fr', 1),
    ]

    for serial, model, last_key_date, next_key_date, test_email, notif_active in notif_test_devices:
        cur.execute("SELECT 1 FROM parc WHERE UPPER(TRIM(num_serie)) = ?", (serial.upper(),))
        exists = cur.fetchone()
        if exists:
            cur.execute("""
                UPDATE parc
                SET date_maj_cle = ?, date_cle_a_faire = ?, date_prog = ?, cis = 'TEST', notification_active = ?, email_notif = ?
                WHERE UPPER(TRIM(num_serie)) = ?
            """, (last_key_date, next_key_date, last_key_date, notif_active, test_email, serial.upper()))
        else:
            cur.execute("""
                INSERT INTO parc
                    (cis, modele, num_serie, affectation, version_logiciel,
                     observation, date_maj_cle, date_cle_a_faire, date_prog, notification_active, email_notif)
                VALUES ('TEST', ?, ?, 'APPAREIL TEST NOTIF', 'TEST',
                       'Appareil de test dynamique pour notifications', ?, ?, ?, ?, ?)
            """, (model, serial, last_key_date, next_key_date, last_key_date, notif_active, test_email))

    conn.commit()
    conn.close()

init_db()

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Helper to verify password hashed with PBKDF2-SHA256
def verify_hash(password, stored_hash):
    if not stored_hash:
        return False
    if "$" not in stored_hash:
        # Fallback for plain text password comparison
        return password == stored_hash
    try:
        salt_hex, hash_hex = stored_hash.split("$")
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
        return pwd_hash.hex() == hash_hex
    except Exception:
        return False

# Middleware/Helper for SQLite transaction
def query_db(db_path, query, args=(), one=False, commit=False):
    db_name = os.path.basename(db_path)
    clean_query = " ".join(query.strip().split())
    safe_args = redact_payload(args)
    if commit:
        log_db(f"{Colors.YELLOW}WRITE{Colors.RESET} on {Colors.BOLD}{db_name}{Colors.RESET} | Query: {clean_query} | Args: {safe_args}")
    else:
        log_db(f"READ on {Colors.BOLD}{db_name}{Colors.RESET} | Query: {clean_query} | Args: {safe_args}")
        
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        if commit:
            conn.commit()
            lastrowid = cur.lastrowid
            conn.close()
            return lastrowid
        rv = cur.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        conn.close()
        log_db(f"{Colors.RED}ERROR{Colors.RESET} on {db_name}: {str(e)}")
        raise e


def load_notification_settings():
    settings = dict(DEFAULT_NOTIFICATION_SETTINGS)
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as settings_file:
                saved = json.load(settings_file)
            if isinstance(saved, dict):
                settings.update({key: saved[key] for key in settings if key in saved})
        except Exception as exc:
            log_logic(f"Unable to read notification settings: {exc}")

    return settings


def save_notification_settings(data):
    current = load_notification_settings()
    allowed_keys = set(DEFAULT_NOTIFICATION_SETTINGS)
    for key, value in data.items():
        if key in allowed_keys:
            if key == 'global_notification_enabled':
                if isinstance(value, str):
                    current[key] = value.lower() == 'true'
                else:
                    current[key] = bool(value)
            else:
                current[key] = value

    with open(SETTINGS_FILE, 'w', encoding='utf-8') as settings_file:
        json.dump(current, settings_file, indent=4, ensure_ascii=False)
    return current


def parse_date_value(value):
    if not value:
        return None
    raw_value = str(value).strip().split(' ')[0]
    for date_format in ('%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y', '%d/%m/%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(raw_value, date_format).date()
        except ValueError:
            continue
    return None


def collect_urgent_operations():
    today = datetime.now().date()
    equipment_rows = query_db(DB_SDIS, """
        SELECT p.rowid AS id, p.num_serie, p.modele, p.cis, p.affectation,
               p.date_maj_cle, p.date_cle_a_faire, m.type
        FROM parc p
        LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
        WHERE UPPER(TRIM(COALESCE(p.cis, ''))) != 'TEST'
          AND p.date_cle_a_faire IS NOT NULL
          AND TRIM(p.date_cle_a_faire) != ''
    """)

    overdue_cryptage = []
    approaching_cryptage = []
    for row in equipment_rows:
        item = dict(row)
        due_date = parse_date_value(item.get('date_cle_a_faire'))
        if not due_date:
            continue
        delta_days = (due_date - today).days
        item['days_delta'] = delta_days
        if delta_days < 0:
            item['days_overdue'] = abs(delta_days)
            overdue_cryptage.append(item)
        elif delta_days <= 30:
            item['days_remaining'] = delta_days
            approaching_cryptage.append(item)

    loan_rows = query_db(DB_SDIS, """
        SELECT p.id, p.stock_id, p.emprunteur, p.date_debut, p.date_fin,
               s.nom, s.modele, s.num_serie, s.cis
        FROM prets p
        JOIN stock s ON s.id = p.stock_id
        WHERE p.date_rendu IS NULL
          AND UPPER(TRIM(COALESCE(s.cis, ''))) != 'TEST'
    """)
    overdue_loans = []
    for row in loan_rows:
        item = dict(row)
        due_date = parse_date_value(item.get('date_fin'))
        if due_date and due_date < today:
            item['days_overdue'] = (today - due_date).days
            overdue_loans.append(item)

    overdue_cryptage.sort(key=lambda item: item['days_overdue'], reverse=True)
    approaching_cryptage.sort(key=lambda item: item['days_remaining'])
    overdue_loans.sort(key=lambda item: item['days_overdue'], reverse=True)
    return {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'summary': {
            'overdue_cryptage': len(overdue_cryptage),
            'approaching_cryptage': len(approaching_cryptage),
            'overdue_loans': len(overdue_loans),
            'total_urgent': len(overdue_cryptage) + len(overdue_loans)
        },
        'overdue_cryptage': overdue_cryptage,
        'approaching_cryptage': approaching_cryptage,
        'overdue_loans': overdue_loans
    }


# --- LOGGING SYSTEM MIDDLEWARES & ENDPOINT ---

@app.before_request
def start_timer():
    g.start_time = time.time()
    # Skip UI logs endpoint to prevent console spam
    if request.path != '/api/logs/ui':
        details = []
        if request.args:
            details.append(f"Query: {redact_payload(dict(request.args))}")
        if request.is_json:
            body = request.get_json(silent=True)
            if body:
                details.append(f"Body: {redact_payload(body)}")
        suffix = f" | {' | '.join(details)}" if details else ""
        log_logic(f"API Request: {Colors.BOLD}{request.method} {request.path}{Colors.RESET} | Client: {request.remote_addr}{suffix}")

@app.after_request
def log_request(response):
    if request.path == '/api/logs/ui':
        return response
        
    diff = time.time() - g.get('start_time', time.time())
    duration_ms = diff * 1000
    
    status_code = response.status_code
    if 200 <= status_code < 300:
        status_color = Colors.GREEN
    elif 300 <= status_code < 400:
        status_color = Colors.CYAN
    else:
        status_color = Colors.RED
        
    error_details = ""
    if status_code >= 400 and response.is_json:
        try:
            error_details = f" | Error: {redact_payload(response.get_json(silent=True))}"
        except Exception:
            error_details = ""
    log_logic(f"API Response: {request.method} {request.path} -> {status_color}{status_code} {response.status}{Colors.RESET} | Duration: {duration_ms:.2f}ms{error_details}")
    return response

@app.route('/api/logs/ui', methods=['POST'])
def log_ui_event():
    try:
        data = request.json or {}
        event_type = data.get('event', 'unknown').upper()
        path = data.get('path', '/')
        details = redact_payload(data.get('details', {}))
        
        if event_type == 'CLICK':
            label = details.get('label', '')
            tag = details.get('tag', '')
            elem_id = details.get('id', '')
            elem_class = details.get('class', '')
            
            id_str = f" id: {elem_id}" if elem_id else ""
            class_str = f" class: {elem_class}" if elem_class else ""
            details_str = f"<{tag}>{id_str}{class_str}"
            log_ui(f"Click on {Colors.BOLD}{label}{Colors.RESET} [{details_str}] (Page: {path})")
            
        elif event_type == 'CHANGE':
            name = details.get('name', '')
            label = details.get('label', '')
            val = details.get('value', '')
            field_identity = f"{name} {label}".lower()
            if any(sensitive in field_identity for sensitive in ('password', 'mot de passe', 'token', 'secret', 'clé', 'key')):
                val = '********'
            log_ui(f"Toggle/Input '{Colors.BOLD}{label or name}{Colors.RESET}' changed to: {Colors.YELLOW}{val}{Colors.RESET} (Page: {path})")
            
        elif event_type == 'SUBMIT':
            form_id = details.get('id', '')
            form_name = details.get('name', '')
            fields = details.get('fields', {})
            
            # redact passwords
            redacted_fields = {}
            for k, v in fields.items():
                if any(x in k.lower() for x in ['pass', 'token', 'secret', 'key']):
                    redacted_fields[k] = '********'
                else:
                    redacted_fields[k] = v
            
            form_str = form_id or form_name or 'unnamed-form'
            log_ui(f"Submitted form '{Colors.BOLD}{form_str}{Colors.RESET}' | Data: {redacted_fields} (Page: {path})")
            
        elif event_type == 'NAVIGATION':
            log_ui(f"Navigation to {Colors.BOLD}{path}{Colors.RESET}")
            
        else:
            log_ui(f"Event: {event_type} | Details: {details} (Page: {path})")
            
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- AUTHENTICATION ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Veuillez saisir un identifiant et un mot de passe'}), 400

    log_logic(f"Login attempt for user: '{Colors.BOLD}{username}{Colors.RESET}'")
    try:
        user_row = query_db(DB_SDIS, "SELECT mot_de_passe, role FROM utilisateurs WHERE identifiant = ?", (username,), one=True)
        if user_row and verify_hash(password, user_row['mot_de_passe']):
            role = user_row['role'] or 'USER'
            log_logic(f"User '{Colors.BOLD}{username}{Colors.RESET}' successfully logged in (Role: {Colors.YELLOW}{role}{Colors.RESET})")
            session_token = secrets.token_urlsafe(32)
            response = jsonify({
                'success': True,
                'user': {
                    'username': username,
                    'role': role
                },
                'token': session_token
            })
            if request.headers.get('X-DolphiSIC-Cookie-Consent') == 'accepted':
                response.set_cookie(
                    SESSION_COOKIE_NAME,
                    session_token,
                    max_age=SESSION_COOKIE_MAX_AGE,
                    httponly=True,
                    samesite='Lax',
                    secure=request.is_secure
                )
                log_logic(f"Session cookie created for user: '{Colors.BOLD}{username}{Colors.RESET}'")
            else:
                log_logic(f"Session cookie skipped for user: '{Colors.BOLD}{username}{Colors.RESET}' (cookie consent not accepted)")
            return response
        log_logic(f"User '{Colors.BOLD}{username}{Colors.RESET}' login FAILED (Invalid credentials)")
        return jsonify({'error': 'Identifiant ou mot de passe incorrect'}), 401
    except Exception as e:
        log_logic(f"User '{Colors.BOLD}{username}{Colors.RESET}' login FAILED (Database Error: {str(e)})")
        return jsonify({'error': f"Erreur de connexion base: {str(e)}"}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({'success': True})
    response.delete_cookie(SESSION_COOKIE_NAME, samesite='Lax')
    log_logic("Session cookie cleared")
    return response

# --- INVENTORY & FLEET ---
@app.route('/api/centres', methods=['GET'])
def get_centres():
    try:
        rows = query_db(DB_SDIS, "SELECT DISTINCT TRIM(cis) as cis FROM centres WHERE cis IS NOT NULL ORDER BY cis ASC")
        return jsonify([r['cis'] for r in rows if r['cis']])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    cis = request.args.get('cis')
    device_type = request.args.get('type')
    if not cis or not device_type:
        return jsonify({'error': 'Paramètres cis et type requis'}), 400

    try:
        query = """
            SELECT p.rowid as id, p.num_serie, p.modele, m.marque, p.affectation,
                   p.date_prog, p.date_maj_cle, p.date_cle_a_faire, p.notification_active, p.email_notif,
                   p.code_pocsag, p.immatriculation, p.rfgi, p.version_logiciel, p.classe_service, p.date_achat, p.observation,
                   p.cis, m.type, p.statut_activite
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE TRIM(p.cis) = TRIM(?) AND TRIM(m.type) = TRIM(?)
        """
        rows = query_db(DB_SDIS, query, (cis, device_type))
        log_logic(f"Device filter results | CIS='{cis}' | Type='{device_type}' | Count={len(rows)}")
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>', methods=['GET'])
def get_device_details(rowid):
    try:
        query = """
            SELECT p.rowid as id, p.num_serie, p.modele, m.marque, p.affectation,
                   p.date_prog, p.date_maj_cle, p.date_cle_a_faire, p.notification_active, p.email_notif,
                   p.code_pocsag, p.immatriculation, p.rfgi, p.version_logiciel, p.classe_service, p.date_achat, p.observation,
                   p.cis, m.type, p.statut_activite
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE p.rowid = ?
        """
        row = query_db(DB_SDIS, query, (rowid,), one=True)
        if row:
            return jsonify(dict(row))
        return jsonify({'error': 'Équipement introuvable'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>/update-cryptage', methods=['POST'])
def update_device_cryptage(rowid):
    data = request.json or {}
    date_maj = data.get('date_maj_cle')
    if not date_maj:
        return jsonify({'error': 'Date de mise à jour requise'}), 400

    date_a_faire = calculate_next_key_date(date_maj)
    log_logic(f"Updating encryption date for Device ID={rowid} to {date_maj}")
    try:
        query_db(DB_SDIS, "UPDATE parc SET date_maj_cle = ?, date_cle_a_faire = ?, notification_active = 0, email_notif = NULL WHERE rowid = ?", 
                 (date_maj, date_a_faire, rowid), commit=True)
        log_logic(f"Device ID={rowid} encryption updated. Next key date: {date_a_faire}")
        return jsonify({'success': True, 'message': 'Dates de chiffrement mises à jour avec succès', 'date_cle_a_faire': date_a_faire})
    except Exception as e:
        log_logic(f"Failed to update encryption for Device ID={rowid}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>/delete', methods=['POST'])
def delete_device(rowid):
    log_logic(f"Deleting Device ID={rowid}")
    try:
        query_db(DB_SDIS, "DELETE FROM parc WHERE rowid = ?", (rowid,), commit=True)
        log_logic(f"Device ID={rowid} deleted successfully")
        return jsonify({'success': True, 'message': 'Équipement supprimé avec succès'})
    except Exception as e:
        log_logic(f"Failed to delete Device ID={rowid}: {str(e)}")
        return jsonify({'error': str(e)}), 500


def normalize_device_ids(raw_ids):
    if not isinstance(raw_ids, list):
        return []
    normalized = []
    for raw_id in raw_ids[:500]:
        try:
            device_id = int(raw_id)
            if device_id > 0 and device_id not in normalized:
                normalized.append(device_id)
        except (TypeError, ValueError):
            continue
    return normalized


@app.route('/api/devices/bulk-update-cryptage', methods=['POST'])
def bulk_update_device_cryptage():
    data = request.json or {}
    device_ids = normalize_device_ids(data.get('ids'))
    date_maj = data.get('date_maj_cle')
    if not device_ids or not date_maj:
        return jsonify({'error': 'Équipements et date de mise à jour requis'}), 400

    date_a_faire = calculate_next_key_date(date_maj)
    placeholders = ','.join('?' for _ in device_ids)
    try:
        query_db(
            DB_SDIS,
            f"""
            UPDATE parc
            SET date_maj_cle = ?, date_cle_a_faire = ?,
                notification_active = 0, email_notif = NULL
            WHERE rowid IN ({placeholders})
            """,
            (date_maj, date_a_faire, *device_ids),
            commit=True
        )
        log_logic(f"Bulk cryptage update | Count={len(device_ids)} | Date={date_maj}")
        return jsonify({
            'success': True,
            'updated': len(device_ids),
            'date_cle_a_faire': date_a_faire
        })
    except Exception as e:
        log_logic(f"Bulk cryptage update failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/bulk-delete', methods=['POST'])
def bulk_delete_devices():
    data = request.json or {}
    device_ids = normalize_device_ids(data.get('ids'))
    if not device_ids:
        return jsonify({'error': 'Aucun équipement sélectionné'}), 400

    placeholders = ','.join('?' for _ in device_ids)
    try:
        query_db(
            DB_SDIS,
            f"DELETE FROM parc WHERE rowid IN ({placeholders})",
            tuple(device_ids),
            commit=True
        )
        log_logic(f"Bulk device deletion | Count={len(device_ids)}")
        return jsonify({'success': True, 'deleted': len(device_ids)})
    except Exception as e:
        log_logic(f"Bulk device deletion failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/modeles', methods=['GET'])
def get_modeles_by_type():
    device_type = request.args.get('type')
    if not device_type:
        return jsonify({'error': 'Paramètre type requis'}), 400
    try:
        rows = query_db(DB_SDIS, "SELECT DISTINCT TRIM(modele) as name FROM materiel WHERE TRIM(type) = TRIM(?) ORDER BY name ASC", (device_type,))
        return jsonify([r['name'] for r in rows if r['name']])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json or {}
    cis = data.get('cis')
    modele = data.get('modele')
    num_serie = data.get('num_serie')
    affectation = data.get('affectation', '')
    version_logiciel = data.get('version_logiciel', '')
    observation = data.get('observation', '')
    date_maj_cle = data.get('date_maj_cle') or None
    
    # Calculate next key date automatically if date_maj_cle is set
    date_cle_a_faire = calculate_next_key_date(date_maj_cle) if date_maj_cle else None

    if not cis or not modele or not num_serie:
        return jsonify({'error': 'CIS, Modèle et Numéro de série requis'}), 400

    log_logic(f"Adding device: Model='{modele}', S/N='{num_serie}', CIS='{cis}'")
    try:
        # Check if model exists
        model_row = query_db(DB_SDIS, "SELECT modele FROM materiel WHERE TRIM(modele) = TRIM(?)", (modele,), one=True)
        if not model_row:
            log_logic(f"Failed to add device: Model '{modele}' not in repository")
            return jsonify({'error': f"Le modèle '{modele}' n'existe pas dans le référentiel matériel"}), 400

        query = """
            INSERT INTO parc (cis, modele, num_serie, affectation, version_logiciel, observation, date_maj_cle, date_cle_a_faire, date_prog)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        date_prog = datetime.now().strftime("%Y-%m-%d")
        new_rowid = query_db(DB_SDIS, query, 
                             (cis, modele, num_serie, affectation, version_logiciel, observation, date_maj_cle, date_cle_a_faire, date_prog), 
                             commit=True)
        log_logic(f"Device added successfully (ID: {new_rowid}, Next Key Date: {date_cle_a_faire})")
        return jsonify({'success': True, 'id': new_rowid, 'message': 'Équipement ajouté au parc avec succès', 'date_cle_a_faire': date_cle_a_faire})
    except Exception as e:
        log_logic(f"Failed to add device: {str(e)}")
        return jsonify({'error': str(e)}), 500

# --- NOTIFICATIONS SETTINGS ---
@app.route('/api/notifications/settings', methods=['GET', 'POST'])
def handle_notification_settings():
    if request.method == 'GET':
        try:
            return jsonify(load_notification_settings())
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    try:
        data = redact_payload(request.json or {})
        saved = save_notification_settings(request.json or {})
        log_logic(f"Notification email setting updated: {data}")
        
        # Trigger an immediate check in the background if global notification is enabled and email is set
        if saved.get('global_notification_enabled', False) and saved.get('email_notif'):
            import threading
            log_logic("Global notification is active, spawning immediate check in background thread.")
            threading.Thread(target=check_and_send_notifications, kwargs={'force': False}, daemon=True).start()

        return jsonify({
            'success': True,
            'message': 'Adresse email enregistrée',
            'settings': saved
        })
    except (TypeError, ValueError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_logic(f"Failed to save notification settings: {e}")
        return jsonify({'error': str(e)}), 500


def send_test_email(recipient):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_host = "smtp-relay.brevo.com"
    smtp_port = 587
    smtp_user = "afb5b1001@smtp-brevo.com"
    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not smtp_password:
        raise ValueError("SMTP_PASSWORD non configuré dans l'environnement ou le fichier .env")
    smtp_from = "dolphisic@outlook.fr"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Dolphisic - Test du système de notification email"
    msg['From'] = f"Dolphisic SDIS 04 <{smtp_from}>"
    msg['To'] = recipient

    text = (
        "Bonjour,\n\n"
        "Ceci est un email de test envoyé depuis votre application Dolphisic.\n"
        "Le système de notification par email est désormais fonctionnel.\n\n"
        "Cordialement,\n"
        "L'équipe SDIS 04"
    )
    
    html = f"""
    <html>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; color: #333333;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e1e4e8;">
          <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">DOLPHISIC</h1>
            <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 14px;">Système de gestion et d'alertes du parc radio</p>
          </div>
          <div style="padding: 30px; line-height: 1.6;">
            <h2 style="color: #0f172a; margin-top: 0; font-size: 18px; font-weight: 600;">Test de notification réussi !</h2>
            <p style="color: #475569;">Bonjour,</p>
            <p style="color: #475569;">Vous recevez ce message car vous avez cliqué sur le bouton de test d'envoi d'email dans les paramètres de <strong>Dolphisic</strong>.</p>
            <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 15px; margin: 20px 0; border-radius: 0 4px 4px 0;">
              <p style="margin: 0; font-size: 14px; color: #1e293b;">
                <strong>Configuration SMTP Brevo :</strong><br>
                Hôte : <code>{smtp_host}</code><br>
                Port : <code>{smtp_port}</code><br>
                Utilisateur : <code>{smtp_user}</code><br>
                Expéditeur : <code>{smtp_from}</code>
              </p>
            </div>
            <p style="color: #475569;">Le système d'envoi d'email est correctement configuré et prêt à vous notifier lors des prochaines échéances de cryptage ou de retour de prêt.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;">
            <p style="color: #64748b; font-size: 12px; text-align: center; margin: 0;">
              Ceci est un message automatique, merci de ne pas y répondre.<br>
              &copy; {datetime.now().year} SDIS 04 - Tous droits réservés.
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain', 'utf-8')
    part2 = MIMEText(html, 'html', 'utf-8')

    msg.attach(part1)
    msg.attach(part2)

    log_logic(f"Connecting to SMTP host {smtp_host}:{smtp_port}...")
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
    
    log_logic("Sending EHLO...")
    server.ehlo()
    
    log_logic("Starting TLS secure channel...")
    server.starttls()
    
    log_logic("Sending EHLO after TLS...")
    server.ehlo()
    
    log_logic(f"Logging in as SMTP user: {smtp_user}...")
    server.login(smtp_user, smtp_password)
    log_logic("SMTP login OK")
    
    log_logic(f"Sending email from {smtp_from} to {recipient}...")
    response = server.sendmail(smtp_from, recipient, msg.as_string())
    log_logic(f"SMTP sendmail response: {response if response else '250 OK (Email accepted for delivery)'}")
    
    log_logic("Closing SMTP connection...")
    server.quit()
    log_logic("Email sent successfully and connection closed.")


def send_consolidated_email(recipient, items):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_host = "smtp-relay.brevo.com"
    smtp_port = 587
    smtp_user = "afb5b1001@smtp-brevo.com"
    smtp_password = os.environ.get("SMTP_PASSWORD")
    smtp_from = "dolphisic@outlook.fr"

    if not smtp_password:
        raise ValueError("SMTP_PASSWORD non configuré dans l'environnement ou le fichier .env")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Dolphisic - {len(items)} alerte(s) d'échéance de cryptage"
    msg['From'] = f"Dolphisic SDIS 04 <{smtp_from}>"
    msg['To'] = recipient

    # Build plain text table
    text_lines = [
        "Bonjour,",
        "",
        "Voici le récapitulatif des équipements radio dont le cryptage arrive à échéance :",
        ""
    ]
    for item in items:
        dev = item['device']
        if item['type'] == 'overdue':
            status = "DÉPASSÉ (En retard)"
        elif item['type'] == 'today':
            status = "AUJOURD'HUI"
        else:
            status = "DEMAIN (1 jour à l'avance)"
        text_lines.append(f"- CIS: {dev['cis']} | Modèle: {dev['modele']} | N° Série: {dev['num_serie']} | Échéance: {dev['date_cle_a_faire']} | Statut: {status}")
    
    text_lines.extend([
        "",
        "Merci d'effectuer les mises à jour nécessaires.",
        "",
        "Cordialement,",
        "L'équipe SDIS 04"
    ])
    text = "\n".join(text_lines)

    # Build HTML table rows
    rows_html = ""
    for item in items:
        dev = item['device']
        if item['type'] == 'overdue':
            status_style = "background-color: #fef2f2; color: #991b1b; border: 1px solid #fee2e2;"
            status_text = "🚨 Retard"
        elif item['type'] == 'today':
            status_style = "background-color: #fff5f5; color: #c53030; border: 1px solid #fed7d7;"
            status_text = "⚠️ Aujourd'hui"
        else:
            status_style = "background-color: #fffbeb; color: #92400e; border: 1px solid #fef3c7;"
            status_text = "📅 Demain (J-1)"

        rows_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
          <td style="padding: 12px; font-weight: 600; color: #1e293b;">{dev['cis']}</td>
          <td style="padding: 12px; color: #334155;">{dev['modele']}</td>
          <td style="padding: 12px; color: #334155; font-family: monospace;">{dev['num_serie']}</td>
          <td style="padding: 12px; color: #334155;">{dev['date_cle_a_faire']}</td>
          <td style="padding: 12px; text-align: center;">
            <span style="display: inline-block; padding: 4px 8px; font-size: 12px; font-weight: 600; border-radius: 4px; {status_style}">{status_text}</span>
          </td>
        </tr>
        """

    html = f"""
    <html>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; color: #333333;">
        <div style="max-width: 700px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e1e4e8;">
          <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">DOLPHISIC</h1>
            <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 14px;">Alertes de cryptage de parc radio</p>
          </div>
          <div style="padding: 30px; line-height: 1.6;">
            <h2 style="color: #0f172a; margin-top: 0; font-size: 18px; font-weight: 600;">Récapitulatif des échéances</h2>
            <p style="color: #475569;">Bonjour,</p>
            <p style="color: #475569;">Voici la liste des équipements dont les clés de cryptage doivent être mises à jour (dépassées, aujourd'hui ou demain) :</p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; text-align: left; font-size: 14px;">
              <thead>
                <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                  <th style="padding: 12px; font-weight: 600; color: #475569;">CIS</th>
                  <th style="padding: 12px; font-weight: 600; color: #475569;">Modèle</th>
                  <th style="padding: 12px; font-weight: 600; color: #475569;">N° Série</th>
                  <th style="padding: 12px; font-weight: 600; color: #475569;">Échéance</th>
                  <th style="padding: 12px; font-weight: 600; color: #475569; text-align: center;">Statut</th>
                </tr>
              </thead>
              <tbody>
                {rows_html}
              </tbody>
            </table>
            
            <p style="color: #475569;">Merci de programmer et d'effectuer ces opérations de cryptage dans les meilleurs délais pour éviter toute interruption de service.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;">
            <p style="color: #64748b; font-size: 12px; text-align: center; margin: 0;">
              Ceci est un message automatique de Dolphisic. Merci de ne pas y répondre.<br>
              &copy; {datetime.now().year} SDIS 04 - Tous droits réservés.
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # Send the message via SMTP
    log_logic(f"Connecting to SMTP host {smtp_host}:{smtp_port}...")
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_password)
    
    log_logic(f"SMTP sending email from {smtp_from} to {recipient}...")
    response = server.sendmail(smtp_from, recipient, msg.as_string())
    log_logic(f"SMTP response: {response if response else '250 OK (Email accepted for delivery)'}")
    
    server.quit()


def check_and_send_notifications(force=False, target_email=None):
    from datetime import datetime, timedelta
    import json
    import os

    log_logic(f"Starting check_and_send_notifications(force={force}, target_email={target_email})...")
    
    # Load all registered notification emails (only enabled ones)
    try:
        if target_email:
            emails_config = query_db(DB_SDIS, "SELECT id, email, global_enabled, notify_j_minus_1, notify_j FROM notification_emails WHERE email = ? AND enabled = 1", (target_email,))
        else:
            emails_config = query_db(DB_SDIS, "SELECT id, email, global_enabled, notify_j_minus_1, notify_j FROM notification_emails WHERE enabled = 1")
    except Exception as e:
        log_logic(f"Failed to query notification emails: {e}")
        return

    if not emails_config:
        log_logic("No registered emails found for notifications.")
        return

    # Load all device assignments to email IDs
    try:
        assignments_rows = query_db(DB_SDIS, "SELECT email_id, device_id FROM notification_email_devices")
        assignments = { (row['email_id'], row['device_id']) for row in assignments_rows }
    except Exception as e:
        log_logic(f"Failed to query device assignments: {e}")
        assignments = set()

    # Query all active devices (excluding hidden devices and reform/lost ones)
    query = """
        SELECT p.rowid AS id, p.num_serie, p.modele, p.cis, p.affectation,
               p.date_maj_cle, p.date_cle_a_faire, m.type
        FROM parc p
        LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
        WHERE UPPER(TRIM(COALESCE(p.cis, ''))) NOT IN ('PERDU', 'REFORME', 'RÉFORME')
          AND p.date_cle_a_faire IS NOT NULL
          AND TRIM(p.date_cle_a_faire) != ''
          AND NOT EXISTS (
              SELECT 1
              FROM dashboard_hidden_devices hidden
              WHERE hidden.device_id = p.rowid
          )
    """
    
    try:
        devices = query_db(DB_SDIS, query)
    except Exception as e:
        log_logic(f"Failed to query devices for notifications: {e}")
        return

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")

    # Load history of already sent notifications
    history_file = os.path.join(SERVER_DIR, "notification_history.json")
    sent_alerts = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                sent_alerts = history_data.get('sent_alerts', [])
        except Exception as e:
            log_logic(f"Unable to read notification history: {e}")

    # Index historical sent entries for faster check
    global_catchups = {a['email'] for a in sent_alerts if 'email' in a and a.get('type') == 'global_catchup'}
    specific_overdues = {(a['email'], a['device_id']) for a in sent_alerts if 'email' in a and 'device_id' in a and a.get('type') == 'overdue'}
    sent_set = { (a['email'], a['device_id'], a['date'], a['type']) for a in sent_alerts if 'email' in a and 'device_id' in a and 'date' in a and 'type' in a }

    notifications_to_send = {}
    new_sent_entries = []

    for dev in devices:
        due_date = parse_date_value(dev['date_cle_a_faire'])
        if not due_date:
            continue
        
        alert_type = None
        if due_date < today:
            alert_type = 'overdue'
        elif due_date == today:
            alert_type = 'today'
        elif due_date == tomorrow:
            alert_type = 'tomorrow'
            
        if not alert_type:
            continue

        device_id = dev['id']

        for email_row in emails_config:
            email = email_row['email'].strip()
            if not email:
                continue

            # Determine eligibility
            eligible = False
            if email_row['global_enabled'] == 1:
                # Global notification logic:
                if alert_type == 'overdue':
                    # Overdue is only included if global catch-up has not been sent yet
                    catchup_sent = (email in global_catchups) if not force else False
                    if not catchup_sent:
                        eligible = True
                elif alert_type == 'today' and email_row['notify_j'] == 1:
                    eligible = True
                elif alert_type == 'tomorrow' and email_row['notify_j_minus_1'] == 1:
                    eligible = True
            else:
                # Specific assigned devices logic:
                if (email_row['id'], device_id) in assignments:
                    if alert_type == 'overdue':
                        # Overdue for specific device is only sent once ever
                        overdue_sent = ((email, device_id) in specific_overdues) if not force else False
                        if not overdue_sent:
                            eligible = True
                    else:
                        eligible = True

            if not eligible:
                continue

            # Check if we already sent this exact alert today (prevent duplicates on same-day runs)
            if not force and (email, device_id, today_str, alert_type) in sent_set:
                continue

            if email not in notifications_to_send:
                notifications_to_send[email] = []
            
            notifications_to_send[email].append({
                'device': dev,
                'type': alert_type
            })
            
            # Track that we are sending this alert
            new_sent_entries.append({
                'email': email,
                'device_id': device_id,
                'date': today_str,
                'type': alert_type
            })

    if not notifications_to_send:
        log_logic("No new notifications to send.")
        return

    # Send consolidated emails
    for email, items in notifications_to_send.items():
        log_logic(f"Sending consolidated email to {email} containing {len(items)} alerts...")
        try:
            send_consolidated_email(email, items)
            log_logic(f"Consolidated email successfully sent to {email}")
            
            # Record global_catchup entry if it was sent now
            email_row = next((r for r in emails_config if r['email'].strip() == email), None)
            if email_row and email_row['global_enabled'] == 1 and (email not in global_catchups or force):
                new_sent_entries.append({
                    'email': email,
                    'device_id': None,
                    'date': today_str,
                    'type': 'global_catchup'
                })
        except Exception as e:
            log_logic(f"Failed to send consolidated email to {email}: {e}")
            # Do not track as sent if it failed to deliver
            new_sent_entries = [entry for entry in new_sent_entries if entry['email'] != email]

    # Update history file
    if not force and new_sent_entries:
        sent_alerts.extend(new_sent_entries)
        # Prune old history entries (e.g. older than 30 days)
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        sent_alerts = [a for a in sent_alerts if a.get('date', '') >= cutoff_date]
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump({'sent_alerts': sent_alerts}, f, indent=4)
            log_logic(f"Notification history updated with {len(new_sent_entries)} new entries.")
        except Exception as e:
            log_logic(f"Failed to save notification history: {e}")


def start_notification_scheduler():
    import threading
    import time

    def run_loop():
        # Delay startup slightly to let the server load
        time.sleep(5)
        log_logic("Notification scheduler check running...")
        try:
            check_and_send_notifications()
        except Exception as e:
            log_logic(f"Error in notification scheduler startup run: {e}")
            
        while True:
            # Run check every 4 hours
            time.sleep(4 * 3600)
            try:
                check_and_send_notifications()
            except Exception as e:
                log_logic(f"Error in notification scheduler loop: {e}")

    thread = threading.Thread(target=run_loop, daemon=True, name="DolphisicNotificationScheduler")
    thread.start()
    log_logic("Notification scheduler background thread started.")


# Trigger scheduler thread startup
start_notification_scheduler()


@app.route('/api/notifications/send', methods=['POST'])
def send_notification():
    settings = load_notification_settings()
    recipient = (request.json or {}).get('email') or settings.get('email_notif')
    if not recipient:
        return jsonify({'error': 'Adresse email destinataire requise'}), 400
    
    log_logic(f"Email send requested for recipient: {recipient} using Brevo SMTP")
    try:
        send_test_email(recipient)
        log_logic(f"Test email successfully sent to {recipient}")
        return jsonify({
            'success': True,
            'message': f"Email de test envoyé avec succès à {recipient} !"
        })
    except Exception as e:
        log_logic(f"Failed to send test email to {recipient}: {str(e)}")
        return jsonify({'error': f"Échec de l'envoi de l'email : {str(e)}"}), 500


@app.route('/api/notifications/run-check', methods=['POST'])
def run_notifications_check():
    force = request.args.get('force', 'false').lower() == 'true'
    log_logic(f"Manual notification check requested (force={force})")
    try:
        check_and_send_notifications(force=force)
        return jsonify({
            'success': True,
            'message': "Vérification des notifications effectuée avec succès !"
        })
    except Exception as e:
        log_logic(f"Manual notification check failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>/toggle-notification', methods=['POST'])
def toggle_device_notification(rowid):
    data = request.json or {}
    active = data.get('notification_active', False)
    email = data.get('email_notif') if active else None
    safe_email = '********' if email else None
    log_logic(f"Toggling notification for Device ID={rowid} | Active={bool(active)} | Email={safe_email}")
    
    try:
        # Check if device exists
        dev = query_db(DB_SDIS, "SELECT rowid FROM parc WHERE rowid = ?", (rowid,), one=True)
        if not dev:
            log_logic(f"Failed to toggle notification: Device ID={rowid} not found")
            return jsonify({'error': 'Équipement introuvable'}), 404
            
        query_db(DB_SDIS, "UPDATE parc SET notification_active = ?, email_notif = ? WHERE rowid = ?",
                 (1 if active else 0, email, rowid), commit=True)
        log_logic(f"Notification updated for Device ID={rowid} | Active={1 if active else 0}")
        return jsonify({
            'success': True, 
            'message': 'Alerte mise à jour avec succès', 
            'notification_active': 1 if active else 0,
            'email_notif': email
        })
    except Exception as e:
        log_logic(f"Failed to toggle notification for Device ID={rowid}: {str(e)}")
        return jsonify({'error': str(e)}), 500


# --- NEW NOTIFICATIONS RELATIONAL API ---
@app.route('/api/notifications/emails', methods=['GET', 'POST'])
def handle_notification_emails():
    if request.method == 'GET':
        try:
            emails = query_db(DB_SDIS, "SELECT id, email, enabled, global_enabled, notify_j_minus_1, notify_j FROM notification_emails")
            return jsonify([dict(row) for row in emails])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # POST: Add new email
    try:
        data = request.json or {}
        email = data.get('email', '').strip()
        if not email:
            return jsonify({'error': 'Adresse email manquante'}), 400
        
        # Insert (enabled = 0 by default)
        email_id = query_db(DB_SDIS, "INSERT INTO notification_emails (email, enabled) VALUES (?, 0)", (email,), commit=True)
        log_logic(f"Added new notification email: {email} (ID: {email_id})")
        return jsonify({
            'success': True,
            'id': email_id,
            'email': email,
            'enabled': 0,
            'global_enabled': 0,
            'notify_j_minus_1': 0,
            'notify_j': 0
        })
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Cette adresse e-mail existe déjà'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/emails/<int:email_id>', methods=['PUT', 'DELETE'])
def handle_single_notification_email(email_id):
    if request.method == 'DELETE':
        try:
            # Delete manually assigned devices to avoid foreign key issues
            query_db(DB_SDIS, "DELETE FROM notification_email_devices WHERE email_id = ?", (email_id,), commit=True)
            # Delete email
            query_db(DB_SDIS, "DELETE FROM notification_emails WHERE id = ?", (email_id,), commit=True)
            log_logic(f"Deleted notification email ID: {email_id}")
            return jsonify({'success': True, 'message': 'E-mail supprimé avec succès'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # PUT: Update configuration
    try:
        data = request.json or {}
        enabled = 1 if data.get('enabled') else 0
        global_enabled = 1 if data.get('global_enabled') else 0
        notify_j_minus_1 = 1 if data.get('notify_j_minus_1') else 0
        notify_j = 1 if data.get('notify_j') else 0

        # Retrieve current configuration to detect toggling global settings on
        old_config = query_db(DB_SDIS, "SELECT email, enabled, global_enabled FROM notification_emails WHERE id = ?", (email_id,), one=True)

        query_db(DB_SDIS, """
            UPDATE notification_emails 
            SET enabled = ?, global_enabled = ?, notify_j_minus_1 = ?, notify_j = ? 
            WHERE id = ?
        """, (enabled, global_enabled, notify_j_minus_1, notify_j, email_id), commit=True)

        log_logic(f"Updated notification email ID {email_id} | enabled={enabled} | global={global_enabled} | J-1={notify_j_minus_1} | J={notify_j}")
        
        email_info = query_db(DB_SDIS, "SELECT email FROM notification_emails WHERE id = ?", (email_id,), one=True)
        if email_info and email_info['email']:
            email = email_info['email'].strip()
            
            # Detect if global notification is newly activated (either enabled toggle on while global was on, or global toggle on while enabled was on)
            is_global_activation = False
            if old_config and enabled == 1 and global_enabled == 1:
                if old_config['enabled'] != 1 or old_config['global_enabled'] != 1:
                    is_global_activation = True

            if is_global_activation:
                log_logic(f"Global notification activated for {email}. Clearing alert history for this email to force catch-up email.")
                history_file = os.path.join(SERVER_DIR, "notification_history.json")
                if os.path.exists(history_file):
                    try:
                        with open(history_file, 'r', encoding='utf-8') as f:
                            hdata = json.load(f)
                        sent_alerts = hdata.get('sent_alerts', [])
                        sent_alerts = [a for a in sent_alerts if a.get('email') != email]
                        with open(history_file, 'w', encoding='utf-8') as f:
                            json.dump({'sent_alerts': sent_alerts}, f, indent=4)
                    except Exception as e:
                        log_logic(f"Failed to clear alert history: {e}")

            if enabled == 1:
                import threading
                log_logic(f"Immediate check triggered in background for {email} after config change")
                threading.Thread(target=check_and_send_notifications, kwargs={'force': False, 'target_email': email}, daemon=True).start()

        return jsonify({'success': True, 'message': 'Configuration mise à jour'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/emails/<int:email_id>/devices', methods=['GET'])
def get_email_devices(email_id):
    try:
        # Join notification_email_devices with parc to get details
        devices = query_db(DB_SDIS, """
            SELECT p.rowid AS id, p.num_serie, p.modele, p.cis, p.date_cle_a_faire
            FROM notification_email_devices d
            JOIN parc p ON d.device_id = p.rowid
            WHERE d.email_id = ?
        """, (email_id,))
        return jsonify([dict(row) for row in devices])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/assign-device', methods=['POST'])
def assign_device_to_email():
    try:
        data = request.json or {}
        device_id = data.get('device_id')
        email_id = data.get('email_id')
        if not device_id or not email_id:
            return jsonify({'error': 'Paramètres device_id et email_id requis'}), 400

        # Check if device and email exist
        dev = query_db(DB_SDIS, "SELECT rowid FROM parc WHERE rowid = ?", (device_id,), one=True)
        email_info = query_db(DB_SDIS, "SELECT id, email FROM notification_emails WHERE id = ?", (email_id,), one=True)
        if not dev or not email_info:
            return jsonify({'error': 'Appareil ou E-mail introuvable'}), 404

        # Insert relationship
        query_db(DB_SDIS, """
            INSERT OR IGNORE INTO notification_email_devices (email_id, device_id)
            VALUES (?, ?)
        """, (email_id, device_id), commit=True)
        
        log_logic(f"Assigned Device ID {device_id} to Email ID {email_id}")

        # Trigger immediate check in background for this email after assignment
        if email_info and email_info['email']:
            import threading
            email = email_info['email'].strip()
            log_logic(f"Immediate check triggered in background for {email} after device assignment")
            threading.Thread(target=check_and_send_notifications, kwargs={'force': False, 'target_email': email}, daemon=True).start()

        return jsonify({'success': True, 'message': 'Appareil lié avec succès aux notifications'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/active-devices', methods=['GET'])
def get_active_notification_devices():
    try:
        devices = query_db(DB_SDIS, """
            SELECT rowid AS id, num_serie, modele, cis, date_cle_a_faire, notification_active
            FROM parc
            WHERE notification_active = 1
        """)
        return jsonify([dict(row) for row in devices])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/emails/<int:email_id>/devices/<int:device_id>', methods=['DELETE'])
def remove_device_from_email(email_id, device_id):
    try:
        query_db(DB_SDIS, """
            DELETE FROM notification_email_devices 
            WHERE email_id = ? AND device_id = ?
        """, (email_id, device_id), commit=True)
        
        log_logic(f"Removed Device ID {device_id} from Email ID {email_id}")
        return jsonify({'success': True, 'message': 'Association supprimée'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- ADVANCED SEARCH ---
@app.route('/api/search/metadata', methods=['GET'])
def get_search_metadata():
    try:
        cis_rows = query_db(DB_SDIS, "SELECT DISTINCT TRIM(cis) as name FROM centres WHERE cis IS NOT NULL ORDER BY name ASC")
        model_rows = query_db(DB_SDIS, "SELECT DISTINCT TRIM(modele) as name FROM materiel WHERE modele IS NOT NULL ORDER BY name ASC")
        types_rows = query_db(DB_SDIS, "SELECT DISTINCT TRIM(type) as name FROM materiel WHERE type IS NOT NULL ORDER BY name ASC")
        return jsonify({
            'centres': [r['name'] for r in cis_rows if r['name']],
            'modeles': [r['name'] for r in model_rows if r['name']],
            'types': [r['name'] for r in types_rows if r['name']]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def advanced_search():
    data = request.json or {}
    
    # Extract criteria
    cis = data.get('cis')
    modele = data.get('modele')
    device_type = data.get('type')
    num_serie = data.get('num_serie')
    affectation = data.get('affectation')
    pocsag = data.get('pocsag') or data.get('code_pocsag')
    rfgi = data.get('rfgi')

    query = """
        SELECT p.rowid as id, p.num_serie, p.modele, m.marque, p.affectation,
               p.date_prog, p.date_maj_cle, p.date_cle_a_faire, p.notification_active, p.email_notif,
               p.code_pocsag, p.immatriculation, p.rfgi, p.version_logiciel, p.classe_service, p.date_achat, p.observation,
               p.cis, m.type, p.statut_activite
        FROM parc p
        LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
        WHERE 1=1
    """
    params = []
    
    if cis:
        query += " AND TRIM(p.cis) = TRIM(?)"
        params.append(cis)
    if modele:
        query += " AND TRIM(p.modele) = TRIM(?)"
        params.append(modele)
    if device_type:
        query += " AND TRIM(m.type) = TRIM(?)"
        params.append(device_type)
    if num_serie:
        query += " AND p.num_serie LIKE ?"
        params.append(f"%{num_serie}%")
    if affectation:
        query += " AND p.affectation LIKE ?"
        params.append(f"%{affectation}%")
    if pocsag:
        query += " AND p.code_pocsag LIKE ?"
        params.append(f"%{pocsag}%")
    if rfgi:
        query += " AND p.rfgi LIKE ?"
        params.append(f"%{rfgi}%")

    try:
        rows = query_db(DB_SDIS, query, params)
        criteria = {
            'cis': cis,
            'modele': modele,
            'type': device_type,
            'num_serie': num_serie,
            'affectation': affectation,
            'pocsag': pocsag,
            'rfgi': rfgi,
        }
        active_criteria = {k: v for k, v in criteria.items() if v}
        log_logic(f"Advanced search results | Criteria: {active_criteria or 'none'} | Count={len(rows)}")
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- STATISTICS ---
@app.route('/api/dashboard/urgent', methods=['GET'])
def get_urgent_dashboard():
    try:
        return jsonify(collect_urgent_operations())
    except Exception as e:
        log_logic(f"Failed to load urgent dashboard: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # Count by Model
        query_models = """
            SELECT p.modele, COALESCE(m.type, 'INCONNU') as type, COUNT(*) as count
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE UPPER(TRIM(COALESCE(p.cis, ''))) != 'TEST'
            GROUP BY p.modele, type
            ORDER BY count DESC
        """
        rows_models = query_db(DB_SDIS, query_models)
        
        # Count by Type (filtered only to BIP, MOBILE, PORTATIF, TOUS, trimmed and grouped)
        query_types = """
            SELECT TRIM(m.type) as type, COUNT(*) as count
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE TRIM(m.type) IN ('BIP', 'MOBILE', 'PORTATIF')
              AND UPPER(TRIM(COALESCE(p.cis, ''))) != 'TEST'
            GROUP BY TRIM(m.type)
            ORDER BY count DESC
        """
        rows_types = query_db(DB_SDIS, query_types)

        # Count by Centre
        query_centres = """
            SELECT TRIM(p.cis) as cis, COUNT(*) as count
            FROM parc p
            WHERE p.cis IS NOT NULL AND TRIM(p.cis) != ''
              AND UPPER(TRIM(p.cis)) != 'TEST'
            GROUP BY cis
            ORDER BY count DESC
        """
        rows_centres = query_db(DB_SDIS, query_centres)
        
        # Get total number of equipments in parc
        total_row = query_db(
            DB_SDIS,
            "SELECT COUNT(*) as total FROM parc WHERE UPPER(TRIM(COALESCE(cis, ''))) != 'TEST'",
            one=True
        )
        total_equipments = total_row['total'] if total_row else 0
        
        return jsonify({
            'by_model': [dict(r) for r in rows_models],
            'by_type': [dict(r) for r in rows_types],
            'by_centre': [dict(r) for r in rows_centres],
            'total_equipments': total_equipments
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- CARTOGRAPHY ---
@app.route('/api/carto', methods=['GET'])
def get_carto_data():
    try:
        # Load sites
        sites = query_db(DB_CARTO, "SELECT id, nom, latitude, longitude, type FROM sites")
        # Load labels
        labels = query_db(DB_CARTO, "SELECT id, texte, latitude, longitude FROM labels_libres")
        # Load liaisons
        liaisons_query = """
            SELECT l.id, l.site_a_id, l.site_b_id, l.label, l.couleur,
                   sA.latitude as lat_a, sA.longitude as lng_a, sA.nom as nom_a,
                   sB.latitude as lat_b, sB.longitude as lng_b, sB.nom as nom_b
            FROM liaisons l
            JOIN sites sA ON l.site_a_id = sA.id
            JOIN sites sB ON l.site_b_id = sB.id
        """
        liaisons = query_db(DB_CARTO, liaisons_query)
        
        return jsonify({
            'sites': [dict(s) for s in sites],
            'labels': [dict(l) for l in labels],
            'liaisons': [dict(li) for li in liaisons]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/sites', methods=['POST'])
def add_or_update_site():
    data = request.json or {}
    site_id = data.get('id')
    nom = data.get('nom')
    lat = data.get('latitude')
    lng = data.get('longitude')
    site_type = data.get('type', 'Point Haut') # Default type

    if not nom or lat is None or lng is None:
        return jsonify({'error': 'Nom, latitude et longitude requis'}), 400

    log_logic(f"Saving Site ID={site_id or 'NEW'}: Name='{nom}', Type='{site_type}', Lat={lat}, Lng={lng}")
    try:
        if site_id:
            query_db(DB_CARTO, "UPDATE sites SET nom = ?, latitude = ?, longitude = ?, type = ? WHERE id = ?",
                     (nom, lat, lng, site_type, site_id), commit=True)
            log_logic(f"Site ID={site_id} updated successfully")
            return jsonify({'success': True, 'id': site_id, 'message': 'Site mis à jour'})
        else:
            new_id = query_db(DB_CARTO, "INSERT INTO sites (nom, latitude, longitude, type) VALUES (?, ?, ?, ?)",
                              (nom, lat, lng, site_type), commit=True)
            log_logic(f"Site created successfully with ID={new_id}")
            return jsonify({'success': True, 'id': new_id, 'message': 'Site créé'})
    except Exception as e:
        log_logic(f"Failed to save site: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/sites/<int:site_id>/delete', methods=['POST'])
def delete_site(site_id):
    log_logic(f"Deleting Site ID={site_id}")
    try:
        # Also clean up liaisons linked to this site
        query_db(DB_CARTO, "DELETE FROM liaisons WHERE site_a_id = ? OR site_b_id = ?", (site_id, site_id), commit=True)
        # Clean up pylones
        query_db(DB_CARTO, "DELETE FROM pylones WHERE site_id = ?", (site_id,), commit=True)
        # Clean up main courante
        query_db(DB_CARTO, "DELETE FROM main_courante WHERE site_id = ?", (site_id,), commit=True)
        # Delete site
        query_db(DB_CARTO, "DELETE FROM sites WHERE id = ?", (site_id,), commit=True)
        log_logic(f"Site ID={site_id} and dependencies deleted successfully")
        return jsonify({'success': True, 'message': 'Site supprimé ainsi que ses dépendances'})
    except Exception as e:
        log_logic(f"Failed to delete Site ID={site_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/labels', methods=['POST'])
def add_label():
    data = request.json or {}
    texte = data.get('texte')
    lat = data.get('latitude')
    lng = data.get('longitude')

    if not texte or lat is None or lng is None:
        return jsonify({'error': 'Texte, latitude et longitude requis'}), 400

    log_logic(f"Adding Free Label: Text='{texte}' at Lat={lat}, Lng={lng}")
    try:
        new_id = query_db(DB_CARTO, "INSERT INTO labels_libres (texte, latitude, longitude) VALUES (?, ?, ?)",
                          (texte, lat, lng), commit=True)
        log_logic(f"Free Label added successfully (ID: {new_id})")
        return jsonify({'success': True, 'id': new_id, 'message': 'Label créé'})
    except Exception as e:
        log_logic(f"Failed to add Free Label: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/labels/<int:label_id>/delete', methods=['POST'])
def delete_label(label_id):
    log_logic(f"Deleting Label ID={label_id}")
    try:
        query_db(DB_CARTO, "DELETE FROM labels_libres WHERE id = ?", (label_id,), commit=True)
        log_logic(f"Label ID={label_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Label supprimé'})
    except Exception as e:
        log_logic(f"Failed to delete Label ID={label_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/liaisons', methods=['POST'])
def add_liaison():
    data = request.json or {}
    site_a_id = data.get('site_a_id')
    site_b_id = data.get('site_b_id')
    label = data.get('label', '')
    couleur = data.get('couleur', '#00FF00') # Default green

    if not site_a_id or not site_b_id:
        return jsonify({'error': 'Sites A et B requis'}), 400

    log_logic(f"Adding Liaison from SiteA={site_a_id} to SiteB={site_b_id} (Label='{label}', Color='{couleur}')")
    try:
        new_id = query_db(DB_CARTO, "INSERT INTO liaisons (site_a_id, site_b_id, label, couleur) VALUES (?, ?, ?, ?)",
                          (site_a_id, site_b_id, label, couleur), commit=True)
        log_logic(f"Liaison created successfully (ID: {new_id})")
        return jsonify({'success': True, 'id': new_id, 'message': 'Liaison créée'})
    except Exception as e:
        log_logic(f"Failed to add Liaison: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/liaisons/<int:liaison_id>/delete', methods=['POST'])
def delete_liaison(liaison_id):
    log_logic(f"Deleting Liaison ID={liaison_id}")
    try:
        query_db(DB_CARTO, "DELETE FROM liaisons WHERE id = ?", (liaison_id,), commit=True)
        log_logic(f"Liaison ID={liaison_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Liaison supprimée'})
    except Exception as e:
        log_logic(f"Failed to delete Liaison ID={liaison_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

# --- SITE DETAIL PANELS ---
@app.route('/api/carto/sites/<int:site_id>/info', methods=['GET', 'POST'])
def site_info(site_id):
    if request.method == 'GET':
        try:
            row = query_db(DB_CARTO, "SELECT inventaire, taches FROM sites WHERE id = ?", (site_id,), one=True)
            if row:
                return jsonify({
                    'inventaire': row['inventaire'] or '',
                    'taches': row['taches'] or ''
                })
            return jsonify({'inventaire': '', 'taches': ''})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else: # POST
        data = request.json or {}
        inventaire = data.get('inventaire', '')
        taches = data.get('taches', '')
        log_logic(f"Updating site info/inventory/tasks for Site ID={site_id}")
        try:
            query_db(DB_CARTO, "UPDATE sites SET inventaire = ?, taches = ? WHERE id = ?", (inventaire, taches, site_id), commit=True)
            log_logic(f"Site ID={site_id} info/inventory/tasks saved successfully")
            return jsonify({'success': True, 'message': 'Informations du site sauvegardées'})
        except Exception as e:
            log_logic(f"Failed to update Site ID={site_id} info: {str(e)}")
            return jsonify({'error': str(e)}), 500

# --- PYLONES CRUD ---
@app.route('/api/carto/sites/<int:site_id>/pylones', methods=['GET'])
def get_pylones(site_id):
    try:
        rows = query_db(DB_CARTO, "SELECT id, nom_pylone, description FROM pylones WHERE site_id = ?", (site_id,))
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/sites/<int:site_id>/pylones', methods=['POST'])
def add_pylone(site_id):
    data = request.json or {}
    nom = data.get('nom_pylone')
    desc = data.get('description', '')
    if not nom:
        return jsonify({'error': 'Nom du pylône requis'}), 400
    log_logic(f"Adding Pylone to Site ID={site_id}: Name='{nom}'")
    try:
        new_id = query_db(DB_CARTO, "INSERT INTO pylones (site_id, nom_pylone, description) VALUES (?, ?, ?)",
                          (site_id, nom, desc), commit=True)
        log_logic(f"Pylone ID={new_id} added successfully to Site ID={site_id}")
        return jsonify({'success': True, 'id': new_id, 'message': 'Pylône ajouté'})
    except Exception as e:
        log_logic(f"Failed to add Pylone: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/pylones/<int:pylone_id>/delete', methods=['POST'])
def delete_pylone(pylone_id):
    log_logic(f"Deleting Pylone ID={pylone_id}")
    try:
        query_db(DB_CARTO, "DELETE FROM pylones WHERE id = ?", (pylone_id,), commit=True)
        log_logic(f"Pylone ID={pylone_id} deleted successfully")
        return jsonify({'success': True, 'message': 'Pylône supprimé'})
    except Exception as e:
        log_logic(f"Failed to delete Pylone ID={pylone_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

# --- MAIN COURANTE CRUD ---
@app.route('/api/carto/sites/<int:site_id>/main_courante', methods=['GET'])
def get_main_courante(site_id):
    try:
        rows = query_db(DB_CARTO, "SELECT id, date_heure, evenement FROM main_courante WHERE site_id = ? ORDER BY id DESC", (site_id,))
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/sites/<int:site_id>/main_courante', methods=['POST'])
def add_main_courante(site_id):
    data = request.json or {}
    evenement = data.get('evenement')
    if not evenement:
        return jsonify({'error': "Texte de l'événement requis"}), 400
    try:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = query_db(DB_CARTO, "INSERT INTO main_courante (site_id, date_heure, evenement) VALUES (?, ?, ?)",
                          (site_id, date_str, evenement), commit=True)
        return jsonify({'success': True, 'id': new_id, 'date_heure': date_str, 'message': 'Événement ajouté'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/main_courante/<int:item_id>/delete', methods=['POST'])
def delete_main_courante(item_id):
    try:
        query_db(DB_CARTO, "DELETE FROM main_courante WHERE id = ?", (item_id,), commit=True)
        return jsonify({'success': True, 'message': 'Événement supprimé'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- LIAISONS INFO ---
@app.route('/api/carto/liaisons/<int:liaison_id>/info', methods=['GET', 'POST'])
def liaison_info(liaison_id):
    if request.method == 'GET':
        try:
            row = query_db(DB_CARTO, "SELECT notes FROM liaisons WHERE id = ?", (liaison_id,), one=True)
            return jsonify({'notes': row['notes'] or '' if row else ''})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else: # POST
        data = request.json or {}
        notes = data.get('notes', '')
        try:
            query_db(DB_CARTO, "UPDATE liaisons SET notes = ? WHERE id = ?", (notes, liaison_id), commit=True)
            return jsonify({'success': True, 'message': 'Notes de liaison sauvegardées'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# --- DOCUMENTS (FILE MANAGEMENT) ---
@app.route('/api/carto/documents', methods=['GET'])
def get_documents():
    parent_id = request.args.get('parent_id')
    parent_type = request.args.get('parent_type')
    if not parent_id or not parent_type:
        return jsonify({'error': 'parent_id et parent_type requis'}), 400
    try:
        rows = query_db(DB_CARTO, "SELECT id, nom_fichier, chemin_relatif FROM documents WHERE parent_id = ? AND parent_type = ?",
                          (parent_id, parent_type))
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/upload', methods=['POST'])
def upload_document():
    parent_id = request.form.get('parent_id')
    parent_type = request.form.get('parent_type')
    
    if not parent_id or not parent_type:
        return jsonify({'error': 'parent_id et parent_type requis'}), 400
        
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    log_logic(f"Uploading file for ParentType='{parent_type}', ParentID='{parent_id}': Filename='{file.filename}'")
    try:
        filename = secure_filename(file.filename)
        # Create a folder structure inside the upload folder if needed
        # Standard: parent_type_parent_id_filename
        unique_filename = f"{parent_type}_{parent_id}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        
        # Save reference in database
        # Relative path from documents_pylones folder
        rel_path = unique_filename
        new_id = query_db(DB_CARTO, "INSERT INTO documents (parent_id, parent_type, nom_fichier, chemin_relatif) VALUES (?, ?, ?, ?)",
                          (parent_id, parent_type, filename, rel_path), commit=True)
                          
        log_logic(f"File uploaded successfully (ID: {new_id}, Path: {rel_path})")
        return jsonify({
            'success': True,
            'document': {
                'id': new_id,
                'nom_fichier': filename,
                'chemin_relatif': rel_path
            },
            'message': 'Fichier téléversé avec succès'
        })
    except Exception as e:
        log_logic(f"Failed to upload file '{file.filename}': {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/documents/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    log_logic(f"Deleting document ID={doc_id}")
    try:
        row = query_db(DB_CARTO, "SELECT chemin_relatif FROM documents WHERE id = ?", (doc_id,), one=True)
        if not row:
            log_logic(f"Failed to delete document ID={doc_id}: Document not found")
            return jsonify({'error': 'Document introuvable'}), 404
            
        chemin = row['chemin_relatif']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], chemin)
        
        # Delete file if exists
        if os.path.exists(filepath):
            os.remove(filepath)
            
        # Delete DB row
        query_db(DB_CARTO, "DELETE FROM documents WHERE id = ?", (doc_id,), commit=True)
        log_logic(f"Document ID={doc_id} deleted successfully from disk and DB")
        return jsonify({'success': True, 'message': 'Document supprimé'})
    except Exception as e:
        log_logic(f"Failed to delete document ID={doc_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/documents/<int:doc_id>/download', methods=['GET'])
def download_document(doc_id):
    try:
        row = query_db(DB_CARTO, "SELECT chemin_relatif, nom_fichier FROM documents WHERE id = ?", (doc_id,), one=True)
        if not row:
            return jsonify({'error': 'Document introuvable'}), 404
            
        chemin = row['chemin_relatif']
        return send_from_directory(app.config['UPLOAD_FOLDER'], chemin, as_attachment=True, download_name=row['nom_fichier'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- STOCK & LOAN MANAGEMENT ---
@app.route('/api/stock', methods=['GET'])
def get_stock():
    try:
        # Get all stock items and join with their currently active loan if there is one
        query = """
            SELECT s.id, s.nom, s.description, s.type_materiel, s.etat, s.statut,
                   s.modele, s.num_serie, s.cis, s.pocsag, s.rfgi, s.identifiant,
                   p.id as active_pret_id, p.emprunteur, p.date_debut, p.date_fin
            FROM stock s
            LEFT JOIN prets p ON s.id = p.stock_id AND p.date_rendu IS NULL
            ORDER BY s.id DESC
        """
        rows = query_db(DB_SDIS, query)
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock', methods=['POST'])
def add_stock_item():
    data = request.json or {}
    description = data.get('description', '')
    type_materiel = data.get('type_materiel')
    etat = data.get('etat')
    modele = data.get('modele', '')
    num_serie = data.get('num_serie', '')
    cis = data.get('cis', '')
    pocsag = data.get('pocsag', '')
    rfgi = data.get('rfgi', '')
    identifiant = data.get('identifiant', '')
    
    nom = data.get('nom')
    if not nom:
        if modele and num_serie:
            nom = f"{modele} ({num_serie})"
        elif modele:
            nom = modele
        else:
            nom = "Matériel"

    if not type_materiel or not etat:
        return jsonify({'error': 'Type de matériel et état requis'}), 400
        
    log_logic(f"Adding stock item: Nom='{nom}', Type='{type_materiel}', Etat='{etat}'")
    try:
        query = """
            INSERT INTO stock 
            (nom, description, type_materiel, etat, statut, modele, num_serie, cis, pocsag, rfgi, identifiant) 
            VALUES (?, ?, ?, ?, 'Disponible', ?, ?, ?, ?, ?, ?)
        """
        item_id = query_db(DB_SDIS, query, (nom, description, type_materiel, etat, modele, num_serie, cis, pocsag, rfgi, identifiant), commit=True)
        log_logic(f"Stock item added successfully (ID: {item_id})")
        return jsonify({'success': True, 'id': item_id, 'message': 'Matériel ajouté au stock avec succès'})
    except Exception as e:
        log_logic(f"Failed to add stock item '{nom}': {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<int:item_id>', methods=['DELETE'])
def delete_stock_item(item_id):
    log_logic(f"Deleting stock item ID={item_id}")
    try:
        # Also clean up loans history for this item
        query_db(DB_SDIS, "DELETE FROM prets WHERE stock_id = ?", (item_id,), commit=True)
        query_db(DB_SDIS, "DELETE FROM stock WHERE id = ?", (item_id,), commit=True)
        log_logic(f"Stock item ID={item_id} and loan history deleted successfully")
        return jsonify({'success': True, 'message': 'Matériel supprimé du stock avec succès'})
    except Exception as e:
        log_logic(f"Failed to delete stock item ID={item_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<int:item_id>/prets', methods=['POST'])
def create_loan(item_id):
    data = request.json or {}
    emprunteur = data.get('emprunteur')
    date_debut = data.get('date_debut')
    date_fin = data.get('date_fin')
    
    if not emprunteur or not date_debut or not date_fin:
        return jsonify({'error': 'Emprunteur, date de début et date de fin requis'}), 400
        
    log_logic(f"Creating loan for Stock Item ID={item_id} | Emprunteur='{emprunteur}', Dates: {date_debut} to {date_fin}")
    try:
        # Check if item is available
        item = query_db(DB_SDIS, "SELECT statut FROM stock WHERE id = ?", (item_id,), one=True)
        if not item:
            log_logic(f"Failed to create loan: Stock item ID={item_id} not found")
            return jsonify({'error': 'Matériel introuvable'}), 404
        if item['statut'] != 'Disponible':
            log_logic(f"Failed to create loan: Stock item ID={item_id} status is '{item['statut']}'")
            return jsonify({'error': 'Ce matériel est déjà prêté ou indisponible'}), 400
            
        # Insert loan
        loan_query = "INSERT INTO prets (stock_id, emprunteur, date_debut, date_fin) VALUES (?, ?, ?, ?)"
        loan_id = query_db(DB_SDIS, loan_query, (item_id, emprunteur, date_debut, date_fin), commit=True)
        
        # Update stock status
        query_db(DB_SDIS, "UPDATE stock SET statut = 'Prêté' WHERE id = ?", (item_id,), commit=True)
        log_logic(f"Loan ID={loan_id} created successfully for Stock Item ID={item_id}")
        return jsonify({'success': True, 'id': loan_id, 'message': 'Prêt enregistré avec succès'})
    except Exception as e:
        log_logic(f"Failed to create loan for stock item ID={item_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/prets/<int:pret_id>/retour', methods=['POST'])
def return_loan(pret_id):
    data = request.json or {}
    changement_etat = data.get('changement_etat', '')
    nouveau_statut_etat = data.get('nouveau_statut_etat') # If they want to update the device's condition
    date_rendu = datetime.now().strftime("%Y-%m-%d")
    
    log_logic(f"Returning loan ID={pret_id} | Changement etat: '{changement_etat}', Nouveau statut/etat: '{nouveau_statut_etat}'")
    try:
        # Fetch loan info
        loan = query_db(DB_SDIS, "SELECT stock_id FROM prets WHERE id = ?", (pret_id,), one=True)
        if not loan:
            log_logic(f"Failed to return loan: Loan ID={pret_id} not found")
            return jsonify({'error': 'Prêt introuvable'}), 404
            
        stock_id = loan['stock_id']
        
        # Update loan record
        update_loan = "UPDATE prets SET date_rendu = ?, changement_etat = ? WHERE id = ?"
        query_db(DB_SDIS, update_loan, (date_rendu, changement_etat, pret_id), commit=True)
        
        # Update stock item status back to 'Disponible'
        if nouveau_statut_etat:
            query_db(DB_SDIS, "UPDATE stock SET statut = 'Disponible', etat = ? WHERE id = ?", (nouveau_statut_etat, stock_id), commit=True)
        else:
            query_db(DB_SDIS, "UPDATE stock SET statut = 'Disponible' WHERE id = ?", (stock_id,), commit=True)
            
        log_logic(f"Loan ID={pret_id} returned successfully (Stock Item ID={stock_id})")
        return jsonify({'success': True, 'message': 'Retour de matériel confirmé'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<int:item_id>/prets', methods=['GET'])
def get_loan_history(item_id):
    try:
        # Fetch all loans for this stock item (ordered by start date descending)
        rows = query_db(DB_SDIS, "SELECT id, emprunteur, date_debut, date_fin, date_rendu, changement_etat FROM prets WHERE stock_id = ? ORDER BY date_debut DESC, id DESC", (item_id,))
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- SERVE REACT FRONTEND ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the compiled React frontend for any non-API route."""
    if path and os.path.exists(os.path.join(DIST_DIR, path)):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, 'index.html')

if __name__ == '__main__':
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = '127.0.0.1'
    print(f"""\n{'='*55}\n  DolphiSIC - Serveur en cours d'execution\n{'='*55}\n  Acces local    : http://localhost:5000\n  Acces reseau   : http://{local_ip}:5000\n{'='*55}\n""")
    app.run(host='0.0.0.0', port=5000, debug=False)
