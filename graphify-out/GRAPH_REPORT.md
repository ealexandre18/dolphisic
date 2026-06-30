# Graph Report - PROJET SDIS  (2026-06-30)

## Corpus Check
- 59 files · ~152,664 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3433 nodes · 10927 edges · 97 communities (85 shown, 12 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b8e9c51e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_V2 Server API Endpoints|V2 Server API Endpoints]]
- [[_COMMUNITY_Core Server API Endpoints|Core Server API Endpoints]]
- [[_COMMUNITY_Server Site & Asset Operations|Server Site & Asset Operations]]
- [[_COMMUNITY_Database Models & Schemas|Database Models & Schemas]]
- [[_COMMUNITY_UI Design & Styles|UI Design & Styles]]
- [[_COMMUNITY_Device Cryptography & Key Management|Device Cryptography & Key Management]]
- [[_COMMUNITY_V2 Cryptography & Key Management|V2 Cryptography & Key Management]]
- [[_COMMUNITY_Project Architecture & Structure|Project Architecture & Structure]]
- [[_COMMUNITY_Database Check Scripts|Database Check Scripts]]
- [[_COMMUNITY_Site Database Comparison|Site Database Comparison]]
- [[_COMMUNITY_Leaflet CSS Comparison|Leaflet CSS Comparison]]
- [[_COMMUNITY_Full Database Validation|Full Database Validation]]
- [[_COMMUNITY_Directory Structure Comparison|Directory Structure Comparison]]
- [[_COMMUNITY_Site Exporter Scripts|Site Exporter Scripts]]
- [[_COMMUNITY_Server UI Logging|Server UI Logging]]
- [[_COMMUNITY_Server Authentication & Security|Server Authentication & Security]]
- [[_COMMUNITY_Frontend Static File Serving|Frontend Static File Serving]]
- [[_COMMUNITY_V2 Server Authentication|V2 Server Authentication]]
- [[_COMMUNITY_V2 Frontend File Serving|V2 Frontend File Serving]]
- [[_COMMUNITY_Server Compare Script|Server Compare Script]]
- [[_COMMUNITY_SVG Search Script|SVG Search Script]]
- [[_COMMUNITY_JS Code Search Script|JS Code Search Script]]
- [[_COMMUNITY_JS Category Search Script|JS Category Search Script]]
- [[_COMMUNITY_JS Selector Search Script|JS Selector Search Script]]
- [[_COMMUNITY_V2 Design Documentation|V2 Design Documentation]]
- [[_COMMUNITY_V2 Data Model Documentation|V2 Data Model Documentation]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 197|Community 197]]
- [[_COMMUNITY_Community 246|Community 246]]

## God Nodes (most connected - your core abstractions)
1. `$()` - 750 edges
2. `$()` - 750 edges
3. `$()` - 750 edges
4. `$()` - 750 edges
5. `_update()` - 79 edges
6. `_update()` - 79 edges
7. `_update()` - 79 edges
8. `_update()` - 79 edges
9. `i()` - 65 edges
10. `i()` - 65 edges

## Surprising Connections (you probably didn't know these)
- `at()` --calls--> `t()`  [EXTRACTED]
  app/public/assets/index-DyRupmtp.js → app/public/assets/index-DyRupmtp.js  _Bridges community 41 → community 0_
- `cf()` --calls--> `t()`  [EXTRACTED]
  app/public/assets/index-DyRupmtp.js → app/public/assets/index-DyRupmtp.js  _Bridges community 41 → community 28_
- `re()` --calls--> `t()`  [EXTRACTED]
  app/public/assets/index-DyRupmtp.js → app/public/assets/index-DyRupmtp.js  _Bridges community 41 → community 29_
- `t()` --calls--> `Pt()`  [EXTRACTED]
  app/public/assets/index-DyRupmtp.js → app/public/assets/index-DyRupmtp.js  _Bridges community 41 → community 3_
- `cr()` --calls--> `n()`  [EXTRACTED]
  app/public/assets/index-DyRupmtp.js → app/public/assets/index-DyRupmtp.js  _Bridges community 41 → community 26_

## Import Cycles
- None detected.

## Communities (97 total, 12 thin omitted)

### Community 0 - "V2 Server API Endpoints"
Cohesion: 0.07
Nodes (69): ad(), ap(), as(), at(), Au(), bu(), Co(), Cu() (+61 more)

