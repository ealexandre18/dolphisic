# Modèle Conceptuel de Données (MCD) - DolphiSIC

Ce document présente le Modèle Conceptuel de Données (MCD) des deux bases de données qui composent l'application **DolphiSIC** (`sdis04.db` et `carto_sdis04.db`).

---

## 1. Diagramme Entité-Association (Mermaid ERD)

```mermaid
erDiagram
    %% sdis04.db - Gestion du Parc & Stock
    UTILISATEUR {
        int id PK
        string identifiant
        string mot_de_passe
        string role
    }

    CENTRE {
        string cis PK
        string comptage
    }

    MATERIEL {
        string modele PK
        string type
        string marque
        string valeur_compta
    }

    EQUIPEMENT_PARC {
        string num_serie PK
        string modele FK
        string cis FK
        string affectation
        string code_pocsag
        string immatriculation
        string rfgi
        string classe_service
        string version_logiciel
        string date_prog
        string date_maj_cle
        string date_cle_a_faire
        string date_achat
        string observation
        string verification
        string champ1
        int notification_active
        string email_notif
        string statut_activite
    }

    STOCK {
        int id PK
        string nom
        string description
        string type_materiel
        string etat
        string statut
        string modele
        string num_serie
        string cis
        string pocsag
        string rfgi
        string identifiant
    }

    PRET {
        int id PK
        int stock_id FK
        string emprunteur
        string date_debut
        string date_fin
        string date_rendu
        string changement_etat
    }

    CENTRE ||--o{ EQUIPEMENT_PARC : "abrite"
    MATERIEL ||--o{ EQUIPEMENT_PARC : "instancie"
    STOCK ||--o{ PRET : "subit"

    %% carto_sdis04.db - Cartographie & Exploitation
    SITE {
        int id PK
        string nom
        float latitude
        float longitude
        string inventaire
        string taches
        string type
    }

    PYLONE {
        int id PK
        int site_id FK
        string nom_pylone
        string description
    }

    MAIN_COURANTE {
        int id PK
        int site_id FK
        string date_heure
        string evenement
    }

    LIAISON {
        int id PK
        int site_a_id FK
        int site_b_id FK
        string label
        string couleur
        string notes
    }

    DOCUMENT {
        int id PK
        int parent_id
        string parent_type
        string nom_fichier
        string chemin_relatif
    }

    LABEL_LIBRE {
        int id PK
        string texte
        float latitude
        float longitude
    }

    SITE ||--o{ PYLONE : "possede"
    SITE ||--o{ MAIN_COURANTE : "concerne"
    SITE ||--o{ LIAISON : "emplit_site_a"
    SITE ||--o{ LIAISON : "emplit_site_b"
```

---

## 2. Description des Associations et Cardinalités

### Base de données : `sdis04.db`

1. **CENTRE <-> EQUIPEMENT_PARC**
   - **Règle** : Un centre de secours (CIS) abrite de 0 à N équipements de parc. Un équipement appartient à au plus 1 centre d'affectation.
   - **Cardinalités** : `CENTRE (0,N) <--- affecte ---> (0,1) EQUIPEMENT_PARC`

2. **MATERIEL <-> EQUIPEMENT_PARC**
   - **Règle** : Un matériel de référence définit les propriétés communes de 0 à N terminaux physiques dans le parc. Un équipement physique correspond à 1 modèle de matériel unique.
   - **Cardinalités** : `MATERIEL (0,N) <--- definit ---> (1,1) EQUIPEMENT_PARC`

3. **STOCK <-> PRET**
   - **Règle** : Un matériel présent dans le stock peut faire l'objet de 0 à N prêts successifs dans le temps. Un prêt donné concerne 1 et 1 seul matériel du stock.
   - **Cardinalités** : `STOCK (0,N) <--- prete ---> (1,1) PRET`

### Base de données : `carto_sdis04.db`

1. **SITE <-> PYLONE**
   - **Règle** : Un site cartographique (point haut/perroquet) possède de 0 à N pylônes de relais. Un pylône est implanté sur 1 unique site.
   - **Cardinalités** : `SITE (0,N) <--- héberge ---> (1,1) PYLONE`

2. **SITE <-> MAIN_COURANTE**
   - **Règle** : Un site cartographique possède un historique d'événements de 0 à N lignes de main courante. Une ligne de main courante concerne 1 seul site.
   - **Cardinalités** : `SITE (0,N) <--- trace ---> (1,1) MAIN_COURANTE`

3. **SITE <-> LIAISON (Liaisons Radio)**
   - **Règle** : Une liaison radio s'établit entre deux sites (site A de départ, site B d'arrivée). Un site peut être impliqué dans 0 à N liaisons distinctes.
   - **Cardinalités** :
     - `SITE (0,N) <--- origine ---> (1,1) LIAISON`
     - `SITE (0,N) <--- destination ---> (1,1) LIAISON`

4. **DOCUMENT (Polymorphisme Conceptuel)**
   - **Règle** : Un document (PDF, photo, schéma) est attaché à un site ou à une liaison (`parent_type` détermine la table liée et `parent_id` contient l'identifiant).
