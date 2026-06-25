# Graph Report - PROJET SDIS  (2026-06-24)

## Corpus Check
- 33 files · ~172,740 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1982 nodes · 5925 edges · 106 communities (97 shown, 9 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.95)
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
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 174|Community 174]]
- [[_COMMUNITY_Community 178|Community 178]]
- [[_COMMUNITY_Community 179|Community 179]]
- [[_COMMUNITY_Community 180|Community 180]]
- [[_COMMUNITY_Community 182|Community 182]]
- [[_COMMUNITY_Community 185|Community 185]]
- [[_COMMUNITY_Community 190|Community 190]]
- [[_COMMUNITY_Community 195|Community 195]]
- [[_COMMUNITY_Community 196|Community 196]]
- [[_COMMUNITY_Community 197|Community 197]]
- [[_COMMUNITY_Community 199|Community 199]]
- [[_COMMUNITY_Community 230|Community 230]]
- [[_COMMUNITY_Community 231|Community 231]]
- [[_COMMUNITY_Community 235|Community 235]]
- [[_COMMUNITY_Community 236|Community 236]]
- [[_COMMUNITY_Community 238|Community 238]]
- [[_COMMUNITY_Community 245|Community 245]]
- [[_COMMUNITY_Community 246|Community 246]]
- [[_COMMUNITY_Community 260|Community 260]]
- [[_COMMUNITY_Community 261|Community 261]]
- [[_COMMUNITY_Community 268|Community 268]]
- [[_COMMUNITY_Community 269|Community 269]]

## God Nodes (most connected - your core abstractions)
1. `$()` - 750 edges
2. `$()` - 750 edges
3. `_update()` - 79 edges
4. `_update()` - 79 edges
5. `i()` - 65 edges
6. `i()` - 65 edges
7. `query_db()` - 54 edges
8. `query_db()` - 51 edges
9. `log_logic()` - 47 edges
10. `log_logic()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `get_centres()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_devices()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_stats()` --references--> `sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md
- `get_carto_data()` --references--> `carto_sdis04 SQLite Database`  [INFERRED]
  server.py → mcd.md

## Import Cycles
- None detected.

## Communities (106 total, 9 thin omitted)

### Community 0 - "V2 Server API Endpoints"
Cohesion: 0.19
Nodes (15): addElements(), beforeUpdate(), buildOrUpdateElements(), configure(), _dataCheck(), datasetScopeKeys(), getDataset(), getElement() (+7 more)

### Community 1 - "Core Server API Endpoints"
Cohesion: 0.05
Nodes (86): carto_sdis04 SQLite Database, EQUIPEMENT_PARC Entity, sdis04 SQLite Database, SITES Entity, STOCK Entity, 1. Diagramme Entité-Association (Mermaid ERD), 2. Description des Associations et Cardinalités, Base de données : `carto_sdis04.db` (+78 more)

### Community 2 - "Server Site & Asset Operations"
Cohesion: 0.12
Nodes (17): aa(), addBox(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), generateLabels(), _getSortedDatasetMetas(), getSortedVisibleDatasetMetas() (+9 more)

### Community 3 - "Database Models & Schemas"
Cohesion: 0.26
Nodes (12): ba(), dc(), ec(), ge(), le(), me(), nf(), path() (+4 more)

### Community 4 - "UI Design & Styles"
Cohesion: 0.67
Nodes (3): Data-Dense Dashboard Style, Real-Time / Operations Landing Pattern, Dashboard Design Specifications (UTF-8)

### Community 5 - "Device Cryptography & Key Management"
Cohesion: 0.22
Nodes (10): acquireContext(), chartOptionScopes(), constructor(), drawBorder(), Fo(), getContext(), getMeta(), Io() (+2 more)

### Community 6 - "V2 Cryptography & Key Management"
Cohesion: 0.25
Nodes (16): apply(), ca(), determineDataLimits(), getUserBounds(), handleTickRangeOptions(), i(), ji(), ks() (+8 more)

