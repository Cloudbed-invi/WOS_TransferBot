# Whiteout Survival Transfer Bot

A standalone, open-source Discord bot designed to automate and manage State Transfers for Whiteout Survival alliances.

This bot connects to the official game API to fetch player data (Power, Furnace, State, Alliance) and synchronizes it automatically with a Google Sheet Dashboard. 

## What the Bot Does
*(Note: You can actually use the Google Sheet Template manually without this bot by typing in the Power/Furnace levels yourself! However, if you set up this bot, all of that manual data entry is automated for you.)*

- **Auto-Syncing**: Runs every 20 minutes to fetch the latest player data for everyone on your sheet.
- **Auto-Transfer Status**: If a player's state updates to your target state, their status is automatically changed to "Transferred".
- **Dynamic Dashboard**: Calculates total invites, approved invites, and alliance limits automatically on the spreadsheet.
- **Discord Integration**: Slash commands allow admins to sort and force-sync the sheet directly from Discord.

## Bot Commands
- `/sync_transfer_manager`: Forces an immediate data fetch from the game API to update all players. (Sends a DM to the bot owner with the log).
- `/sort_transfers`: Sorts the entire sheet. It groups players by Alliance first (using the order you specified during setup), then sorts them by highest Furnace Level, then highest Power!

---

## 1. Gather Your Keys (Takes 2 minutes)

You only need three things to get started:

**1. A Discord Bot Token**
* Go to the [Discord Developer Portal](https://discord.com/developers/applications) -> **New Application**.
* Go to the **Bot** tab -> Click **Reset Token** to get your password.
* *Important:* Scroll down and check the box for **Message Content Intent**.

**2. Your Discord User ID (Optional)**
* In Discord, go to **User Settings -> Advanced** and turn on **Developer Mode**.
* Right-click your own profile picture in any chat and select **Copy User ID**.
* *(This is a long number like `123456789012345678`. The bot uses this to DM you sync logs!)*

**3. A Google credentials.json file**
* Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project.
* Search for **Google Sheets API** at the top and click **Enable**.
* Go to **IAM & Admin -> Service Accounts** and create one.
* Click on your new service account -> **Keys** tab -> **Add Key** -> **JSON**. 
* Put the downloaded file in the bot's folder and name it `credentials.json`.

**4. The Google Sheet Template**
* Click this link: **[Transfer Sheet Template](https://docs.google.com/spreadsheets/d/1iD502n5EAqDNAtN_9PNtMpTkOxDann0Uf65n_1RGmPQ/edit?usp=sharing)**
* Go to **File -> Make a Copy** to save it to your own Google Drive.
* Open your `credentials.json`, copy the `client_email` address, and **Share** your copied Google Sheet with that email as an Editor.
* Copy the link to your new Google Sheet!

---

## 2. Setup

Now that you have your prerequisites, setting up the bot is incredibly easy!

1. Install Python 3.10+ from the Windows Store or Python.org.
2. Double-click the **`1_Install_and_Setup.bat`** file in the folder.
3. Follow the prompts on the black screen. It will ask for your Discord Token, Sheet URL, Target State, and Alliance Limits.

### How the Sheet Works
- **ID**: Paste player IDs in column B (Transfer Data tab). The bot will use these to fetch data.
- **Autofilled Columns**: The bot will automatically populate **Name**, **Power**, **Furnace**, **State**, and **Alliance**. Do not edit these manually.
- **Type of Invite**: Choose Ordinary or Special from the dropdown. This tracks your state's Special Invite quota.
- **Joining Alliance**: Choose the alliance that is taking this player.
- **Status**: The current status of the transfer. If you set it to "Invite Sent", and the bot detects the player has arrived in your state, it will automatically change to "Transferred"!

---

## 3. Running the Bot

To start the bot, just double-click **`2_Run_Bot.bat`**. 

> [!WARNING]
> **Keep the window open!** The black command prompt window that appears is the brain of your bot. If you close this window, the bot will go offline and stop syncing.

That's it! The bot is now online and monitoring your sheet.

## Important Notes on Discord DMs
If you provided your **Discord User ID** during setup to receive sync logs, please note:
1. You **must** invite the bot to a Discord Server that you are in.
2. You must ensure your privacy settings allow Direct Messages from server members. 
*(If you skip this, the bot won't be able to send you the error logs!)*
