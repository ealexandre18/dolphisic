import os
import sys
import sqlite3
import hashlib
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

# Resolve the directory of server.py using its absolute path.
# This works regardless of the working directory when Python is launched.
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
# Change cwd to SERVER_DIR so SQLite relative paths always resolve correctly.
os.chdir(SERVER_DIR)

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
        raise e

# --- AUTHENTICATION ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Veuillez saisir un identifiant et un mot de passe'}), 400

    try:
        user_row = query_db(DB_SDIS, "SELECT mot_de_passe, role FROM utilisateurs WHERE identifiant = ?", (username,), one=True)
        if user_row and verify_hash(password, user_row['mot_de_passe']):
            return jsonify({
                'success': True,
                'user': {
                    'username': username,
                    'role': user_row['role'] or 'USER'
                },
                'token': f"dummy-session-token-{username}"
            })
        return jsonify({'error': 'Identifiant ou mot de passe incorrect'}), 401
    except Exception as e:
        return jsonify({'error': f"Erreur de connexion base: {str(e)}"}), 500

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
                   p.statut_activite
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE TRIM(p.cis) = TRIM(?) AND TRIM(m.type) = TRIM(?)
        """
        rows = query_db(DB_SDIS, query, (cis, device_type))
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
    try:
        query_db(DB_SDIS, "UPDATE parc SET date_maj_cle = ?, date_cle_a_faire = ?, notification_active = 0, email_notif = NULL WHERE rowid = ?", 
                 (date_maj, date_a_faire, rowid), commit=True)
        return jsonify({'success': True, 'message': 'Dates de chiffrement mises à jour avec succès', 'date_cle_a_faire': date_a_faire})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>/delete', methods=['POST'])
def delete_device(rowid):
    try:
        query_db(DB_SDIS, "DELETE FROM parc WHERE rowid = ?", (rowid,), commit=True)
        return jsonify({'success': True, 'message': 'Équipement supprimé avec succès'})
    except Exception as e:
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

    try:
        # Check if model exists
        model_row = query_db(DB_SDIS, "SELECT modele FROM materiel WHERE TRIM(modele) = TRIM(?)", (modele,), one=True)
        if not model_row:
            return jsonify({'error': f"Le modèle '{modele}' n'existe pas dans le référentiel matériel"}), 400

        query = """
            INSERT INTO parc (cis, modele, num_serie, affectation, version_logiciel, observation, date_maj_cle, date_cle_a_faire, date_prog)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        date_prog = datetime.now().strftime("%Y-%m-%d")
        new_rowid = query_db(DB_SDIS, query, 
                             (cis, modele, num_serie, affectation, version_logiciel, observation, date_maj_cle, date_cle_a_faire, date_prog), 
                             commit=True)
        return jsonify({'success': True, 'id': new_rowid, 'message': 'Équipement ajouté au parc avec succès', 'date_cle_a_faire': date_cle_a_faire})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- NOTIFICATIONS SETTINGS ---