### Community 7 - "Project Architecture & Structure"
Cohesion: 0.09
Nodes (25): DesignSystemGenerator, _detect_page_type(), format_ascii_box(), format_markdown(), format_master_md(), format_page_override_md(), generate_design_system(), _generate_intelligent_overrides() (+17 more)

### Community 8 - "Database Check Scripts"
Cohesion: 0.09
Nodes (25): DesignSystemGenerator, _detect_page_type(), format_ascii_box(), format_markdown(), format_master_md(), format_page_override_md(), generate_design_system(), _generate_intelligent_overrides() (+17 more)

### Community 9 - "Site Database Comparison"
Cohesion: 0.18
Nodes (16): getDatasetMeta(), getMaxBorderWidth(), _getRotation(), _getRotationExtents(), getStyle(), hide(), isDatasetVisible(), labelColor() (+8 more)

### Community 10 - "Leaflet CSS Comparison"
Cohesion: 0.07
Nodes (29): Accessibility, Available Domains, Available Stacks, Common Rules for Professional UI, Example Workflow, How to Use This Skill, Icons & Visual Elements, Interaction (+21 more)

### Community 11 - "Full Database Validation"
Cohesion: 0.18
Nodes (17): afterDatasetsUpdate(), buildOrUpdateControllers(), _destroyDatasetMeta(), getController(), getDatasetMeta(), getMaxBorderWidth(), _getRotationExtents(), hide() (+9 more)

### Community 12 - "Directory Structure Comparison"
Cohesion: 0.10
Nodes (34): An(), average(), beforeLayout(), bl(), bn(), cl(), dl(), el() (+26 more)

### Community 13 - "Site Exporter Scripts"
Cohesion: 0.08
Nodes (34): bs(), Do(), ea(), er(), es(), gu(), hr(), Ia() (+26 more)

### Community 14 - "Server UI Logging"
Cohesion: 0.22
Nodes (18): ai(), bc(), bi(), C(), cc(), ci(), ei(), ii() (+10 more)

### Community 15 - "Server Authentication & Security"
Cohesion: 0.11
Nodes (21): color(), _computeLabelArea(), darken(), dr(), drawLabels(), er(), fr(), Ft() (+13 more)

### Community 16 - "Frontend Static File Serving"
Cohesion: 0.12
Nodes (25): cr(), cs(), easeInOutElastic(), Ed(), en(), Fn(), Gn(), Hn() (+17 more)

### Community 17 - "V2 Server Authentication"
Cohesion: 0.12
Nodes (31): a(), addEventListener(), bd(), br(), cf(), de(), fd(), ff() (+23 more)

### Community 18 - "V2 Frontend File Serving"
Cohesion: 0.07
Nodes (29): Accessibility, Available Domains, Available Stacks, Common Rules for Professional UI, Example Workflow, How to Use This Skill, Icons & Visual Elements, Interaction (+21 more)

### Community 19 - "Server Compare Script"
Cohesion: 0.16
Nodes (20): a(), addEventListener(), ae(), ba(), br(), cf(), _computeLabelSizes(), fp() (+12 more)

### Community 20 - "SVG Search Script"
Cohesion: 0.15
Nodes (15): BM25, detect_domain(), _load_csv(), Lowercase, split, remove punctuation, filter short words, Build BM25 index from documents, Score all documents against query, Load CSV and return list of dicts, Core search function using BM25 (+7 more)

### Community 21 - "JS Code Search Script"
Cohesion: 0.20
Nodes (14): An(), average(), bn(), getCenterPoint(), getProps(), hasValue(), inRange(), inXRange() (+6 more)

### Community 22 - "JS Category Search Script"
Cohesion: 0.45
Nodes (11): ce(), fc(), Fi(), he(), ic(), Ja(), pc(), Pi() (+3 more)

