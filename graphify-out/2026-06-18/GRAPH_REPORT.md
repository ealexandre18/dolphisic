# Graph Report - .  (2026-06-18)

## Corpus Check
- 19 files · ~13,142 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 130 nodes · 226 edges · 26 communities (18 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_V2 Server API Endpoints|V2 Server API Endpoints]]
- [[_COMMUNITY_Core Server API Endpoints|Core Server API Endpoints]]
- [[_COMMUNITY_Server Site & Asset Operations|Server Site & Asset Operations]]
- [[_COMMUNITY_Database Models & Schemas|Database Models & Schemas]]
- [[_COMMUNITY_UI Design & Styles|UI Design & Styles]]
- [[_COMMUNITY_Device Cryptography & Key Management|Device Cryptography & Key Management]]
- [[_COMMUNITY_V2 Cryptography & Key Management|V2 Cryptography & Key Management]]
- [[_COMMUNITY_Project Architecture & Structure|Project Architecture & Structure]]
- [[_COMMUNITY_Server UI Logging|Server UI Logging]]
- [[_COMMUNITY_Server Authentication & Security|Server Authentication & Security]]
- [[_COMMUNITY_Frontend Static File Serving|Frontend Static File Serving]]
- [[_COMMUNITY_V2 Server Authentication|V2 Server Authentication]]
- [[_COMMUNITY_V2 Frontend File Serving|V2 Frontend File Serving]]
- [[_COMMUNITY_V2 Design Documentation|V2 Design Documentation]]
- [[_COMMUNITY_V2 Data Model Documentation|V2 Data Model Documentation]]

## God Nodes (most connected - your core abstractions)
1. `query_db()` - 40 edges
2. `query_db()` - 39 edges
3. `log_logic()` - 22 edges
4. `sdis04 SQLite Database` - 6 edges
5. `Modèle Conceptuel de Données` - 5 edges
6. `login()` - 4 edges
7. `update_device_cryptage()` - 4 edges
8. `add_device()` - 4 edges
9. `carto_sdis04 SQLite Database` - 4 edges
10. `calculate_next_key_date()` - 3 edges

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

## Communities (26 total, 8 thin omitted)

### Community 0 - "V2 Server API Endpoints"
Cohesion: 0.10
Nodes (36): add_label(), add_liaison(), add_main_courante(), add_or_update_site(), add_pylone(), add_stock_item(), advanced_search(), create_loan() (+28 more)

### Community 1 - "Core Server API Endpoints"
Cohesion: 0.15
Nodes (22): add_main_courante(), add_stock_item(), advanced_search(), Colors, delete_label(), delete_liaison(), delete_main_courante(), download_document() (+14 more)

### Community 2 - "Server Site & Asset Operations"
Cohesion: 0.13
Nodes (15): add_label(), add_liaison(), add_or_update_site(), add_pylone(), create_loan(), delete_device(), delete_document(), delete_pylone() (+7 more)

### Community 3 - "Database Models & Schemas"
Cohesion: 0.20
Nodes (10): carto_sdis04 SQLite Database, EQUIPEMENT_PARC Entity, sdis04 SQLite Database, SITES Entity, STOCK Entity, Modèle Conceptuel de Données, get_carto_data(), get_centres() (+2 more)

### Community 4 - "UI Design & Styles"
Cohesion: 0.50
Nodes (3): Data-Dense Dashboard Style, Real-Time / Operations Landing Pattern, Dashboard Design Specifications (UTF-8)

### Community 5 - "Device Cryptography & Key Management"
Cohesion: 0.67
Nodes (3): add_device(), calculate_next_key_date(), update_device_cryptage()

### Community 6 - "V2 Cryptography & Key Management"
Cohesion: 0.67
Nodes (3): add_device(), calculate_next_key_date(), update_device_cryptage()

## Knowledge Gaps
- **9 isolated node(s):** `Colors`, `Dashboard Design Specifications`, `Modèle Conceptuel de Données (V2)`, `EQUIPEMENT_PARC Entity`, `STOCK Entity` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `sdis04 SQLite Database` connect `Database Models & Schemas` to `V2 Server API Endpoints`, `Core Server API Endpoints`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `carto_sdis04 SQLite Database` connect `Database Models & Schemas` to `V2 Server API Endpoints`, `Core Server API Endpoints`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `query_db()` connect `V2 Server API Endpoints` to `V2 Server Authentication`, `V2 Cryptography & Key Management`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `sdis04 SQLite Database` (e.g. with `server.py` and `get_centres()`) actually correct?**
  _`sdis04 SQLite Database` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Colors`, `Serve the compiled React frontend for any non-API route.`, `Serve the compiled React frontend for any non-API route.` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `V2 Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.09851551956815115 - nodes in this community are weakly interconnected._
- **Should `Core Server API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.14666666666666667 - nodes in this community are weakly interconnected._