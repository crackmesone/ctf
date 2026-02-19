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
# 1. Import the scoreboard (choose one method)

# Method A: With API token (get from CTFd admin)
./import-scoreboard.sh https://crackmesone.ctfd.io YOUR_API_TOKEN

# Method B: Manual - export from CTFd and save as scoreboard.json

# 2. Flip the switch
sed -i '' 's/isEventOver: false/isEventOver: true/' config.js

# 3. Deploy
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
| `scoreboard.json` | Player rankings (top 100 shown) |
| `import-scoreboard.sh` | Helper script to fetch scoreboard from CTFd |
| `index.html` | Main page |
| `style.css` | Styling (matches crackmes.one theme) |
| `app.js` | Logic to toggle UI and load scoreboard |

## Scoreboard Format

```json
{
  "standings": [
    {"name": "player1", "score": 1000},
    {"name": "player2", "score": 950}
  ]
}
```

## Local Preview

```bash
python3 -m http.server 8080
# Open http://localhost:8080
# Hard refresh (Cmd+Shift+R) after changing config.js
```