### Community 23 - "JS Selector Search Script"
Cohesion: 0.25
Nodes (8): getStyle(), labelColor(), labelPointStyle(), _removeDatasetHoverStyle(), removeHoverStyle(), _setDatasetHoverStyle(), setHoverStyle(), _setStyle()

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (8): addControllers(), addPlugins(), addScales(), _each(), removeControllers(), _removeElements(), removePlugins(), removeScales()

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (5): _removeDatasetHoverStyle(), removeHoverStyle(), _setDatasetHoverStyle(), setHoverStyle(), _setStyle()

### Community 28 - "Community 28"
Cohesion: 0.18
Nodes (17): Ao(), bf(), bs(), gc(), gr(), hc(), ho(), Id() (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.21
Nodes (13): bo(), Do(), getMinMax(), go(), ko(), Na(), Oo(), p() (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.25
Nodes (8): addControllers(), addPlugins(), addScales(), _each(), removeControllers(), _removeElements(), removePlugins(), removeScales()

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (13): addElements(), beforeUpdate(), buildOrUpdateElements(), configure(), _dataCheck(), datasetScopeKeys(), getDataset(), getElement() (+5 more)

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (8): cn(), _eventHandler(), _getLegendItemAt(), _handleEvent(), _positionChanged(), setActiveElements(), updateHoverStyle(), _updateHoverStyles()

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (9): afterAutoSkip(), buildLookupTable(), cd(), getDecimalForPixel(), getDecimalForValue(), getValueForPixel(), initOffsets(), Kd() (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.36
Nodes (13): ce(), fc(), Fi(), he(), ic(), Ja(), pc(), pf() (+5 more)

### Community 35 - "Community 35"
Cohesion: 0.29
Nodes (8): cn(), _eventHandler(), _getLegendItemAt(), _handleEvent(), _positionChanged(), setActiveElements(), updateHoverStyle(), _updateHoverStyles()

### Community 36 - "Community 36"
Cohesion: 0.17
Nodes (12): ar(), _computeLabelArea(), describe(), drawLabels(), getLabelItems(), jr(), li(), Mr() (+4 more)

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (15): BM25, detect_domain(), _load_csv(), Lowercase, split, remove punctuation, filter short words, Build BM25 index from documents, Score all documents against query, Load CSV and return list of dicts, Core search function using BM25 (+7 more)

### Community 38 - "Community 38"
Cohesion: 0.33
Nodes (6): _onDataPop(), _onDataPush(), _onDataShift(), _onDataSplice(), _onDataUnshift(), _sync()

### Community 39 - "Community 39"
Cohesion: 0.36
Nodes (13): dc(), ec(), ge(), Gi(), Ki(), me(), nc(), So() (+5 more)

### Community 40 - "Community 40"
Cohesion: 0.27
Nodes (11): ac(), b(), Dt(), eo(), fa(), Gf(), ka(), le() (+3 more)

### Community 41 - "Community 41"
Cohesion: 0.11
Nodes (25): alpha(), Ct(), D(), E(), ee(), ep(), et(), Ft() (+17 more)

### Community 42 - "Community 42"
Cohesion: 0.20
Nodes (11): alpha(), Ct(), ep(), et(), greyscale(), hslString(), Qe(), vr() (+3 more)

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (21): ac(), acquireContext(), ae(), chartOptionScopes(), constructor(), fa(), Fo(), getContext() (+13 more)

### Community 44 - "Community 44"
Cohesion: 0.27
Nodes (11): D(), E(), ee(), g(), ie(), m(), ne(), O() (+3 more)

### Community 45 - "Community 45"
Cohesion: 0.42
Nodes (9): ai(), bi(), ci(), ei(), ii(), oi(), ri(), si() (+1 more)

### Community 46 - "Community 46"
Cohesion: 0.22
Nodes (9): createResolver(), datasetAnimationScopeKeys(), datasetElementScopeKeys(), _resolveAnimations(), resolveDatasetElementOptions(), _resolveElementOptions(), resolveNamedOptions(), _updateAnimationTarget() (+1 more)

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (6): buildOrUpdateControllers(), _destroyDatasetMeta(), getController(), _removeUnreferencedMetasets(), updateIndex(), _updateMetasets()

### Community 48 - "Community 48"
Cohesion: 0.22
Nodes (8): hp(), it(), kt(), lp(), Ot(), remove(), rgbString(), unregister()

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): _onDataPop(), _onDataPush(), _onDataShift(), _onDataSplice(), _onDataUnshift(), _sync()

### Community 50 - "Community 50"
Cohesion: 0.07
Nodes (47): aa(), addBox(), adjustHitBoxes(), afterDraw(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), _computeTitleHeight() (+39 more)

### Community 51 - "Community 51"
Cohesion: 0.40
Nodes (5): afterDatasetsUpdate(), gl(), hl(), reset(), _resetElements()

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (6): bindEvents(), bindResponsiveEvents(), bindUserEvents(), _checkEventBindings(), isAttached(), unbindEvents()

### Community 53 - "Community 53"
Cohesion: 0.20
Nodes (10): bindEvents(), bindResponsiveEvents(), bindUserEvents(), _checkEventBindings(), clear(), clearCache(), _destroy(), isAttached() (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.40
Nodes (5): ar(), describe(), Mr(), pr(), route()

### Community 55 - "Community 55"
Cohesion: 0.12
Nodes (27): Ao(), b(), bf(), bo(), Dt(), eo(), g(), getPadding() (+19 more)

### Community 56 - "Community 56"
Cohesion: 0.33
Nodes (7): getAfterBody(), getBeforeBody(), getFooter(), getTitle(), gs(), hs(), hu()

### Community 57 - "Community 57"
Cohesion: 0.27
Nodes (15): apply(), fl(), hl(), i(), jc(), ks(), l(), ml() (+7 more)

### Community 58 - "Community 58"
Cohesion: 0.39
Nodes (8): cancel(), _createDescriptors(), _descriptors(), _notify(), _notifyStateChanges(), removeBox(), stop(), tick()

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (4): clear(), clearCache(), _destroy(), releaseContext()

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): buildOrUpdateScales(), ensureScalesHaveIDs(), _updateScales()

### Community 61 - "Community 61"
Cohesion: 0.20
Nodes (14): dataset(), getRange(), Id(), ji(), Ki(), Mi(), nc(), ni() (+6 more)

### Community 62 - "Community 62"
Cohesion: 0.67
Nodes (3): override(), register(), ws()

### Community 63 - "Community 63"
Cohesion: 0.06
Nodes (52): adjustHitBoxes(), afterDraw(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelItems(), _computeLabelSizes(), _computeTitleHeight() (+44 more)

### Community 64 - "Community 64"
Cohesion: 0.20
Nodes (15): bc(), C(), cc(), gc(), hc(), Hi(), oc(), sc() (+7 more)

### Community 65 - "Community 65"
Cohesion: 0.18
Nodes (13): as(), _cachedScopes(), createResolver(), datasetAnimationScopeKeys(), datasetElementScopeKeys(), getOptionScopes(), pluginScopeKeys(), _resolveAnimations() (+5 more)

### Community 66 - "Community 66"
Cohesion: 0.33
Nodes (7): active(), _animateOptions(), _createAnimations(), da(), ma(), pa(), wait()

### Community 69 - "Community 69"
Cohesion: 0.67
Nodes (3): hd(), jd(), md()

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (3): buildOrUpdateScales(), ensureScalesHaveIDs(), _updateScales()

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (3): afterTickToLabelConversion(), beforeTickToLabelConversion(), _convertTicksToLabels()

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (3): hd(), jd(), md()

### Community 77 - "Community 77"
Cohesion: 0.19
Nodes (14): _drawDataset(), _drawDatasets(), getDevicePixelRatio(), getMaximumSize(), gl(), notifyPlugins(), render(), reset() (+6 more)

### Community 78 - "Community 78"
Cohesion: 0.16
Nodes (18): ca(), determineDataLimits(), diff(), endOf(), _generate(), getAllParsedValues(), getDataTimestamps(), _getLabelBounds() (+10 more)

### Community 81 - "Community 81"
Cohesion: 0.24
Nodes (10): afterTickToLabelConversion(), beforeTickToLabelConversion(), _convertTicksToLabels(), format(), generateTickLabels(), getLabelAndValue(), getLabelForValue(), lr() (+2 more)

### Community 84 - "Community 84"
Cohesion: 0.18
Nodes (11): color(), darken(), dr(), fr(), hexString(), mix(), nr(), numeric() (+3 more)

### Community 105 - "Community 105"
Cohesion: 0.10
Nodes (28): cr(), cs(), easeInOutElastic(), Ed(), en(), _exec(), Fn(), Gn() (+20 more)

### Community 115 - "Community 115"
Cohesion: 0.03
Nodes (10): $(), be(), getActiveElements(), getElementsAtEventForMode(), _getRegistryForType(), isForType(), No(), se() (+2 more)

### Community 174 - "Community 174"
Cohesion: 0.03
Nodes (19): $(), be(), _exec(), getActiveElements(), getElementsAtEventForMode(), _getOtherScale(), getPadding(), _getRegistryForType() (+11 more)

### Community 178 - "Community 178"
Cohesion: 0.22
Nodes (22): add(), af(), bt(), df(), ef(), get(), _getAnims(), gr() (+14 more)

### Community 179 - "Community 179"
Cohesion: 0.09
Nodes (45): add(), af(), bd(), bt(), _cachedScopes(), de(), df(), diff() (+37 more)

### Community 180 - "Community 180"
Cohesion: 0.10
Nodes (28): afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterFit(), afterSetDimensions(), afterUpdate(), beforeBuildTicks(), beforeCalculateLabelRotation() (+20 more)

### Community 182 - "Community 182"
Cohesion: 0.11
Nodes (24): afterBuildTicks(), afterCalculateLabelRotation(), afterDataLimits(), afterFit(), afterSetDimensions(), afterUpdate(), beforeBuildTicks(), beforeCalculateLabelRotation() (+16 more)

### Community 185 - "Community 185"
Cohesion: 0.07
Nodes (54): Al(), applyStack(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference(), _computeAngle() (+46 more)

### Community 190 - "Community 190"
Cohesion: 0.07
Nodes (61): ad(), afterAutoSkip(), ap(), at(), Au(), bu(), buildLookupTable(), buildTicks() (+53 more)

### Community 195 - "Community 195"
Cohesion: 0.07
Nodes (69): ad(), ap(), as(), at(), Au(), bu(), Co(), Cu() (+61 more)

### Community 196 - "Community 196"
Cohesion: 0.17
Nodes (16): active(), _animateOptions(), cancel(), _createAnimations(), _createDescriptors(), da(), _descriptors(), ma() (+8 more)

### Community 197 - "Community 197"
Cohesion: 0.06
Nodes (82): add_device(), add_label(), add_liaison(), add_main_courante(), add_or_update_site(), add_pylone(), add_stock_item(), advanced_search() (+74 more)

### Community 199 - "Community 199"
Cohesion: 0.08
Nodes (44): Al(), beforeLayout(), bl(), cl(), dl(), drawBackground(), drawCaret(), ea() (+36 more)

### Community 230 - "Community 230"
Cohesion: 0.07
Nodes (50): applyStack(), _calculateBarIndexPixels(), _calculateBarValuePixels(), calculateCircumference(), calculateTotal(), _circumference(), _computeAngle(), countVisibleElements() (+42 more)

### Community 231 - "Community 231"
Cohesion: 0.07
Nodes (43): buildTicks(), calculateLabelRotation(), _calculatePadding(), _computeGridLineItems(), _computeLabelItems(), computeTickLimit(), _drawArgs(), drawGrid() (+35 more)

### Community 235 - "Community 235"
Cohesion: 0.08
Nodes (24): dependencies, clsx, framer-motion, lucide-react, next, react, react-dom, tailwind-merge (+16 more)

### Community 236 - "Community 236"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 238 - "Community 238"
Cohesion: 0.12
Nodes (16): aliases, components, hooks, lib, ui, utils, rsc, $schema (+8 more)

### Community 245 - "Community 245"
Cohesion: 0.15
Nodes (7): menus, viewIds, viewLabels, Window, menus, IMenu, MenuProps

### Community 246 - "Community 246"
Cohesion: 0.06
Nodes (30): Project Structure Flattening, 1. Retrait et Centrage des Cartes KPI du Tableau de bord, 1. Résolution de l'Erreur de Sérialisation JSON, 1. Simplification de la Structure du Projet (Flattening), 1. Structure de la Base de Données Relationnelle, 1. Suppression Totale des Hashes (`#`) de l'URL, 2. Activation du Système de Mail avec les configurations Brevo SMTP, 2. API REST CRUD et Moteur Mis à Jour (+22 more)

### Community 260 - "Community 260"
Cohesion: 0.40
Nodes (4): DolphiSIC Redesign, Installation manuelle, Lancement complet, Structure

## Knowledge Gaps
- **148 isolated node(s):** `metadata`, `Window`, `menus`, `viewIds`, `viewLabels` (+143 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `$()` connect `Community 174` to `Device Cryptography & Key Management`, `V2 Cryptography & Key Management`, `Site Database Comparison`, `Server UI Logging`, `Server Authentication & Security`, `Frontend Static File Serving`, `Server Compare Script`, `JS Code Search Script`, `Community 26`, `Community 27`, `Community 28`, `Community 29`, `Community 31`, `Community 33`, `Community 34`, `Community 35`, `Community 39`, `Community 40`, `Community 42`, `Community 44`, `Community 46`, `Community 47`, `Community 48`, `Community 49`, `Community 50`, `Community 179`, `Community 51`, `Community 53`, `Community 182`, `Community 54`, `Community 56`, `Community 195`, `Community 196`, `Community 199`, `Community 71`, `Community 74`, `Community 75`, `Community 230`, `Community 231`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `$()` connect `Community 115` to `V2 Server API Endpoints`, `Server Site & Asset Operations`, `Database Models & Schemas`, `Full Database Validation`, `Directory Structure Comparison`, `Site Exporter Scripts`, `V2 Server Authentication`, `JS Category Search Script`, `JS Selector Search Script`, `Community 30`, `Community 32`, `Community 36`, `Community 38`, `Community 41`, `Community 43`, `Community 45`, `Community 178`, `Community 180`, `Community 52`, `Community 55`, `Community 185`, `Community 57`, `Community 58`, `Community 60`, `Community 59`, `Community 190`, `Community 63`, `Community 64`, `Community 65`, `Community 66`, `Community 61`, `Community 62`, `Community 69`, `Community 77`, `Community 78`, `Community 81`, `Community 84`, `Community 105`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `it()` connect `Community 190` to `V2 Server Authentication`, `Community 115`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `BM25 ranking algorithm for text search`, `Lowercase, split, remove punctuation, filter short words`, `Build BM25 index from documents` to the rest of the system?**
  _202 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Core Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.05318352059925094 - nodes in this community are weakly interconnected._
- **Should `Server Site & Asset Operations` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Project Architecture & Structure` be split into smaller, more focused modules?**
  _Cohesion score 0.0855614973262032 - nodes in this community are weakly interconnected._