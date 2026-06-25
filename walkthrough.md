# Rapport de Walkthrough - Restructuration du Projet et Correction de la Base de Données

Toutes les étapes pour simplifier et aplatir la structure du projet afin d'avoir une application web autonome et exécutable par simple copier-coller à la racine de `PROJET SDIS/` ont été complétées avec succès.

---

## 🛠️ Modifications Apportées

### 1. Simplification de la Structure du Projet (Flattening)
- **Déplacement des fichiers de production** :
  - Le dossier `dist/` (contenant le frontend React compilé) a été déplacé à la racine du projet.
  - Le script serveur `server.py` et le lanceur `start.bat` ont été également positionnés à la racine.
- **Suppression des composants obsolètes** :
  - Suppression de la version desktop Python (`Cryptis.exe`, scripts d'installation, sources du dossier `src/`, dossiers de test).
  - Suppression de la version web alternative obsolète `cryptisweb2/`.
  - La racine du projet ne contient désormais que le strict menu minimal nécessaire au bon fonctionnement de la version Web (**DolphiSIC**).

### 2. Résolution du Bug d'Accès à la Base de Données
- **Correction dans `server.py`** :
  - **Problème** : Une seconde définition de `BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))` à la ligne 55 écrasait la valeur correcte et ciblait le dossier parent (`Desktop/`), provoquant l'erreur `no such table: utilisateurs` lors du chargement des bases de données.
  - **Correction** : Cette ligne a été modifiée pour réutiliser `SERVER_DIR` (`BASE_DIR = SERVER_DIR`), assurant que les bases de données SQLite `sdis04.db` et `carto_sdis04.db` soient recherchées et lues dans le dossier racine du projet.

### 3. Correction de l'Affichage et du Défilement des Onglets (Points Hauts / Perroquets)
- **Problème** : Les 6 onglets de la vue détaillée d'un site (Inventaire, Tâches, Infos, Pylônes, Log, Documents) débordaient sur les écrans standards et le texte de l'onglet "Documents" était coupé (seule la lettre "D" était visible). De plus, la classe `no-scrollbar` masquait complètement la barre de défilement horizontal, rendant le glissement impossible sur ordinateur.
- **Correction apportées dans le code frontend compilé** :
  - **Élargissement du volet latéral (Drawer)** : La largeur du tiroir d'informations est passée de `380px` à `410px` pour offrir plus d'espace de lecture.
  - **Optimisation des espacements** : L'espace (gap) entre les onglets a été réduit à `8px` pour maximiser la visibilité directe des boutons sans avoir besoin de faire défiler.
  - **Intégration d'une barre de défilement moderne** : Remplacement de la classe `no-scrollbar` par une classe personnalisée `.drawer-tabs-scrollbar` dans `index.css`. Cette classe configure une barre de défilement horizontale très fine (4px de hauteur) et discrète, reprenant la couleur principale de l'application (`var(--primary)`).

### 4. Refonte du Formulaire d'Ajout et de Gestion des Stocks
- **Nouveau Schéma de Base de Données** :
  - La table `stock` a été modifiée (avec scripts de migration automatique) pour accueillir 6 nouvelles colonnes : `modele`, `num_serie`, `cis`, `pocsag`, `rfgi` et `identifiant`.
- **Formulaire de saisie dynamique (Modal)** :
  - L'état initial du matériel et la description restent saisissables.
  - Sélection d'un type de matériel parmi : `BIP`, `Antares`, `Analogique`, `Accessoire`, `Autre`.
  - Si le type est `BIP`, `Antares` ou `Analogique` :
    - Sélection du **Modèle** parmi une liste filtrée spécifique au type.
    - Saisie obligatoire du **CIS** et du **Numéro de série**.
    - Affichage conditionnel de champs requis supplémentaires : **POCSAG** (si BIP), **RFGI** (si Antares) ou **Identifiant** (si Analogique).
  - Si le type est `Accessoire` ou `Autre` :
    - Saisie d'un nom libre pour le matériel (comportement d'origine).
