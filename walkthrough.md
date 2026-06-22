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
