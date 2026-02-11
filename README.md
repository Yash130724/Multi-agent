# StartupPulse

A multi-agent intelligence system that automatically collects, curates, and delivers a daily email digest tailored for AI startup founders. Five specialized agents scrape RSS feeds, academic repositories, government portals, funding platforms, and GitHub to surface what matters most — so you never miss a beat.

## What You Get

Every day, a single beautifully formatted email lands in your inbox with five color-coded sections:

| Section | Sources | What It Covers |
|---|---|---|
| **AI News** | OpenAI, Google AI, Anthropic, DeepMind, NVIDIA, Microsoft, MIT Tech Review, The Verge, TechCrunch, VentureBeat | Latest AI announcements and industry moves |
| **Research Papers** | arXiv (AI, ML, NLP, CV, Robotics), Hugging Face, Papers With Code | New papers with auto-detected conference tags |
| **Government Grants** | Startup India, MEITY, DST, MSME, BIRAC, T-Hub, WE-Hub, IIIT-H CIE | Active schemes and subsidies (India-focused) |
| **Startup Funding** | Y Combinator, Antler India, 100X.VC, Techstars, Indian Angel Network, Better Capital | Open applications, accelerator batches, funding rounds |
| **GitHub Trending** | GitHub Trending (daily + weekly) | Hot repositories with star counts and languages |

## Architecture

```
                  main.py (CLI)
                      |
        +-------------+-------------+
        |             |             |
    collect()    format_digest()  send_email()
        |             |             |
   +---------+   formatter.py   emailer.py
   | Agents  |
   +---------+
   |  news   |---> RSS (feedparser)
   | papers  |---> RSS (feedparser)
   | grants  |---> Web scraping (requests + BeautifulSoup)
   | funding |---> Web scraping (requests + BeautifulSoup)
   | github  |---> Web scraping (requests + BeautifulSoup)
   +---------+
        |
    storage.py ---> data/{agent}/items_YYYY-MM-DD.json
```

Each agent inherits from `BaseAgent` and implements its own `collect()` method. Agents run independently — a failure in one does not affect the others. Collected items are deduplicated by URL and stored as JSON files with automatic 7-day retention cleanup.

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/your-username/startup-pulse.git
cd startup-pulse
pip install -r requirements.txt
```

### 2. Configure email

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
RECIPIENT_EMAIL=recipient@example.com
```

> **Note:** You need a Gmail App Password, not your regular password. Enable 2FA on your Google account, then go to **Google Account > Security > App Passwords** and generate one for "Mail".

### 3. Run

```bash
# Collect from all agents and send the digest
python main.py --daily
```

## Usage

```bash
# Run all agents (collect only, no email)
python main.py --collect

# Run a single agent
python main.py --collect-agent news
python main.py --collect-agent papers
python main.py --collect-agent grants
python main.py --collect-agent funding
python main.py --collect-agent github

# Send digest from today's collected data
python main.py --send

# Full pipeline: collect everything, then send
python main.py --daily
```

## Agents in Detail

### NewsAgent
Pulls from 10 RSS feeds across two tiers. Tier 1 sources (company blogs like OpenAI, Anthropic, DeepMind) are prioritized at the top of the digest. Only articles from the last **24 hours** are included.

### PapersAgent
Monitors 8 academic feeds including 6 arXiv categories. Papers from the last **72 hours** are collected (wider window to catch weekend publications). Automatically detects and tags papers mentioning major conferences (NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, and 80+ others).

### GrantsAgent
Scrapes 11 government and institutional portals for active grants and schemes. Uses intelligent link filtering — strong indicator keywords (grant, scheme, subsidy, fund) surface relevant links while noise words (login, download, navigation) are filtered out. Expired listings are automatically excluded.

### FundingAgent
Scrapes 7 startup funding platforms for open applications and active programs. Targets accelerator batches, seed funding rounds, and investment opportunities. Capped at 8 items per source to keep the digest focused.

### GitHubAgent
Extracts trending repositories from GitHub's daily and weekly trending pages. Captures repo name, description, language, total stars, and stars gained in the period.

## Project Structure

```
StartupPulse/
├── startup_pulse/                  # Main Python package
│   ├── __init__.py
│   ├── agents/                     # Collection agents
│   │   ├── __init__.py             # Agent registry (ALL_AGENTS, COLLECTIBLE_AGENTS)
│   │   ├── base.py                 # BaseAgent ABC
│   │   ├── news.py                 # NewsAgent
│   │   ├── papers.py               # PapersAgent
│   │   ├── grants.py               # GrantsAgent
│   │   ├── funding.py              # FundingAgent
│   │   └── github.py               # GitHubAgent
│   ├── core/                       # Config + storage
│   │   ├── __init__.py             # Re-exports config & storage
│   │   ├── config.py               # All sources, feeds, keywords, email config
│   │   └── storage.py              # JSON file storage with dedup & cleanup
│   └── delivery/                   # Formatting + email sending
│       ├── __init__.py             # Re-exports formatter & emailer
│       ├── formatter.py            # HTML email template engine
│       └── emailer.py              # Gmail SMTP sender
├── data/                           # Auto-managed JSON storage
├── main.py                         # CLI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Configuration

All data sources, keywords, and settings are centralized in `startup_pulse/core/config.py`:

- **RSS feeds** — Add or remove news and paper feeds
- **Scraping sources** — Add URLs for grant/funding portals
- **Keywords** — 60+ AI keywords and 89 conference names for smart filtering
- **Retention** — Data files are auto-cleaned after 7 days (configurable)

## Scheduling (Optional)

For a true daily digest, set up a cron job or Task Scheduler:

**Linux/macOS (cron):**
```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/startup-pulse && python main.py --daily
```

**Windows (Task Scheduler):**
Create a basic task that runs `python main.py --daily` in the project directory at your preferred time.

## Requirements

- Python 3.8+
- Gmail account with 2FA and App Password
- Internet connection for RSS feeds and web scraping

## License

MIT