- **Correction du Bug d'Enregistrement** :
  - **Problème** : Lors de la soumission du formulaire d'ajout avec un type radio (BIP, Antares, Analogique), l'application ne s'enregistrait pas. C'était dû à une condition de validation JavaScript qui bloquait la requête si le champ `nom` (masqué pour ces types) était vide.
  - **Correction** : La validation a été modifiée pour autoriser l'enregistrement si soit le `nom` (pour les accessoires/autres) soit le `modele` (pour les radios) est présent.
- **Affichage détaillé (Drawer)** :
  - Le panneau d'information (tiroir) du stock affiche désormais toutes ces informations détaillées de manière structurée lorsqu'un appareil est sélectionné.

### 5. Correction de la Suppression des Liaisons et Ajout des Boutons de Suppression Globaux
- **Bug de suppression des liaisons** :
  - **Problème** : Cliquer sur le bouton de suppression d'une liaison déclenchait une erreur de référence (`handleDeleteLiaison is not defined`) car la fonction n'avait pas été déclarée dans le frontend.
  - **Correction** : Remplacement de l'appel erroné par une fonction asynchrone en ligne qui effectue un appel `POST` on `/api/carto/liaisons/<id>/delete` puis rafraîchit la carte et ferme le tiroir.
- **Accessibilité des boutons de suppression des Sites et des Liaisons** :
  - **Problème** : Pour supprimer un site (point haut ou perroquet), le bouton n'était visible que sous l'onglet spécifique "Infos", ce qui le rendait difficile d'accès. De plus, il n'y avait aucun moyen rapide de supprimer une liaison.
  - **Correction** : Ajout de boutons de suppression dédiés (icône corbeille rouge `Ne`) directement dans l'en-tête du volet latéral (à gauche du bouton de fermeture). Ces boutons sont visibles dès qu'un site ou une liaison est sélectionné(e), quel que soit l'onglet affiché.

---

## 🧪 Validation du Fonctionnement

