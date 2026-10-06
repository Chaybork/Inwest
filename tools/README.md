# Hilfsskripte

## mcp_client.py – direkter Zugriff auf die Plugin-MCP-Server

Falls die Session die Plugin-Server (Bio Research, Exa) beim Start nicht verbinden konnte,
lassen sie sich mit diesem Skript direkt per JSON-RPC über HTTPS ansprechen.
Voraussetzung: Die Hosts sind in der Netzwerkfreigabe der Umgebung erlaubt.

```
python3 -I tools/mcp_client.py <server-url> tools/list
python3 -I tools/mcp_client.py <server-url> tools/call '{"name":"<tool>","arguments":{...}}'
```

| Server | URL | Auth | Werkzeuge |
|---|---|---|---|
| PubMed | https://pubmed.mcp.claude.com/mcp | keine | search_articles, get_article_metadata, find_related_articles, lookup_article_by_citation, convert_article_ids, get_full_text_article, get_copyright_status |
| bioRxiv/medRxiv | https://hcls.mcp.claude.com/biorxiv/mcp | keine | search_preprints, get_preprint, … |
| ClinicalTrials | https://hcls.mcp.claude.com/clinical_trials/mcp | keine | search_trials, get_trial_details, … |
| ChEMBL | https://hcls.mcp.claude.com/chembl/mcp | keine | compound_search, drug_search, … |
| Exa | https://mcp.exa.ai/mcp | anonym (ratenbegrenzt) oder API-Key | web_search_exa, web_fetch_exa (holt Seiten serverseitig, auch solche, die die Umgebung selbst sperrt; Argument `urls` ist eine Liste) |
| Consensus | https://mcp.consensus.app/mcp | OAuth nötig (401 ohne Anmeldung) | search |
| Wiley | https://connector.scholargateway.ai/mcp | OAuth nötig (401 ohne Anmeldung) | – |

Beispiele:

```
python3 -I tools/mcp_client.py https://pubmed.mcp.claude.com/mcp tools/call \
  '{"name":"search_articles","arguments":{"query":"gambling disorder comorbidity meta-analysis","max_results":5}}'

python3 -I tools/mcp_client.py https://mcp.exa.ai/mcp tools/call \
  '{"name":"web_fetch_exa","arguments":{"urls":["https://www.nice.org.uk/guidance/ng248/chapter/Recommendations"],"maxCharacters":8000}}'
```
