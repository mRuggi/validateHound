# validateHound
Hacktoberfest 2025 project, validator + lightweight viewer of **rusthound-ce** and similar collectors output data.

Questo repository è il punto di partenza per uno strumento CLI che:
- carica gli output JSON/ZIP di RustHound-CE,
- esegue validazioni di schema e consistenza,
- fornisce un sommario e (in futuro) un viewer leggero.

## Quickstart

1. Crea e attiva un virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate    # linux/macOS
# .venv\Scripts\activate     # Windows (PowerShell)
```

2. Installa dipendenze:

```bash
pip install -r requirements.txt
```