Le serveur a été lancé localement à des fins de test avec les résultats suivants :
- **Authentification (`/api/login`)** : **OK** (les identifiants d'administration sont validés avec succès via la table `utilisateurs` de la base SQLite).
- **Ressources Statiques (`/`)** : **OK** (le frontend Web est correctement servi par Flask).
- **API Données (`/api/centres`)** : **OK** (les 51 centres de secours sont bien récupérés depuis la base locale SQLite).
- **Styles & Interface** : Le menu détaillé des points hauts s'affiche correctement sans couper l'onglet "Documents" et intègre désormais sa barre de défilement discrète.
- **Ajout Stock** : Le formulaire dynamique affiche correctement les nouveaux champs en fonction du type sélectionné et les données sont correctement sauvegardées (le bug d'enregistrement bloqué a été résolu) et affichées dans la base de données.
- **Suppression Carto** : Les liaisons radio peuvent désormais être supprimées avec succès. Les boutons de suppression des sites et des liaisons sont visibles et fonctionnels directement depuis l'en-tête du tiroir d'information.

---

## 🚀 Comment Déployer et Copier le Projet

Le dossier principal `PROJET SDIS` est maintenant totalement autonome. Pour le transférer sur une autre machine :
1. **Copiez/Collez** le dossier entier `PROJET SDIS/` sur le nouvel ordinateur.
2. Sur la machine hôte, double-cliquez sur le fichier [start.bat](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/start.bat) pour démarrer l'application. Le script installera automatiquement les modules requis (`flask` et `flask-cors`) s'ils ne sont pas présents, démarrera le serveur, affichera l'adresse IP locale à utiliser sur le réseau, et ouvrira l'application dans votre navigateur.

---

## 🎨 Redesign DolphiSIC - Navigation et Centrage de la Barre

Nous avons finalisé l'intégration du redesign en résolvant tous les points bloquants de navigation, de rendu et de conflit de port :

### 1. Suppression Totale des Hashes (`#`) de l'URL
- La navigation Next.js n'utilise plus de fragments de hash `#` dans la barre d'adresse. Elle est entièrement pilotée par un état React local (`activeTab`) dans [page.tsx](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/app/page.tsx).
- Les clics sur les liens du menu sont interceptés et annulés (`preventDefault()`) pour conserver une URL propre de type `http://localhost:3005/`.

### 2. Contrôleur de Navigation Unifié (`window.changeLegacyView`) dans l'IIFE de l'Iframe
- Pour permettre d'accéder sans problème à toutes les pages (incluant la "Cartographie" et les onglets du sous-menu), nous avons injecté une fonction globale `window.changeLegacyView` à l'intérieur de la fermeture lexicale (IIFE) des fichiers HTML ([index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/public/legacy/index.html) et [index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dist/index.html)).
- Cette fonction centralise le basculement entre les extensions personnalisées (Dashboard, Settings) et les vues React de base de l'Iframe, s'assurant de masquer ou d'afficher correctement les panneaux correspondants via `openExtension` et `closeExtension` en fonction de la vue demandée.

### 3. Résolution de Conflit de Port (Port 3005 par Défaut)
- Pour éviter les blocages lorsque le port 3000 est déjà occupé, le port par défaut du serveur de développement Next.js a été configuré sur le port **3005** dans [package.json](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/package.json).
- Le script lanceur [start-redesign.bat](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/start-redesign.bat) démarre et ouvre automatiquement le site sur le port 3005.

### 4. Centrage du Menu de Navigation
- Le bloc contenant le logo et le titre "DolphiSIC" est maintenant placé en position absolue à gauche (`absolute left-4`), libérant le flux horizontal pour centrer parfaitement la barre de menus au milieu du header.
- La liste `<ul>` du composant de navigation dans [navbar.tsx](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/components/ui/navbar.tsx) a été complétée avec le style `justify-center` pour un alignement horizontal parfait.

### 5. Correction de l'Animation de Soulignement Rouge (Framer Motion)
- Suppression d'un doublon de clé `layoutId="cursor"` présent sur le conteneur du sous-menu déroulant (dropdown) dans [navbar.tsx](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/components/ui/navbar.tsx), qui interférait avec Framer Motion et bloquait le rendu du trait rouge lors du survol de l'onglet "Parc matériel".

---

## 🎨 Simplification des KPI et Intégration Brevo (Dernières modifications)

### 1. Retrait et Centrage des Cartes KPI du Tableau de bord
- **Suppression des cartes** : Les deux blocs HTML correspondant aux KPI "Échéance après 30 jours" (id `#valid-count`) et "Équipements suivis" (id `#total-count`) ont été retirés de [index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/public/legacy/index.html).
- **Sécurisation JavaScript** : Les lignes JavaScript affectant le `textContent` de ces deux éléments ont été supprimées dans la fonction `updateDashboardFilter` pour éviter toute erreur de type `TypeError: Cannot set properties of null (setting 'textContent')`. Les variables de calcul ont été préservées pour ne pas altérer les indicateurs circulaires et barres d'échéances du bas de page.
- **Centrage horizontal** : La classe `.dolphi-dashboard-kpis` a été ajustée pour n'occuper que 3 colonnes (`grid-template-columns: repeat(3, minmax(0, 360px))`) et est désormais parfaitement centrée sur la largeur de l'écran grâce à l'ajout de `justify-content: center` dans ses règles de style CSS.

### 2. Activation du Système de Mail avec les configurations Brevo SMTP
- **Client SMTP Python** : Intégration de la fonction `send_test_email` dans les deux fichiers serveurs backend : [dolphisic_redesign/backend/server.py](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/backend/server.py) et [server.py](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/server.py).
- **Identifiants Brevo** : Configuration en STARTTLS (port 587) sur l'hôte `smtp-relay.brevo.com` avec l'adresse d'expédition et d'identification `afb5b1001@smtp-brevo.com`.
- **Adresse d'expédition personnalisée** : Ajout de la configuration `smtp_from = "dolphisic@outlook.fr"` pour définir l'expéditeur de l'enveloppe SMTP et de l'en-tête `From:`.
- **E-mail HTML Premium** : Lors du clic sur le bouton de test dans l'onglet **Paramètres**, l'application envoie un e-mail au format HTML stylisé reprenant la charte graphique de Dolphisic (dégradés sombres, typographie soignée, bloc d'information structuré).
- **Validation** : Les tests d'envoi ont été validés avec succès via un script de test dédié, confirmant que le routage des notifications fonctionne.
- **Débogage SMTP** : Intégration de traces logiques détaillées dans la console (`[LOGIC]`) pour chaque étape de l'envoi de mail (connexion, EHLO, STARTTLS, authentification SMTP, réponse de livraison du serveur 250 OK, déconnexion).
- **Sécurisation par variable d'environnement** :
  - Création de fonctions `load_env()` au démarrage de chaque serveur Python pour lire de manière transparente un fichier local `.env` sans dépendance externe.
  - Remplacement du mot de passe en dur par un appel à `os.environ.get("SMTP_PASSWORD")` afin d'éviter tout blocage de type fuite de clé secrète par GitHub lors des `git push`.
  - Ajout des fichiers locaux `.env` aux règles `.gitignore` du projet (à la racine et dans `dolphisic_redesign/`) afin de les exclure du suivi de version.

### 3. Automatisation et Consolidation des Notifications d'Échéance
- **Seeding d'équipements de test dynamiques** : Insertion et mise à jour automatique de 3 appareils sous le CIS `TEST` dans la base SQLite à chaque démarrage (1 expirant aujourd'hui, 2 expirant demain). Leurs dates d'échéances sont recalculées dynamiquement à la volée.
- **Moteur d'analyse J et J-1** : Développement de la routine `check_and_send_notifications` qui balaie le parc à la recherche des cryptages arrivant à échéance le jour même (aujourd'hui) ou 1 jour à l'avance (demain).
- **Consolidation par destinataire** : Si la notification générale est active, tous les appareils concernés du parc sont regroupés dans **un seul et unique e-mail récapitulatif** envoyé à l'adresse globale. De même pour les alertes d'équipements individuels, regroupées par destinataire pour éviter la réception d'e-mails séparés.
- **Historique anti-doublon** : Suivi des envois dans `notification_history.json` pour garantir qu'aucune notification n'est renvoyée inutilement (par exemple suite à des redémarrages serveur).
- **Planification en tâche de fond** : Démarrage d'un thread démon (`start_notification_scheduler`) qui effectue une vérification automatique au lancement puis toutes les 4 heures.
- **Endpoint de déclenchement manuel** : Exposition de la route POST `/api/notifications/run-check` pour forcer manuellement la vérification, supportant également le paramètre `?force=true` pour contourner l'anti-doublon lors des phases de tests.
- **Validation** : Les tests d'intégration complets ont validé que les 3 appareils de test (1 aujourd'hui et 2 demain) sont bien regroupés en un unique e-mail HTML premium et envoyés avec succès.