@app.route('/api/notifications/settings', methods=['GET', 'POST'])
def handle_notification_settings():
    if request.method == 'GET':
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify(data)
            # Default fallback settings
            return jsonify({
                "global_notification_enabled": False,
                "notify_exceeded": True,
                "notify_approaching": True,
                "email_notif": ""
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else: # POST
        try:
            data = request.json or {}
            # Write to JSON file
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return jsonify({'success': True, 'message': 'Paramètres de notification enregistrés'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/devices/<int:rowid>/toggle-notification', methods=['POST'])
def toggle_device_notification(rowid):
    data = request.json or {}
    active = data.get('notification_active', False)
    email = data.get('email_notif') if active else None
    
    try:
        # Check if device exists
        dev = query_db(DB_SDIS, "SELECT rowid FROM parc WHERE rowid = ?", (rowid,), one=True)
        if not dev:
            return jsonify({'error': 'Équipement introuvable'}), 404
            
        query_db(DB_SDIS, "UPDATE parc SET notification_active = ?, email_notif = ? WHERE rowid = ?",
                 (1 if active else 0, email, rowid), commit=True)
        return jsonify({
            'success': True, 
            'message': 'Alerte mise à jour avec succès', 
            'notification_active': 1 if active else 0,
            'email_notif': email
        })
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
    observation = data.get('observation')
    version_logiciel = data.get('version_logiciel')

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
    if observation:
        query += " AND p.observation LIKE ?"
        params.append(f"%{observation}%")
    if version_logiciel:
        query += " AND p.version_logiciel LIKE ?"
        params.append(f"%{version_logiciel}%")

    try:
        rows = query_db(DB_SDIS, query, params)
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- STATISTICS ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # Count by Model
        query_models = """
            SELECT p.modele, COALESCE(m.type, 'INCONNU') as type, COUNT(*) as count
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            GROUP BY p.modele, type
            ORDER BY count DESC
        """
        rows_models = query_db(DB_SDIS, query_models)
        
        # Count by Type (filtered only to BIP, MOBILE, PORTATIF, TOUS, trimmed and grouped)
        query_types = """
            SELECT TRIM(m.type) as type, COUNT(*) as count
            FROM parc p
            LEFT JOIN materiel m ON TRIM(p.modele) = TRIM(m.modele)
            WHERE TRIM(m.type) IN ('BIP', 'MOBILE', 'PORTATIF', 'TOUS')
            GROUP BY TRIM(m.type)
            ORDER BY count DESC
        """
        rows_types = query_db(DB_SDIS, query_types)

        # Count by Centre
        query_centres = """
            SELECT TRIM(p.cis) as cis, COUNT(*) as count
            FROM parc p
            WHERE p.cis IS NOT NULL AND TRIM(p.cis) != ''
            GROUP BY cis
            ORDER BY count DESC
        """
        rows_centres = query_db(DB_SDIS, query_centres)
        
        # Get total number of equipments in parc
        total_row = query_db(DB_SDIS, "SELECT COUNT(*) as total FROM parc", one=True)
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

    try:
        if site_id:
            query_db(DB_CARTO, "UPDATE sites SET nom = ?, latitude = ?, longitude = ?, type = ? WHERE id = ?",
                     (nom, lat, lng, site_type, site_id), commit=True)
            return jsonify({'success': True, 'id': site_id, 'message': 'Site mis à jour'})
        else:
            new_id = query_db(DB_CARTO, "INSERT INTO sites (nom, latitude, longitude, type) VALUES (?, ?, ?, ?)",
                              (nom, lat, lng, site_type), commit=True)
            return jsonify({'success': True, 'id': new_id, 'message': 'Site créé'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/sites/<int:site_id>/delete', methods=['POST'])
def delete_site(site_id):
    try:
        # Also clean up liaisons linked to this site
        query_db(DB_CARTO, "DELETE FROM liaisons WHERE site_a_id = ? OR site_b_id = ?", (site_id, site_id), commit=True)
        # Clean up pylones
        query_db(DB_CARTO, "DELETE FROM pylones WHERE site_id = ?", (site_id,), commit=True)
        # Clean up main courante
        query_db(DB_CARTO, "DELETE FROM main_courante WHERE site_id = ?", (site_id,), commit=True)
        # Delete site
        query_db(DB_CARTO, "DELETE FROM sites WHERE id = ?", (site_id,), commit=True)
        
        return jsonify({'success': True, 'message': 'Site supprimé ainsi que ses dépendances'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/labels', methods=['POST'])
def add_label():
    data = request.json or {}
    texte = data.get('texte')
    lat = data.get('latitude')
    lng = data.get('longitude')

    if not texte or lat is None or lng is None:
        return jsonify({'error': 'Texte, latitude et longitude requis'}), 400

    try:
        new_id = query_db(DB_CARTO, "INSERT INTO labels_libres (texte, latitude, longitude) VALUES (?, ?, ?)",
                          (texte, lat, lng), commit=True)
        return jsonify({'success': True, 'id': new_id, 'message': 'Label créé'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/labels/<int:label_id>/delete', methods=['POST'])
def delete_label(label_id):
    try:
        query_db(DB_CARTO, "DELETE FROM labels_libres WHERE id = ?", (label_id,), commit=True)
        return jsonify({'success': True, 'message': 'Label supprimé'})
    except Exception as e:
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

    try:
        new_id = query_db(DB_CARTO, "INSERT INTO liaisons (site_a_id, site_b_id, label, couleur) VALUES (?, ?, ?, ?)",
                          (site_a_id, site_b_id, label, couleur), commit=True)
        return jsonify({'success': True, 'id': new_id, 'message': 'Liaison créée'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/liaisons/<int:liaison_id>/delete', methods=['POST'])
def delete_liaison(liaison_id):
    try:
        query_db(DB_CARTO, "DELETE FROM liaisons WHERE id = ?", (liaison_id,), commit=True)
        return jsonify({'success': True, 'message': 'Liaison supprimée'})
    except Exception as e:
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
        try:
            query_db(DB_CARTO, "UPDATE sites SET inventaire = ?, taches = ? WHERE id = ?", (inventaire, taches, site_id), commit=True)
            return jsonify({'success': True, 'message': 'Informations du site sauvegardées'})
        except Exception as e:
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
    try:
        new_id = query_db(DB_CARTO, "INSERT INTO pylones (site_id, nom_pylone, description) VALUES (?, ?, ?)",
                          (site_id, nom, desc), commit=True)
        return jsonify({'success': True, 'id': new_id, 'message': 'Pylône ajouté'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/pylones/<int:pylone_id>/delete', methods=['POST'])
def delete_pylone(pylone_id):
    try:
        query_db(DB_CARTO, "DELETE FROM pylones WHERE id = ?", (pylone_id,), commit=True)
        return jsonify({'success': True, 'message': 'Pylône supprimé'})
    except Exception as e:
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
        return jsonify({'error': str(e)}), 500

@app.route('/api/carto/documents/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    try:
        row = query_db(DB_CARTO, "SELECT chemin_relatif FROM documents WHERE id = ?", (doc_id,), one=True)
        if not row:
            return jsonify({'error': 'Document introuvable'}), 404
            
        chemin = row['chemin_relatif']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], chemin)
        
        # Delete file if exists
        if os.path.exists(filepath):
            os.remove(filepath)
            
        # Delete DB row
        query_db(DB_CARTO, "DELETE FROM documents WHERE id = ?", (doc_id,), commit=True)
        return jsonify({'success': True, 'message': 'Document supprimé'})
    except Exception as e:
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
        
    try:
        query = """
            INSERT INTO stock 
            (nom, description, type_materiel, etat, statut, modele, num_serie, cis, pocsag, rfgi, identifiant) 
            VALUES (?, ?, ?, ?, 'Disponible', ?, ?, ?, ?, ?, ?)
        """
        item_id = query_db(DB_SDIS, query, (nom, description, type_materiel, etat, modele, num_serie, cis, pocsag, rfgi, identifiant), commit=True)
        return jsonify({'success': True, 'id': item_id, 'message': 'Matériel ajouté au stock avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<int:item_id>', methods=['DELETE'])
def delete_stock_item(item_id):
    try:
        # Also clean up loans history for this item
        query_db(DB_SDIS, "DELETE FROM prets WHERE stock_id = ?", (item_id,), commit=True)
        query_db(DB_SDIS, "DELETE FROM stock WHERE id = ?", (item_id,), commit=True)
        return jsonify({'success': True, 'message': 'Matériel supprimé du stock avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<int:item_id>/prets', methods=['POST'])
def create_loan(item_id):
    data = request.json or {}
    emprunteur = data.get('emprunteur')
    date_debut = data.get('date_debut')
    date_fin = data.get('date_fin')
    
    if not emprunteur or not date_debut or not date_fin:
        return jsonify({'error': 'Emprunteur, date de début et date de fin requis'}), 400
        
    try:
        # Check if item is available
        item = query_db(DB_SDIS, "SELECT statut FROM stock WHERE id = ?", (item_id,), one=True)
        if not item:
            return jsonify({'error': 'Matériel introuvable'}), 404
        if item['statut'] != 'Disponible':
            return jsonify({'error': 'Ce matériel est déjà prêté ou indisponible'}), 400
            
        # Insert loan
        loan_query = "INSERT INTO prets (stock_id, emprunteur, date_debut, date_fin) VALUES (?, ?, ?, ?)"
        loan_id = query_db(DB_SDIS, loan_query, (item_id, emprunteur, date_debut, date_fin), commit=True)
        
        # Update stock status
        query_db(DB_SDIS, "UPDATE stock SET statut = 'Prêté' WHERE id = ?", (item_id,), commit=True)
        
        return jsonify({'success': True, 'id': loan_id, 'message': 'Prêt enregistré avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prets/<int:pret_id>/retour', methods=['POST'])
def return_loan(pret_id):
    data = request.json or {}
    changement_etat = data.get('changement_etat', '')
    nouveau_statut_etat = data.get('nouveau_statut_etat') # If they want to update the device's condition
    date_rendu = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Fetch loan info
        loan = query_db(DB_SDIS, "SELECT stock_id FROM prets WHERE id = ?", (pret_id,), one=True)
        if not loan:
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