### Community 1 - "Core Server API Endpoints"
Cohesion: 0.13
Nodes (14): carto_sdis04 SQLite Database, EQUIPEMENT_PARC Entity, sdis04 SQLite Database, SITES Entity, STOCK Entity, 📊 1. Base de Données de Gestion (`sdis04.db`), 🗺️ 2. Base de Données Cartographique (`carto.db`), 📋 3. Règles de Gestion Clés (+6 more)

### Community 2 - "Server Site & Asset Operations"
Cohesion: 0.02
Nodes (124): $(), acquireContext(), addControllers(), addPlugins(), addScales(), afterDraw(), afterTickToLabelConversion(), ar() (+116 more)

### Community 3 - "Database Models & Schemas"
Cohesion: 0.02
Nodes (123): $(), aa(), addBox(), addControllers(), addElements(), addPlugins(), addScales(), afterAutoSkip() (+115 more)

### Community 4 - "UI Design & Styles"
Cohesion: 0.67
Nodes (3): Data-Dense Dashboard Style, Real-Time / Operations Landing Pattern, Dashboard Design Specifications (UTF-8)

### Community 5 - "Device Cryptography & Key Management"
Cohesion: 0.02
Nodes (126): $(), active(), addControllers(), addElements(), addPlugins(), addScales(), afterAutoSkip(), afterDraw() (+118 more)

### Community 6 - "V2 Cryptography & Key Management"
Cohesion: 0.03
Nodes (106): acquireContext(), afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterDatasetsUpdate(), afterFit(), afterSetDimensions(), afterUpdate() (+98 more)

### Community 7 - "Project Architecture & Structure"
Cohesion: 0.08
Nodes (41): beforeLayout(), bl(), cl(), Ct(), dl(), ea(), el(), et() (+33 more)

