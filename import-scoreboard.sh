#!/bin/bash
# ============================================
# CTFd Scoreboard Import Script
# ============================================
# Usage: ./import-scoreboard.sh [CTFd_URL] [API_TOKEN]
#
# Option 1: Use API (requires admin token)
#   ./import-scoreboard.sh https://crackmesone.ctfd.io YOUR_API_TOKEN
#
# Option 2: Use exported JSON file
#   Copy the scoreboard JSON from CTFd admin panel and save as scoreboard.json
#
# CTFd Export: Admin Panel -> Config -> Backup -> Export Scoreboard
# ============================================

CTFD_URL="${1:-https://crackmesone.ctfd.io}"
API_TOKEN="$2"

if [ -z "$API_TOKEN" ]; then
    echo "============================================"
    echo "No API token provided."
    echo ""
    echo "Option 1: Provide API token as second argument"
    echo "  ./import-scoreboard.sh $CTFD_URL YOUR_TOKEN"
    echo ""
    echo "Option 2: Manual export from CTFd"
    echo "  1. Go to CTFd Admin -> Scoreboard"
    echo "  2. Use browser dev tools (F12) -> Network tab"
    echo "  3. Look for /api/v1/scoreboard request"
    echo "  4. Copy the JSON response"
    echo "  5. Save to scoreboard.json in this format:"
    echo ""
    echo '  {"standings": [{"name": "player", "score": 100}, ...]}'
    echo ""
    echo "Option 3: Use curl with cookies (if logged in)"
    echo "  curl '$CTFD_URL/api/v1/scoreboard' \\"
    echo "    -H 'Cookie: session=YOUR_SESSION_COOKIE' \\"
    echo "    | jq '.data' > scoreboard.json"
    echo "============================================"
    exit 1
fi

echo "Fetching scoreboard from $CTFD_URL..."

# Fetch scoreboard via API
curl -s "$CTFD_URL/api/v1/scoreboard" \
    -H "Authorization: Token $API_TOKEN" \
    -H "Content-Type: application/json" \
    | jq '{standings: [.data[] | {name: .name, score: .score}]}' > scoreboard.json

if [ $? -eq 0 ] && [ -s scoreboard.json ]; then
    PLAYER_COUNT=$(jq '.standings | length' scoreboard.json)
    echo "✓ Successfully imported $PLAYER_COUNT players to scoreboard.json"
    echo ""
    echo "Top 5:"
    jq -r '.standings[:5][] | "  \(.name): \(.score)"' scoreboard.json
    echo ""
    echo "Next steps:"
    echo "  1. Edit config.js and set isEventOver: true"
    echo "  2. git add . && git commit -m 'CTF ended - import final scoreboard'"
    echo "  3. git push"
else
    echo "✗ Failed to fetch scoreboard. Check your API token."
    exit 1
fi
