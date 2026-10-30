# Developer scripts verification

Working-tree verification, 2026-10-29–30. Application behavior, dependency versions and migrations are unchanged. Changes add Bash setup/service/test commands, numbered developer instructions, and a byte-for-byte original README backup. Feature-delivery role guides, policies and templates are retained.

| Check | Actual result |
| --- | --- |
| `./scripts/setup.sh` twice | Existing `.env`, database credentials/data preserved; no migrations pending; Django checks passed |
| `./scripts/test.sh` | 171 server tests passed in 153.12 seconds; system, migration drift, Ruff lint/format passed |
| `./scripts/test.sh unit` after final guards | 13 unit tests passed, covering private configuration, reruns, invalid settings, suite locking, inherited signals and occupied/recently closed ports |
| `./scripts/test.sh browser` | 8 bundled-browser cases passed; 13 native cases intentionally skipped |
| `./scripts/test.sh native --collect-only` | Driver started/stopped; all 13 native tests collected. Full native journeys were not rerun |
| Combined development launcher | Healthy app/SMTP/UI startup; Ctrl-C and forced app exit stopped all three owned services; immediate restart succeeded; both database servers preserved |
| Test interruption | Ctrl-C stopped the real test scheduler, removed the disposable database and released the suite lock |
| Documentation and syntax | Bash 3.2 syntax, embedded Python syntax, local links/anchors and `git diff --check` passed; `README.template.md` matches the original tracked README exactly |

The full server run preceded the final port-guard test and interruption-cleanup adjustment; focused unit and real lifecycle checks verified those later changes. Current server collection includes the added port-guard test. Initial wrapper failures exposed inherited ignored SIGINT and TCP TIME_WAIT handling; both were corrected and their affected checks passed.

Real setup checks used the already configured checkout. Fresh secret generation and configuration guards were tested in isolated temporary checkouts; package installation and creation of a new real PostgreSQL cluster were not executed. Mail/revisit helper journeys were not rerun. Detailed smoke artifacts remain ignored under `.local/`.