### 4. Paramétrage et Déclenchement Immédiat
- **Ajout de l'option dans l'interface** : Ajout d'un interrupteur (toggle switch) "Notification globale" dans la section Paramètres de l'application ([dolphisic_redesign/public/legacy/index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/public/legacy/index.html) et [dist/index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dist/index.html)).
- **Déclenchement instantané à la sauvegarde** : Dès que l'utilisateur active l'option dans ses paramètres et clique sur "Enregistrer", le serveur Python lance immédiatement une routine de vérification en tâche de fond. Si des appareils sont dépassés, pour aujourd'hui ou pour demain, l'utilisateur reçoit instantanément son rapport consolidé (sans attendre le déclenchement périodique du planificateur de 4h).

---

## 🔔 Nouveau Système de Notifications Relationnel et Menu Dédié (Dernières modifications)

### 1. Structure de la Base de Données Relationnelle
- Ajout de deux nouvelles tables SQLite dans `init_db()` sur les deux serveurs (`server.py` et `dolphisic_redesign/backend/server.py`) :
  - `notification_emails` : Gère les destinataires e-mail et leurs configurations personnalisées (Global vs. Individuel, filtres J/J-1).
  - `notification_email_devices` : Gère les associations manuelles d'appareils avec cascading.

### 2. API REST CRUD et Moteur Mis à Jour
- Implémentation complète de l'API de gestion des notifications (`/api/notifications/emails`, `/api/notifications/assign-device`, etc.).
- Refonte du moteur de notification `check_and_send_notifications` pour s'adapter à la structure relationnelle et envoyer un rapport consolidé distinct à chaque destinataire.
- Historique d'envoi anti-doublon indexé par destinataire, appareil, date et type.

