# Whiteout Survival Transfer Bot

A standalone, open-source Discord bot designed to automate and manage State Transfers for Whiteout Survival alliances.

This bot connects to the official game API to fetch player data (Power, Furnace, State, Alliance) and synchronizes it automatically with a Google Sheet Dashboard. 

## Features
- **Auto-Syncing**: Runs every 20 minutes to fetch the latest player data for everyone on your sheet.
- **Auto-Transfer Status**: If a player's state updates to your target state, their status is automatically changed to "Transferred".
- **Dynamic Dashboard**: Automatically formats your Google Sheet with a clean, color-coded dashboard tracking total invites, approved invites, and limits for each alliance.
- **Discord Integration**: Slash commands like `/sort_transfers` and `/sync_transfer_manager` allow admins to manage the sheet directly from Discord.

---

## 1. Gather Your Keys (Takes 2 minutes)

You only need three things to get started:

**1. A Discord Bot Token**
* Go to the [Discord Developer Portal](https://discord.com/developers/applications) -> **New Application**.
* Go to the **Bot** tab -> Click **Reset Token** to get your password.
* *Important:* Scroll down and check the box for **Message Content Intent**.

**2. A Google credentials.json file**
* Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
* Search for **Google Sheets API** at the top and click **Enable**.
* Go to **IAM & Admin -> Service Accounts** and create one.
* Click on your new service account -> **Keys** tab -> **Add Key** -> **JSON**. 
* Put the downloaded file in the bot's folder and name it `credentials.json`.

**3. A blank Google Sheet**
* Create a blank Google Sheet.
* Open `credentials.json`, copy the `client_email` address, and **Share** your Google Sheet with that email as an Editor.
* Copy the link to your Google Sheet!

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
