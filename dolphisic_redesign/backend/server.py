import os
import sys
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
          AND UPPER(TRIM(COALESCE(m.type, ''))) NOT IN ('BIP', 'BIPS')
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


@app.route('/api/notifications/send', methods=['POST'])
def send_notification_placeholder():
    settings = load_notification_settings()
    recipient = (request.json or {}).get('email') or settings.get('email_notif')
    if not recipient:
        return jsonify({'error': 'Adresse email destinataire requise'}), 400
    log_logic(f"Email send requested for recipient: {recipient} (provider not configured)")
    return jsonify({
        'success': False,
        'message': "Bouton prêt. Configuration d'envoi à compléter."
    })

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


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'dolphisic-redesign-backend'})


# --- SERVE REACT FRONTEND ---
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the compiled React frontend for any non-API route."""
    if path and os.path.exists(os.path.join(DIST_DIR, path)):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('DOLPHISIC_PORT', '5001'))
    print(f"""\n{'='*55}\n  DolphiSIC Redesign - Backend en cours d'execution\n{'='*55}\n  Application : http://localhost:3005\n  API locale  : http://127.0.0.1:{port}/api/health\n{'='*55}\n""")
    app.run(host='127.0.0.1', port=port, debug=False)
