# Whiteout Survival Transfer Bot

A standalone, open-source Discord bot designed to automate and manage State Transfers for Whiteout Survival alliances.

This bot connects to the official game API to fetch player data (Power, Furnace, State, Alliance) and synchronizes it automatically with a Google Sheet Dashboard. 

## Features
- **Auto-Syncing**: Runs every 20 minutes to fetch the latest player data for everyone on your sheet.
- **Auto-Transfer Status**: If a player's state updates to your target state, their status is automatically changed to "Transferred".
- **Dynamic Dashboard**: Automatically formats your Google Sheet with a clean, color-coded dashboard tracking total invites, approved invites, and limits for each alliance.
- **Discord Integration**: Slash commands like `/sort_transfers` and `/sync_transfer_manager` allow admins to manage the sheet directly from Discord.

---

## 1. Prerequisites

Before running the bot, you will need to gather 3 things:
1. **A Discord Bot Token** (To run the bot)
2. **A Google Service Account `credentials.json` file** (To access Google Sheets)
3. **A blank Google Sheet URL** (Where the data will be stored)

### Getting a Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and give it a name.
3. Go to the **Bot** tab and click **Reset Token** to get your token. Copy it down.
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
5. Go to **OAuth2 -> URL Generator**, select `bot` and `applications.commands`, and give it Administrator permissions. Copy the generated URL and paste it in your browser to invite the bot to your server.

### Getting Google Sheets Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project.
3. Go to **APIs & Services -> Enabled APIs & Services** and enable the **Google Sheets API**.
4. Go to **IAM & Admin -> Service Accounts** and create a new Service Account.
5. Click on the Service Account you just created, go to the **Keys** tab, click **Add Key -> Create new key**, and select **JSON**.
6. A file will download. Rename this file to `credentials.json` and place it in the same folder as this bot.

### Creating the Google Sheet
1. Go to Google Sheets and create a completely Blank spreadsheet.
2. Click **Share** in the top right.
3. Open your `credentials.json` file and find the `client_email` address.
4. Add that email address as an **Editor** to your Google Sheet.
5. Copy the URL of your Google Sheet.

---

## 2. Setup

Now that you have your prerequisites, setting up the bot is incredibly easy!

1. Install Python 3.10+ and install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the interactive setup script:
   ```bash
   python setup.py
   ```
3. Follow the prompts on screen. You will be asked for:
   - Your Discord Bot Token
   - Your Discord User ID (so the bot can DM you sync logs)
   - Your Google Sheet URL
   - Your target state number
   - A list of your state's alliances and their transfer limits

The setup script will generate a `.env` file and a `config.json` file automatically.

---

## 3. Formatting the Google Sheet

Next, run the sheet setup tool. This will inject all the formulas, headers, dropdown validations, and color-coding rules into your blank Google Sheet!

```bash
python setup_sheet.py
```

Once this finishes, open your Google Sheet. You will see a beautiful dashboard on the right side!

### How the Sheet Works
- **ID**: Paste player IDs in column B. The bot will use these to fetch data.
- **Autofilled Columns**: The bot will automatically populate **Nickname**, **Power**, **Furnace**, **State**, and **Alliance**. Do not edit these manually.
- **Type of Invite**: Choose Ordinary or Special from the dropdown. This is used to track your state's Special Invite quota.
- **Invited By**: Choose the alliance that is taking this player.
- **Status**: The current status of the transfer. If you set it to "Invite Sent", and the bot detects the player has arrived in your state, it will automatically change to "Transferred"!

---

## 4. Running the Bot

Finally, boot up the bot!

```bash
python bot.py
```

The bot is now online! In Discord, you can use the following commands:
- `/sync_transfer_manager`: Forces an immediate data fetch from the game API to update all players.
- `/sort_transfers`: Sorts the entire sheet. It groups players by Alliance first (using the order you specified during setup), then sorts them by highest Furnace Level, then highest Power!
