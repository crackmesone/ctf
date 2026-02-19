# Crackmes.one RE CTF 2026

Static site for the 1st Crackmes.one Reverse Engineering CTF.

**Live site:** https://ctf.crackmes.one

## Switching Between Versions

The site has two modes controlled by `config.js`:

| Mode | `isEventOver` | Shows |
|------|---------------|-------|
| Live | `false` | "CTF is LIVE!" banner + Enter CTF button |
| Ended | `true` | "CTF has ended!" banner + Hall of Fame |

### Switch to "CTF Ended" mode

```bash
# 1. Download scoreboard CSV from CTFd admin panel
#    (Admin -> Scoreboard -> Export CSV)

# 2. Convert CSV to JSON (strips emails, keeps rank/name/score only)
python3 convert-scoreboard.py "Crackmesone CTF-scoreboard.csv"

# 3. Flip the switch
sed -i '' 's/isEventOver: false/isEventOver: true/' config.js

# 4. Deploy
git add .
git commit -m "CTF ended - final scoreboard"
git push
```

### Switch back to "Live" mode

```bash
sed -i '' 's/isEventOver: true/isEventOver: false/' config.js
git add config.js
git commit -m "Switch to live mode"
git push
```

## Files

| File | Purpose |
|------|---------|
| `config.js` | Toggle `isEventOver` to switch modes |
| `scoreboard.json` | Player rankings (generated from CSV) |
| `convert-scoreboard.py` | Convert CTFd CSV export to JSON |
| `index.html` | Main page |
| `style.css` | Styling (matches crackmes.one theme) |
| `app.js` | Logic to toggle UI and load scoreboard |

## Scoreboard

The Hall of Fame shows top 100 players by default with a "Show All Players" button to display everyone.

### Converting from CTFd Export

1. Go to CTFd Admin -> Scoreboard -> Export (CSV)
2. Run: `python3 convert-scoreboard.py "your-export.csv"`
3. This creates `scoreboard.json` with only rank, name, and score (no emails)

### JSON Format

```json
{
  "standings": [
    {"rank": 1, "name": "player1", "score": 1000},
    {"rank": 2, "name": "player2", "score": 950}
  ]
}
```

## Local Preview

```bash
python3 -m http.server 8080
# Open http://localhost:8080
# Hard refresh (Cmd+Shift+R) after changing config.js
```

## Privacy

- `.gitignore` excludes `*.csv` files to prevent committing emails
- Only `scoreboard.json` (rank, name, score) is committed
