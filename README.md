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

1. Install Python 3.10+ from the Windows Store or Python.org.
2. Double-click the **`1_Install_and_Setup.bat`** file in the folder.
3. Follow the prompts on the black screen. It will ask for your Discord Token, Sheet URL, Target State, and Alliance Limits.

Once you answer the questions, the setup script will instantly configure your Blank Google Sheet with all the colors, dropdowns, and dashboards!

### How the Sheet Works
- **ID**: Paste player IDs in column B. The bot will use these to fetch data.
- **Autofilled Columns**: The bot will automatically populate **Nickname**, **Power**, **Furnace**, **State**, and **Alliance**. Do not edit these manually.
- **Type of Invite**: Choose Ordinary or Special from the dropdown. This is used to track your state's Special Invite quota.
- **Invited By**: Choose the alliance that is taking this player.
- **Status**: The current status of the transfer. If you set it to "Invite Sent", and the bot detects the player has arrived in your state, it will automatically change to "Transferred"!

---

## 3. Running the Bot

To start the bot, just double-click **`2_Run_Bot.bat`**.

That's it! The bot is now online. In Discord, you can use:
- `/sync_transfer_manager`: Forces an immediate fetch to update all players.
- `/sort_transfers`: Sorts the entire sheet by Alliance -> Furnace -> Power.
