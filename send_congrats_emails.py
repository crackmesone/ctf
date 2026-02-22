#!/usr/bin/env python3
"""
Send congratulatory emails to top 100 Crackmes.one CTF players.

Usage:
    # Send to ranks 1-50 (first batch)
    python send_congrats_emails.py --start 1 --end 50

    # Send to ranks 51-100 (second batch)
    python send_congrats_emails.py --start 51 --end 100

    # Dry run (preview without sending)
    python send_congrats_emails.py --start 1 --end 50 --dry-run

    # Send to a single player (for testing)
    python send_congrats_emails.py --start 1 --end 1 --dry-run
"""

import csv
import argparse
import os
import time

import resend

# Configuration
CSV_FILE = "Crackmesone CTF-scoreboard.csv"
FROM_EMAIL = "admin@mail.crackmes.one"
REPLY_TO = "crackmesone@gmail.com"
TOTAL_PARTICIPANTS = 2331
HALL_OF_FAME_URL = "https://ctf.crackmes.one/#hall-of-fame"

# Email templates
EMAIL_TEMPLATE_TOP20 = """\
Hey {username},

Congratulations on finishing #{rank} out of {total_participants} participants in Crackmes.one CTF — and solving every single challenge! That's a seriously impressive result.

Your name is now on the Hall of Fame — take a look: {hall_of_fame_url}

We genuinely enjoyed putting together these challenges, and it's rewarding to see players like you work through them. Whether you solved that one challenge that had been frustrating you for hours or powered through the entire set — we appreciate you being part of this.

If you're up for it, we'd love to see writeups of any challenges you found interesting. The CTF community thrives on shared knowledge, and your approach might help someone else learn something new. We're also giving away a Binary Ninja license and a WinRAR license for the best writeups — details here: https://blog.crackmes.one/2026/02/21/crackmes-one-ctf-2026-recap.html#best-writeup-prize

Feel free to share your achievement on social media too — you earned it.

Thanks for playing, and hope to see you at future events.

Xusheng
Crackmes.one
"""

EMAIL_TEMPLATE_TOP100 = """\
Hey {username},

Congratulations on finishing Top 100 out of {total_participants} participants in Crackmes.one CTF! That's a seriously impressive result.

Your name is now on the Hall of Fame — take a look: {hall_of_fame_url}

We genuinely enjoyed putting together these challenges, and it's rewarding to see players like you work through them. Whether you solved that one challenge that had been frustrating you for hours or powered through the entire set — we appreciate you being part of this.

If you're up for it, we'd love to see writeups of any challenges you found interesting. The CTF community thrives on shared knowledge, and your approach might help someone else learn something new. We're also giving away a Binary Ninja license and a WinRAR license for the best writeups — details here: https://blog.crackmes.one/2026/02/21/crackmes-one-ctf-2026-recap.html#best-writeup-prize

Feel free to share your achievement on social media too — you earned it.

Thanks for playing, and hope to see you at future events.

Xusheng
Crackmes.one
"""


def get_subject(rank: int) -> str:
    """Generate email subject based on rank."""
    if rank <= 20:
        return f"Congratulations on placing #{rank} in Crackmes.one CTF!"
    else:
        return "Congratulations on placing Top 100 in Crackmes.one CTF!"


def get_email_body(rank: int, username: str) -> str:
    """Generate email body based on rank."""
    if rank <= 20:
        return EMAIL_TEMPLATE_TOP20.format(
            username=username,
            rank=rank,
            total_participants=TOTAL_PARTICIPANTS,
            hall_of_fame_url=HALL_OF_FAME_URL,
        )
    else:
        return EMAIL_TEMPLATE_TOP100.format(
            username=username,
            total_participants=TOTAL_PARTICIPANTS,
            hall_of_fame_url=HALL_OF_FAME_URL,
        )


def load_scoreboard(csv_path: str) -> list[dict]:
    """Load the scoreboard CSV and return top 100 players."""
    players = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = int(row["place"])
            if rank <= 100:
                players.append({
                    "rank": rank,
                    "username": row["user name"],
                    "email": row["user email"],
                })
    return players


def send_email(player: dict, dry_run: bool = False) -> bool:
    """Send congratulatory email to a player. Returns True on success."""
    rank = player["rank"]
    username = player["username"]
    email = player["email"]

    subject = get_subject(rank)
    body = get_email_body(rank, username)

    if dry_run:
        print(f"\n{'='*60}")
        print(f"[DRY RUN] Would send to: {email}")
        print(f"Username: {username} | Rank: #{rank}")
        print(f"Subject: {subject}")
        print(f"{'='*60}")
        print(body)
        return True

    try:
        params: resend.Emails.SendParams = {
            "from": FROM_EMAIL,
            "to": [email],
            "reply_to": REPLY_TO,
            "subject": subject,
            "text": body,
        }
        response = resend.Emails.send(params)
        print(f"[OK] Sent to {username} ({email}) - Rank #{rank} - ID: {response['id']}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send to {username} ({email}): {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Send congratulatory emails to top 100 Crackmes.one CTF players."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Starting rank (inclusive), default: 1",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=100,
        help="Ending rank (inclusive), default: 100",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview emails without actually sending them",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Resend API key (or set RESEND_API_KEY env var)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between emails (default: 0.5)",
    )
    args = parser.parse_args()

    # Validate range
    if args.start < 1 or args.end > 100 or args.start > args.end:
        print("Error: Invalid range. Must be between 1 and 100, and start <= end.")
        return 1

    # Set up API key
    api_key = args.api_key or os.environ.get("RESEND_API_KEY")
    if not api_key and not args.dry_run:
        print("Error: Resend API key required. Set RESEND_API_KEY or use --api-key.")
        return 1

    if not args.dry_run:
        resend.api_key = api_key

    # Load players
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, CSV_FILE)
    players = load_scoreboard(csv_path)

    # Filter to requested range
    selected = [p for p in players if args.start <= p["rank"] <= args.end]

    print(f"Crackmes.one CTF - Congratulatory Email Sender")
    print(f"{'='*50}")
    print(f"Range: Rank #{args.start} to #{args.end}")
    print(f"Players to email: {len(selected)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'='*50}")

    if not args.dry_run:
        confirm = input(f"\nSend {len(selected)} emails? (yes/no): ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return 0

    # Send emails
    success = 0
    failed = 0
    for player in selected:
        if send_email(player, dry_run=args.dry_run):
            success += 1
        else:
            failed += 1
        if not args.dry_run and player != selected[-1]:
            time.sleep(args.delay)

    print(f"\n{'='*50}")
    print(f"Done! Sent: {success}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