### 3. Interface Graphique et Routage
- Création de la page **"Notifications"** (vue moderne à deux colonnes) à la place de l'ancienne option d'e-mail unique des Paramètres.
- Intégration dans la barre de navigation Next.js.
- Ajout du bouton d'association cloche (🔔) dans les colonnes Actions du tableau des équipements. Cliquer sur la cloche d'un appareil l'associe instantanément à l'e-mail actif en `localStorage`.

### 4. Validation
- Les tests d'intégration complets via script python ont validé que les rapports globaux et par appareil sont compilés de façon isolée et envoyés avec succès.

---

## 🛠️ Corrections et Améliorations Ergonomiques de la Page Notifications

### 1. Résolution de l'Erreur de Sérialisation JSON
- **Problème** : Lors de la navigation vers l'onglet "Notifications", le chargement des données échouait et affichait un message d'erreur rouge : `Erreur de chargement des emails: Object of type Row is not JSON serializable`. Ce bug survenait car les points d'accès API Flask renvoyaient directement des listes de lignes brutes de type `sqlite3.Row` (configuré via `row_factory`).
- **Correction** : Les endpoints de l'API relationnelle de notifications ont été modifiés dans [server.py](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/server.py) et [dolphisic_redesign/backend/server.py](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/backend/server.py) pour transformer chaque ligne en dictionnaire Python (`dict(row)`) avant la sérialisation via `jsonify()`. Les routes corrigées incluent :
  - `GET /api/notifications/emails`
  - `GET /api/notifications/emails/<int:email_id>/devices`
  - `GET /api/notifications/active-devices`

### 2. Condensation et Alignement Graphique
- **Problème** : La vue de notifications s'étirait sur toute la largeur de l'écran, ce qui rendait l'interface vide et peu ergonomique sur des écrans d'ordinateurs larges.
- **Correction** :
  - Ajout d'un conteneur principal `#dolphi-notifications-form` doté d'une largeur maximale de `1100px` et centré horizontalement avec des marges automatiques (`margin: 0 auto;`).
  - Ajustement de la grille à deux colonnes pour équilibrer les proportions : la colonne de gauche (gestion et configuration) occupe désormais `1.15fr` et la colonne de droite (équipements assignés) occupe `0.85fr`, séparées par un espace (gap) plus net de `28px`.

### 3. Ajustement des Espacements (Aération des Titres et Formulaires)
- **Problème** : Le titre "Gestion des Destinataires" et les autres titres de section étaient trop collés aux éléments de formulaire (champs de saisie, tableaux, sélecteurs) à cause d'une règle globale `margin: 0;` sur les balises `h2`.
- **Correction** : Injection de marges inférieures spécifiques inline sur les titres `h2` concernés dans les fichiers [dolphisic_redesign/public/legacy/index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dolphisic_redesign/public/legacy/index.html) et [dist/index.html](file:///c:/Users/Ewan%20Alexandre/Desktop/PROJET%20SDIS/dist/index.html) :
  - `margin-bottom: 16px` sous *Gestion des Destinataires* et *Sélectionnez une adresse pour la configurer* afin d'aérer les inputs.
  - `margin-bottom: 8px` sous *Équipements sous Surveillance Individuelle* pour offrir une transition douce vers le paragraphe de description.