### Community 8 - "Database Check Scripts"
Cohesion: 0.09
Nodes (39): applyStack(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference(), _computeAngle(), countVisibleElements() (+31 more)

### Community 9 - "Site Database Comparison"
Cohesion: 0.07
Nodes (67): ad(), ap(), at(), Au(), bf(), bs(), bu(), buildTicks() (+59 more)

### Community 10 - "Leaflet CSS Comparison"
Cohesion: 0.02
Nodes (122): $(), aa(), active(), addBox(), addControllers(), addElements(), addPlugins(), addScales() (+114 more)

### Community 11 - "Full Database Validation"
Cohesion: 0.06
Nodes (56): Al(), buildTicks(), ca(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelItems(), computeTickLimit() (+48 more)

### Community 12 - "Directory Structure Comparison"
Cohesion: 0.05
Nodes (70): Al(), applyStack(), ca(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference() (+62 more)

### Community 13 - "Site Exporter Scripts"
Cohesion: 0.15
Nodes (14): aa(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), generateLabels(), _getSortedDatasetMetas(), getSortedVisibleDatasetMetas(), getVisibleDatasetCount() (+6 more)

### Community 14 - "Server UI Logging"
Cohesion: 0.04
Nodes (135): a(), ac(), ae(), ai(), Ao(), apply(), b(), ba() (+127 more)

### Community 15 - "Server Authentication & Security"
Cohesion: 0.04
Nodes (153): a(), ac(), add(), addEventListener(), ae(), ai(), alpha(), Ao() (+145 more)

### Community 16 - "Frontend Static File Serving"
Cohesion: 0.04
Nodes (89): addElements(), afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterDatasetsUpdate(), afterFit(), afterSetDimensions(), afterUpdate() (+81 more)

### Community 17 - "V2 Server Authentication"
Cohesion: 0.04
Nodes (135): a(), ac(), ae(), ai(), Ao(), apply(), b(), ba() (+127 more)

### Community 18 - "V2 Frontend File Serving"
Cohesion: 0.04
Nodes (92): acquireContext(), afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterDatasetsUpdate(), afterFit(), afterSetDimensions(), afterUpdate() (+84 more)

### Community 19 - "Server Compare Script"
Cohesion: 0.03
Nodes (107): aa(), acquireContext(), addBox(), afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterDatasetsUpdate(), afterFit() (+99 more)

### Community 20 - "SVG Search Script"
Cohesion: 0.07
Nodes (69): ad(), ap(), as(), at(), Au(), bu(), Co(), Cu() (+61 more)

### Community 21 - "JS Code Search Script"
Cohesion: 0.06
Nodes (74): ad(), ap(), as(), at(), Au(), bu(), buildTicks(), Co() (+66 more)

### Community 22 - "JS Category Search Script"
Cohesion: 0.07
Nodes (51): adjustHitBoxes(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelArea(), _computeLabelItems(), computeTickLimit(), _computeTitleHeight() (+43 more)

### Community 23 - "JS Selector Search Script"
Cohesion: 0.08
Nodes (24): dependencies, clsx, framer-motion, lucide-react, next, react, react-dom, tailwind-merge (+16 more)

### Community 26 - "Community 26"
Cohesion: 0.07
Nodes (44): adjustHitBoxes(), afterDraw(), _computeTitleHeight(), cr(), cs(), draw(), _drawArgs(), drawBody() (+36 more)

### Community 27 - "Community 27"
Cohesion: 0.07
Nodes (56): adjustHitBoxes(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelArea(), _computeLabelItems(), computeTickLimit(), _computeTitleHeight() (+48 more)

### Community 28 - "Community 28"
Cohesion: 0.09
Nodes (47): add(), addEventListener(), af(), bd(), bt(), _cachedScopes(), cf(), de() (+39 more)

### Community 29 - "Community 29"
Cohesion: 0.07
Nodes (51): alpha(), beforeLayout(), bl(), cl(), Ct(), D(), dl(), E() (+43 more)

### Community 30 - "Community 30"
Cohesion: 0.05
Nodes (69): Al(), applyStack(), ca(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference() (+61 more)

### Community 31 - "Community 31"
Cohesion: 0.06
Nodes (48): buildTicks(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelItems(), computeTickLimit(), determineDataLimits(), diff() (+40 more)

### Community 32 - "Community 32"
Cohesion: 0.09
Nodes (51): add(), addEventListener(), af(), bd(), bt(), _cachedScopes(), cf(), de() (+43 more)

### Community 33 - "Community 33"
Cohesion: 0.07
Nodes (60): add(), addEventListener(), af(), afterAutoSkip(), bd(), bt(), buildLookupTable(), _cachedScopes() (+52 more)

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (14): An(), average(), bn(), getCenterPoint(), getProps(), hasValue(), inRange(), inXRange() (+6 more)

### Community 35 - "Community 35"
Cohesion: 0.10
Nodes (37): Al(), beforeLayout(), bl(), cl(), dl(), el(), first(), fl() (+29 more)

### Community 36 - "Community 36"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 37 - "Community 37"
Cohesion: 0.11
Nodes (45): get_smtp_config(), , (rowid,), one=True)         if not device:             return jsonify({'erro, update_device(), add_device(), bulk_delete_devices(), bulk_update_device_cryptage(), calculate_next_key_date(), check_and_send_notifications() (+37 more)

### Community 38 - "Community 38"
Cohesion: 0.11
Nodes (37): addBox(), af(), bt(), _cachedScopes(), df(), ef(), ep(), ff() (+29 more)

### Community 39 - "Community 39"
Cohesion: 0.12
Nodes (16): aliases, components, hooks, lib, ui, utils, rsc, $schema (+8 more)

### Community 40 - "Community 40"
Cohesion: 0.10
Nodes (35): beforeLayout(), bl(), cl(), dl(), ea(), el(), first(), fl() (+27 more)

### Community 41 - "Community 41"
Cohesion: 0.04
Nodes (128): a(), ac(), ae(), ai(), Ao(), apply(), b(), ba() (+120 more)

### Community 42 - "Community 42"
Cohesion: 0.05
Nodes (65): adjustHitBoxes(), afterDraw(), alpha(), _computeLabelArea(), _computeTitleHeight(), cr(), cs(), D() (+57 more)

### Community 43 - "Community 43"
Cohesion: 0.07
Nodes (52): applyStack(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference(), _computeAngle(), countVisibleElements() (+44 more)

### Community 44 - "Community 44"
Cohesion: 0.15
Nodes (17): active(), _animateOptions(), cancel(), _createAnimations(), _createDescriptors(), da(), _descriptors(), ks() (+9 more)

### Community 45 - "Community 45"
Cohesion: 0.08
Nodes (24): dependencies, clsx, framer-motion, lucide-react, next, react, react-dom, tailwind-merge (+16 more)

### Community 46 - "Community 46"
Cohesion: 0.20
Nodes (14): An(), average(), bn(), getCenterPoint(), getProps(), hasValue(), inRange(), inXRange() (+6 more)

### Community 47 - "Community 47"
Cohesion: 0.09
Nodes (32): cs(), easeInOutElastic(), Ed(), en(), er(), Fn(), fr(), Ft() (+24 more)

### Community 48 - "Community 48"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 49 - "Community 49"
Cohesion: 0.12
Nodes (16): aliases, components, hooks, lib, ui, utils, rsc, $schema (+8 more)

### Community 50 - "Community 50"
Cohesion: 0.17
Nodes (12): afterAutoSkip(), buildLookupTable(), cd(), getDecimalForPixel(), getDecimalForValue(), getValueForPixel(), hp(), initOffsets() (+4 more)

### Community 52 - "Community 52"
Cohesion: 0.20
Nodes (14): An(), average(), bn(), getCenterPoint(), getProps(), hasValue(), inRange(), inXRange() (+6 more)

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (14): An(), average(), bn(), getCenterPoint(), getProps(), hasValue(), inRange(), inXRange() (+6 more)

### Community 54 - "Community 54"
Cohesion: 0.22
Nodes (8): Accessibility & Inclusion, Anti-references, Brand Personality, Design Principles, Product, Product Purpose, Register, Users

### Community 55 - "Community 55"
Cohesion: 0.25
Nodes (7): Color, Components, DolphiSIC Design System, Motion, Overview, Typography, UX Rules

### Community 56 - "Community 56"
Cohesion: 0.33
Nodes (4): menus, viewIds, viewLabels, Window

### Community 57 - "Community 57"
Cohesion: 0.33
Nodes (4): menus, viewIds, viewLabels, Window

### Community 59 - "Community 59"
Cohesion: 0.40
Nodes (4): 📊 1. MCD de Gestion & Suivi (`sdis04.db`), 🗺️ 2. MCD de Cartographie (`carto.db`), Codes Mocodo pour la génération des MCD, 💡 Rappel sur la syntaxe Mocodo et les cardinalités utilisées :

### Community 60 - "Community 60"
Cohesion: 0.40
Nodes (3): start.sh script, DOLPHISIC_PORT, NODE_OPTIONS

### Community 62 - "Community 62"
Cohesion: 0.40
Nodes (4): DolphiSIC Redesign, Installation manuelle, Lancement complet, Structure

### Community 70 - "Community 70"
Cohesion: 0.40
Nodes (4): DolphiSIC Redesign, Installation manuelle, Lancement complet, Structure

### Community 71 - "Community 71"
Cohesion: 0.40
Nodes (3): DOLPHISIC_PORT, NODE_OPTIONS, start.sh script

### Community 94 - "Community 94"
Cohesion: 0.15
Nodes (17): active(), _animateOptions(), cancel(), _createAnimations(), _createDescriptors(), da(), _descriptors(), ks() (+9 more)

### Community 197 - "Community 197"
Cohesion: 0.05
Nodes (90): add_device(), bulk_delete_devices(), bulk_update_device_cryptage(), calculate_next_key_date(), check_and_send_notifications(), collect_urgent_operations(), Colors, delete_device() (+82 more)

### Community 246 - "Community 246"
Cohesion: 0.06
Nodes (33): Project Structure Flattening, 1. Retrait et Centrage des Cartes KPI du Tableau de bord, 1. Résolution de l'Alignement Horizontal Éparpillé des Noms (Bug de largeur Leaflet en Onglet Caché), 1. Résolution de l'Erreur de Sérialisation JSON, 1. Simplification de la Structure du Projet (Flattening), 1. Structure de la Base de Données Relationnelle, 1. Suppression Totale des Hashes (`#`) de l'URL, 2. Activation du Système de Mail avec les configurations Brevo SMTP (+25 more)

## Knowledge Gaps
- **195 isolated node(s):** `metadata`, `Window`, `menus`, `viewIds`, `viewLabels` (+190 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `$()` connect `Database Models & Schemas` to `V2 Server API Endpoints`, `V2 Cryptography & Key Management`, `Database Check Scripts`, `Community 41`, `Full Database Validation`, `Community 44`, `Community 46`, `Community 26`, `Community 28`, `Community 29`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `$()` connect `Device Cryptography & Key Management` to `Community 32`, `Community 40`, `Community 47`, `V2 Server Authentication`, `Server Compare Script`, `JS Code Search Script`, `JS Category Search Script`, `Community 53`, `Community 30`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `$()` connect `Server Site & Asset Operations` to `Community 34`, `Community 38`, `Project Architecture & Structure`, `Site Database Comparison`, `Directory Structure Comparison`, `Site Exporter Scripts`, `Server Authentication & Security`, `Frontend Static File Serving`, `Community 50`, `Community 27`, `Community 94`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **What connects `metadata`, `Window`, `menus` to the rest of the system?**
  _197 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `V2 Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.06564364876385337 - nodes in this community are weakly interconnected._
- **Should `Core Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `Server Site & Asset Operations` be split into smaller, more focused modules?**
  _Cohesion score 0.019270604481827883 - nodes in this community are weakly interconnected._