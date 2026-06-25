# Graph Report - PROJET SDIS  (2026-06-23)

## Corpus Check
- 27 files · ~154,069 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1873 nodes · 5779 edges · 97 communities (88 shown, 9 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6d10438`
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
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 123|Community 123]]
- [[_COMMUNITY_Community 174|Community 174]]
- [[_COMMUNITY_Community 178|Community 178]]
- [[_COMMUNITY_Community 179|Community 179]]
- [[_COMMUNITY_Community 180|Community 180]]
- [[_COMMUNITY_Community 182|Community 182]]
- [[_COMMUNITY_Community 185|Community 185]]
- [[_COMMUNITY_Community 189|Community 189]]
- [[_COMMUNITY_Community 190|Community 190]]
- [[_COMMUNITY_Community 191|Community 191]]
- [[_COMMUNITY_Community 195|Community 195]]
- [[_COMMUNITY_Community 196|Community 196]]
- [[_COMMUNITY_Community 197|Community 197]]
- [[_COMMUNITY_Community 198|Community 198]]
- [[_COMMUNITY_Community 199|Community 199]]
- [[_COMMUNITY_Community 202|Community 202]]
- [[_COMMUNITY_Community 230|Community 230]]
- [[_COMMUNITY_Community 231|Community 231]]
- [[_COMMUNITY_Community 232|Community 232]]
- [[_COMMUNITY_Community 233|Community 233]]
- [[_COMMUNITY_Community 234|Community 234]]
- [[_COMMUNITY_Community 235|Community 235]]
- [[_COMMUNITY_Community 236|Community 236]]
- [[_COMMUNITY_Community 238|Community 238]]
- [[_COMMUNITY_Community 242|Community 242]]
- [[_COMMUNITY_Community 245|Community 245]]
- [[_COMMUNITY_Community 246|Community 246]]
- [[_COMMUNITY_Community 260|Community 260]]
- [[_COMMUNITY_Community 261|Community 261]]
- [[_COMMUNITY_Community 267|Community 267]]
- [[_COMMUNITY_Community 268|Community 268]]
- [[_COMMUNITY_Community 269|Community 269]]

## God Nodes (most connected - your core abstractions)
1. `$()` - 750 edges
2. `$()` - 750 edges
3. `_update()` - 79 edges
4. `_update()` - 79 edges
5. `i()` - 65 edges
6. `i()` - 65 edges
7. `query_db()` - 48 edges
8. `query_db()` - 45 edges
9. `log_logic()` - 43 edges
10. `dc()` - 41 edges

## Surprising Connections (you probably didn't know these)
- `get_centres()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_devices()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_stats()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_carto_data()` --references--> `carto_sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `_generate_intelligent_overrides()` --calls--> `search()`  [INFERRED]
  .codex/skills/ui-ux-pro-max/scripts/design_system.py → .codex/skills/ui-ux-pro-max/scripts/core.py

## Import Cycles
- None detected.

## Communities (97 total, 9 thin omitted)

### Community 0 - "V2 Server API Endpoints"
Cohesion: 0.24
Nodes (12): a(), ae(), br(), eo(), ff(), gt(), H(), q() (+4 more)

### Community 1 - "Core Server API Endpoints"
Cohesion: 0.06
Nodes (80): carto_sdis04 SQLite Database, EQUIPEMENT_PARC Entity, sdis04 SQLite Database, SITES Entity, STOCK Entity, 1. Diagramme Entité-Association (Mermaid ERD), 2. Description des Associations et Cardinalités, Base de données : `carto_sdis04.db` (+72 more)

### Community 2 - "Server Site & Asset Operations"
Cohesion: 0.19
Nodes (17): apply(), D(), E(), ee(), g(), gr(), ie(), ks() (+9 more)

### Community 3 - "Database Models & Schemas"
Cohesion: 0.39
Nodes (8): cancel(), _createDescriptors(), _descriptors(), _notify(), _notifyStateChanges(), removeBox(), stop(), tick()

### Community 4 - "UI Design & Styles"
Cohesion: 0.67
Nodes (3): Data-Dense Dashboard Style, Real-Time / Operations Landing Pattern, Dashboard Design Specifications (UTF-8)

### Community 5 - "Device Cryptography & Key Management"
Cohesion: 0.21
Nodes (14): addElements(), ba(), beforeUpdate(), buildOrUpdateElements(), configure(), _dataCheck(), datasetScopeKeys(), getDataset() (+6 more)

### Community 6 - "V2 Cryptography & Key Management"
Cohesion: 0.38
Nodes (7): bo(), Do(), getPadding(), ko(), qo(), wo(), yo()

### Community 7 - "Project Architecture & Structure"
Cohesion: 0.15
Nodes (25): beforeLayout(), bl(), cl(), dl(), el(), first(), fl(), interpolate() (+17 more)

### Community 8 - "Database Check Scripts"
Cohesion: 0.17
Nodes (12): afterAutoSkip(), buildLookupTable(), cd(), getDecimalForPixel(), getDecimalForValue(), getValueForPixel(), hp(), initOffsets() (+4 more)

### Community 9 - "Site Database Comparison"
Cohesion: 0.17
Nodes (17): afterDatasetsUpdate(), getDatasetMeta(), getMaxBorderWidth(), _getRotationExtents(), getStyle(), gl(), hide(), isDatasetVisible() (+9 more)

### Community 10 - "Leaflet CSS Comparison"
Cohesion: 0.14
Nodes (22): cr(), easeInOutElastic(), Ed(), en(), Fn(), Gn(), Hn(), In() (+14 more)

### Community 11 - "Full Database Validation"
Cohesion: 0.16
Nodes (17): datasetElementScopeKeys(), getDatasetMeta(), getMaxBorderWidth(), _getRotation(), _getRotationExtents(), getStyle(), hide(), isDatasetVisible() (+9 more)

### Community 12 - "Directory Structure Comparison"
Cohesion: 0.13
Nodes (17): aa(), Ao(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), _drawDataset(), _drawDatasets(), generateLabels() (+9 more)

### Community 13 - "Site Exporter Scripts"
Cohesion: 0.13
Nodes (16): bs(), color(), darken(), dr(), er(), fr(), hexString(), hr() (+8 more)

### Community 14 - "Server UI Logging"
Cohesion: 0.20
Nodes (14): ac(), acquireContext(), chartOptionScopes(), constructor(), fa(), Fo(), getContext(), getMeta() (+6 more)

### Community 15 - "Server Authentication & Security"
Cohesion: 0.13
Nodes (15): color(), _computeLabelArea(), darken(), dr(), drawLabels(), fr(), getLabelItems(), hexString() (+7 more)

### Community 16 - "Frontend Static File Serving"
Cohesion: 0.22
Nodes (11): aa(), afterDraw(), _drawDataset(), _drawDatasets(), notifyPlugins(), oa(), sa(), _updateDataset() (+3 more)

### Community 17 - "V2 Server Authentication"
Cohesion: 0.14
Nodes (17): alpha(), Ct(), ep(), et(), greyscale(), hslString(), ht(), interpolate() (+9 more)

### Community 18 - "V2 Frontend File Serving"
Cohesion: 0.24
Nodes (10): afterTickToLabelConversion(), beforeTickToLabelConversion(), _convertTicksToLabels(), format(), generateTickLabels(), getLabelAndValue(), getLabelForValue(), lr() (+2 more)

### Community 19 - "Server Compare Script"
Cohesion: 0.20
Nodes (18): Ao(), at(), b(), bf(), bs(), _computeLabelSizes(), hc(), ho() (+10 more)

### Community 20 - "SVG Search Script"
Cohesion: 0.33
Nodes (7): active(), _animateOptions(), _createAnimations(), da(), ma(), pa(), wait()

### Community 21 - "JS Code Search Script"
Cohesion: 0.40
Nodes (5): afterTickToLabelConversion(), beforeTickToLabelConversion(), _convertTicksToLabels(), generateTickLabels(), _tickFormatFunction()

### Community 22 - "JS Category Search Script"
Cohesion: 0.08
Nodes (65): a(), alpha(), apply(), bi(), bt(), ca(), ce(), dc() (+57 more)

### Community 23 - "JS Selector Search Script"
Cohesion: 0.22
Nodes (9): datasetAnimationScopeKeys(), _removeDatasetHoverStyle(), removeHoverStyle(), _resolveAnimations(), _setDatasetHoverStyle(), setHoverStyle(), _setStyle(), _updateAnimationTarget() (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (8): addControllers(), addPlugins(), addScales(), _each(), removeControllers(), _removeElements(), removePlugins(), removeScales()

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (5): _removeDatasetHoverStyle(), removeHoverStyle(), _setDatasetHoverStyle(), setHoverStyle(), _setStyle()

### Community 28 - "Community 28"
Cohesion: 0.08
Nodes (39): addBox(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), beforeLayout(), bl(), cl(), dl() (+31 more)

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (26): addElements(), afterDatasetsUpdate(), ba(), beforeUpdate(), buildOrUpdateElements(), _dataCheck(), formats(), getDataset() (+18 more)

### Community 30 - "Community 30"
Cohesion: 0.22
Nodes (9): addControllers(), addPlugins(), addScales(), _each(), remove(), removeControllers(), removePlugins(), removeScales() (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.18
Nodes (12): buildOrUpdateControllers(), _checkEventBindings(), clear(), clearCache(), _destroy(), _destroyDatasetMeta(), getController(), releaseContext() (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (8): cn(), _eventHandler(), _getLegendItemAt(), _handleEvent(), _positionChanged(), setActiveElements(), updateHoverStyle(), _updateHoverStyles()

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (12): afterAutoSkip(), buildLookupTable(), cd(), getDecimalForPixel(), getDecimalForValue(), getValueForPixel(), hp(), initOffsets() (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.29
Nodes (8): addBox(), getDevicePixelRatio(), getMaximumSize(), _refresh(), render(), resize(), running(), start()

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (7): cn(), _getLegendItemAt(), _handleEvent(), _positionChanged(), setActiveElements(), updateHoverStyle(), _updateHoverStyles()

### Community 36 - "Community 36"
Cohesion: 0.33
Nodes (6): ar(), describe(), gr(), Mr(), pr(), route()

### Community 37 - "Community 37"
Cohesion: 0.43
Nodes (7): _calculateBarIndexPixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), _getStackCount(), _getStackIndex(), _getStacks()

### Community 38 - "Community 38"
Cohesion: 0.33
Nodes (6): _onDataPop(), _onDataPush(), _onDataShift(), _onDataSplice(), _onDataUnshift(), _sync()

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (7): active(), _animateOptions(), _createAnimations(), da(), ma(), pa(), wait()

### Community 40 - "Community 40"
Cohesion: 0.09
Nodes (31): ac(), chartOptionScopes(), constructor(), determineDataLimits(), ea(), endOf(), fa(), getAllParsedValues() (+23 more)

### Community 41 - "Community 41"
Cohesion: 0.08
Nodes (33): acquireContext(), as(), bo(), Do(), ds(), Fo(), g(), getPadding() (+25 more)

### Community 42 - "Community 42"
Cohesion: 0.50
Nodes (4): bindEvents(), bindResponsiveEvents(), bindUserEvents(), isAttached()

### Community 43 - "Community 43"
Cohesion: 0.40
Nodes (6): er(), Ft(), hr(), Pt(), rgb(), zs()

### Community 44 - "Community 44"
Cohesion: 0.40
Nodes (5): ar(), describe(), Mr(), pr(), route()

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (3): buildOrUpdateScales(), ensureScalesHaveIDs(), _updateScales()

### Community 46 - "Community 46"
Cohesion: 0.18
Nodes (13): as(), _cachedScopes(), createResolver(), datasetAnimationScopeKeys(), datasetElementScopeKeys(), getOptionScopes(), pluginScopeKeys(), _resolveAnimations() (+5 more)

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (6): buildOrUpdateControllers(), _destroyDatasetMeta(), getController(), _removeUnreferencedMetasets(), updateIndex(), _updateMetasets()

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): _onDataPop(), _onDataPush(), _onDataShift(), _onDataSplice(), _onDataUnshift(), _sync()

### Community 50 - "Community 50"
Cohesion: 0.11
Nodes (24): buildTicks(), ca(), computeTickLimit(), determineDataLimits(), diff(), endOf(), _generate(), getAllParsedValues() (+16 more)

### Community 51 - "Community 51"
Cohesion: 0.28
Nodes (9): bd(), de(), fd(), Id(), kt(), Nd(), Ot(), Pn() (+1 more)

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (3): hd(), jd(), md()

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (10): bindEvents(), bindResponsiveEvents(), bindUserEvents(), _checkEventBindings(), clear(), clearCache(), _destroy(), isAttached() (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.67
Nodes (3): override(), register(), ws()

### Community 55 - "Community 55"
Cohesion: 0.33
Nodes (7): _eventHandler(), getDevicePixelRatio(), getMaximumSize(), isPointInArea(), render(), resize(), running()

### Community 56 - "Community 56"
Cohesion: 0.33
Nodes (7): getAfterBody(), getBeforeBody(), getFooter(), getTitle(), gs(), hs(), hu()

### Community 57 - "Community 57"
Cohesion: 0.40
Nodes (5): afterBuildTicks(), afterDataLimits(), beforeBuildTicks(), beforeDataLimits(), _callHooks()

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (3): override(), register(), ws()

### Community 105 - "Community 105"
Cohesion: 0.10
Nodes (29): cr(), cs(), easeInOutElastic(), Ed(), en(), _exec(), Fn(), Gn() (+21 more)

### Community 115 - "Community 115"
Cohesion: 0.03
Nodes (11): $(), afterDraw(), afterUpdate(), be(), buildLabels(), getActiveElements(), getElementsAtEventForMode(), _getRegistryForType() (+3 more)

### Community 174 - "Community 174"
Cohesion: 0.03
Nodes (12): $(), be(), buildOrUpdateScales(), ensureScalesHaveIDs(), _exec(), getActiveElements(), getElementsAtEventForMode(), _getRegistryForType() (+4 more)

### Community 178 - "Community 178"
Cohesion: 0.06
Nodes (71): add(), addEventListener(), ae(), af(), ai(), at(), b(), bc() (+63 more)

### Community 179 - "Community 179"
Cohesion: 0.06
Nodes (90): add(), af(), ai(), bc(), bi(), bt(), C(), cc() (+82 more)

### Community 180 - "Community 180"
Cohesion: 0.09
Nodes (32): afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterFit(), afterSetDimensions(), beforeBuildTicks(), beforeCalculateLabelRotation(), beforeDataLimits() (+24 more)

### Community 182 - "Community 182"
Cohesion: 0.10
Nodes (23): afterCalculateLabelRotation(), afterFit(), afterSetDimensions(), afterUpdate(), beforeCalculateLabelRotation(), beforeFit(), beforeSetDimensions(), buildLabels() (+15 more)

### Community 185 - "Community 185"
Cohesion: 0.14
Nodes (27): applyStack(), _calculateBarValuePixels(), calculateCircumference(), _circumference(), _computeAngle(), countVisibleElements(), format(), getBasePixel() (+19 more)

### Community 189 - "Community 189"
Cohesion: 0.07
Nodes (29): Accessibility, Available Domains, Available Stacks, Common Rules for Professional UI, Example Workflow, How to Use This Skill, Icons & Visual Elements, Interaction (+21 more)

### Community 190 - "Community 190"
Cohesion: 0.07
Nodes (67): ad(), ap(), Au(), bf(), bu(), buildTicks(), Co(), Cu() (+59 more)

### Community 191 - "Community 191"
Cohesion: 0.05
Nodes (71): adjustHitBoxes(), Al(), br(), calculateLabelRotation(), _calculatePadding(), ci(), _computeGridLineItems(), _computeLabelArea() (+63 more)

### Community 195 - "Community 195"
Cohesion: 0.07
Nodes (66): ad(), ap(), Au(), bu(), Co(), Cu(), dd(), dp() (+58 more)

### Community 196 - "Community 196"
Cohesion: 0.33
Nodes (9): cancel(), _createDescriptors(), _descriptors(), _notify(), _notifyStateChanges(), remove(), removeBox(), stop() (+1 more)

### Community 197 - "Community 197"
Cohesion: 0.06
Nodes (76): add_device(), add_label(), add_liaison(), add_main_courante(), add_or_update_site(), add_pylone(), add_stock_item(), advanced_search() (+68 more)

### Community 198 - "Community 198"
Cohesion: 0.06
Nodes (40): BM25, detect_domain(), _load_csv(), Lowercase, split, remove punctuation, filter short words, Build BM25 index from documents, Score all documents against query, Load CSV and return list of dicts, Core search function using BM25 (+32 more)

### Community 199 - "Community 199"
Cohesion: 0.15
Nodes (17): An(), average(), bn(), dataset(), getCenterPoint(), getProps(), hasValue(), inRange() (+9 more)

### Community 202 - "Community 202"
Cohesion: 0.24
Nodes (13): addEventListener(), cf(), Dt(), fp(), jo(), Lo(), Mo(), pd() (+5 more)

### Community 230 - "Community 230"
Cohesion: 0.06
Nodes (58): Al(), applyStack(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference(), _computeAngle() (+50 more)

### Community 231 - "Community 231"
Cohesion: 0.08
Nodes (44): adjustHitBoxes(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelItems(), _computeTitleHeight(), cs(), draw() (+36 more)

### Community 232 - "Community 232"
Cohesion: 0.67
Nodes (3): hd(), jd(), md()

### Community 233 - "Community 233"
Cohesion: 0.12
Nodes (27): Ct(), D(), E(), ee(), ep(), et(), Ft(), greyscale() (+19 more)

### Community 234 - "Community 234"
Cohesion: 0.50
Nodes (4): jp(), mp(), np(), Pp()

### Community 235 - "Community 235"
Cohesion: 0.08
Nodes (24): dependencies, clsx, framer-motion, lucide-react, next, react, react-dom, tailwind-merge (+16 more)

### Community 236 - "Community 236"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 238 - "Community 238"
Cohesion: 0.12
Nodes (16): aliases, components, hooks, lib, ui, utils, rsc, $schema (+8 more)

### Community 242 - "Community 242"
Cohesion: 0.13
Nodes (19): An(), average(), bn(), dataset(), getCenterPoint(), getProps(), getRange(), hasValue() (+11 more)

### Community 245 - "Community 245"
Cohesion: 0.15
Nodes (7): menus, viewIds, viewLabels, Window, menus, IMenu, MenuProps

### Community 246 - "Community 246"
Cohesion: 0.10
Nodes (20): Project Structure Flattening, 1. Retrait et Centrage des Cartes KPI du Tableau de bord, 1. Simplification de la Structure du Projet (Flattening), 1. Suppression Totale des Hashes (`#`) de l'URL, 2. Activation du Système de Mail avec les configurations Brevo SMTP, 2. Contrôleur de Navigation Unifié (`window.changeLegacyView`) dans l'IIFE de l'Iframe, 2. Résolution du Bug d'Accès à la Base de Données, 3. Automatisation et Consolidation des Notifications d'Échéance (+12 more)

### Community 260 - "Community 260"
Cohesion: 0.40
Nodes (4): DolphiSIC Redesign, Installation manuelle, Lancement complet, Structure

## Knowledge Gaps
- **117 isolated node(s):** `metadata`, `Window`, `menus`, `viewIds`, `viewLabels` (+112 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `$()` connect `Community 115` to `Database Models & Schemas`, `Project Architecture & Structure`, `Database Check Scripts`, `Full Database Validation`, `Directory Structure Comparison`, `Site Exporter Scripts`, `SVG Search Script`, `JS Code Search Script`, `JS Category Search Script`, `JS Selector Search Script`, `Community 29`, `Community 30`, `Community 31`, `Community 32`, `Community 34`, `Community 36`, `Community 37`, `Community 38`, `Community 40`, `Community 41`, `Community 42`, `Community 45`, `Community 178`, `Community 180`, `Community 54`, `Community 185`, `Community 190`, `Community 191`, `Community 232`, `Community 105`, `Community 233`, `Community 242`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 174` to `V2 Server API Endpoints`, `Server Site & Asset Operations`, `Device Cryptography & Key Management`, `V2 Cryptography & Key Management`, `Site Database Comparison`, `Leaflet CSS Comparison`, `Server UI Logging`, `Server Authentication & Security`, `Frontend Static File Serving`, `V2 Server Authentication`, `V2 Frontend File Serving`, `Server Compare Script`, `Community 26`, `Community 27`, `Community 28`, `Community 33`, `Community 35`, `Community 39`, `Community 43`, `Community 44`, `Community 46`, `Community 47`, `Community 49`, `Community 50`, `Community 179`, `Community 51`, `Community 53`, `Community 182`, `Community 55`, `Community 56`, `Community 57`, `Community 52`, `Community 59`, `Community 58`, `Community 195`, `Community 196`, `Community 199`, `Community 202`, `Community 230`, `Community 231`, `Community 234`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `it()` connect `Community 33` to `Community 51`, `Community 174`, `Community 195`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `BM25 ranking algorithm for text search`, `Lowercase, split, remove punctuation, filter short words`, `Build BM25 index from documents` to the rest of the system?**
  _145 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Core Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.05651176133103844 - nodes in this community are weakly interconnected._
- **Should `Leaflet CSS Comparison` be split into smaller, more focused modules?**
  _Cohesion score 0.13852813852813853 - nodes in this community are weakly interconnected._
- **Should `Directory Structure Comparison` be split into smaller, more focused modules?**
  _Cohesion score 0.1323529411764706 - nodes in this community are weakly interconnected._