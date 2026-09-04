# VoteZenBot — Final Pre-Deployment Repository

VoteZenBot is a Pyrogram + MongoDB Telegram giveaway/voting bot.

## Locked behavior

- Main giveaway: channel entry cards, one active vote per voter, vote toggle, force membership check, hoster `/incr`, leaderboard, early/manual/automatic end.
- Mini giveaway: sequential participant numbers, live single-message entries list, random unique winners.
- A channel can have only one active VoteZenBot giveaway at a time.
- A hoster can save up to 5 channels.
- Main and mini setup supports optional start/end times. If no end time is supplied, the hoster must use `/end`.
- `/cancel` asks for confirmation; on confirmation it cancels even after participants have joined and removes stored entry posts where possible.
- `/incr` only increases displayed votes. Manual votes are stored separately from real voter identities.
- `/banp` removes the participant and their giveaway activity; `/unbanp` lets them rejoin as a fresh participant.
- Owner/SAdmin access mode can operate a giveaway as its hoster. Normal Admin cannot access a hoster's giveaway.
- Giveaway data export is available before cleanup. Heavy participant/voter data is removed after 4 days; a lightweight summary remains.
- Entry cards use participant PFP when available and a fixed fallback image otherwise.
- DM UI uses Unicode small caps. Channel headers use mathematical sans-serif bold italic.
- Health endpoint is included for Render.

## Environment

Copy `.env.example` to `.env`:

    API_ID=
    API_HASH=
    BOT_TOKEN=
    MONGO_URI=
    OWNER_ID=
    BOT_USERNAME=VoteZenBot
    FALLBACK_PFP_URL=

`FALLBACK_PFP_URL` should be a stable image URL. The bot also falls back to a text entry if Telegram cannot fetch the image.

## Run

    pip install -r requirements.txt
    python main.py

Docker:

    docker build -t votezenbot .
    docker run --env-file .env votezenbot

## Before public deployment

Run the integration checklist in `tests/INTEGRATION_CHECKLIST.md` with a real test channel and test accounts. Telegram permissions, membership events, image fetching and Render networking cannot be fully verified without real credentials.

## Guide PDFs / pages

`static/guide_user.pdf`, `static/guide_admin.pdf`, `static/guide_user.html`, and `static/guide_admin.html` are the bundled defaults sent by `/help` and served at `/guide` and `/guide/admin`. The owner can replace either PDF at any time with `/helppdf` — Telegram's copy then takes priority over the bundled file automatically. Both send paths are wrapped defensively, so a missing or corrupted file will never crash `/help`.
