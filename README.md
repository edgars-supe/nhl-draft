# NHL Fantasy Draft

Live standings for an NHL fantasy draft, updated from real-time NHL data.

## Quick Start

```bash
uv run python main.py
```

Generates `index.html` and prints a table to the console.

## How It Works

The script:

1. Fetches current NHL standings from the NHL API
2. Loads your draft assignments from `draft.json`
3. Outputs a console table and an HTML page with team cards

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `standings.py` | Fetches & caches NHL standings |
| `models.py` | `Team` and `Drafter` data classes |
| `display.py` | Console table output |
| `html_output.py` | Generates `index.html` from template |
| `standings_template.html` | Jinja2 HTML template |
| `style.css` | Dark theme styles |
| `draft.json` | Your team assignments |

## Setup

```bash
uv sync
uv run python main.py
```

## Running

```bash
uv run python main.py
```

Open `index.html` in a browser.
