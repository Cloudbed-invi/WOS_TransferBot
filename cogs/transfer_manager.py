import discord
from discord.ext import commands, tasks
from discord import app_commands
import gspread
from google.oauth2.service_account import Credentials
import os
import asyncio
from cogs.login_handler import LoginHandler
import time
import logging
import json

logger = logging.getLogger(__name__)

class TransferManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.target_state = config.get('target_state', '3693')
        except FileNotFoundError:
            self.target_state = '3693'
            
        admin_id_str = os.getenv("ADMIN_ID")
        self.admin_id = int(admin_id_str) if admin_id_str and admin_id_str.isdigit() else None
            
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.sync_task.start()
        
    def cog_unload(self):
        self.sync_task.cancel()
        
    def _get_sheet_id(self):
        return os.getenv("SHEET_ID")

    @tasks.loop(minutes=20)
    async def sync_task(self):
        """Runs every 20 minutes to read the sheet and fetch new data."""
        sheet_id = self._get_sheet_id()
        if not sheet_id or not os.path.exists('credentials.json'):
            return
            
        try:
            # Doing the sync in an async loop to avoid blocking discord bot
            await self._run_sheet_sync(sheet_id)
        except Exception as e:
            logger.error(f"TransferManager sync_task error: {e}")
            
    @sync_task.before_loop
    async def before_sync(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="sync_transfer_manager", description="Force an immediate sync of the Transfer Manager Google Sheet")
    @app_commands.default_permissions(administrator=True)
    async def sync_transfer_manager_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        sheet_id = self._get_sheet_id()
        if not sheet_id:
            await interaction.followup.send("?? Transfer Sheet ID not found. Please run the setup script.")
            return

        try:
            await self._run_sheet_sync(sheet_id)
            await interaction.followup.send("? Successfully fetched live data and updated the Google Sheet!")
        except Exception as e:
            import traceback
            traceback.print_exc()
            await interaction.followup.send(f"?? Failed to synchronize: {str(e)}")

    @app_commands.command(name="sort_transfers", description="Sort sheet by Alliance > Furnace > Power")
    async def sort_transfers(self, interaction: discord.Interaction):
        await interaction.response.defer()
        sheet_id = self._get_sheet_id()
        if not sheet_id:
            await interaction.followup.send("?? Transfer Sheet ID not found.")
            return
        
        try:
            # Ensure worksheet is initialized
            if not self.worksheet:
                credentials = Credentials.from_service_account_file('credentials.json', scopes=self.scopes)
                gc = gspread.authorize(credentials)
                self.worksheet = gc.open_by_key(sheet_id).sheet1

            # We fetch columns B through N so we don't mess up the S.NO formulas in Col A
            rows = await asyncio.to_thread(self.worksheet.get, "B2:N1000")
            
            # Filter out completely blank rows
            valid_rows = [r for r in rows if len(r) > 0 and r[0].strip()]
            
            if not valid_rows:
                await interaction.followup.send("?? No data to sort!")
                return
            
            def parse_power(p_str):
                if not p_str: return 0
                import re
                m = re.match(r'^([\d\.]+)\s*([mMkK]?)$', p_str.strip())
                if m:
                    val = float(m.group(1))
                    mult = m.group(2).upper()
                    if mult == 'M': return int(val * 1000000)
                    if mult == 'K': return int(val * 1000)
                    return int(val)
                try: return int(p_str.replace(',', ''))
                except: return 0
                
            def parse_furnace(f_str):
                if not f_str: return 0
                f_str = f_str.strip().upper()
                if f_str.startswith('FC'):
                    try: return 1000 + int(f_str.replace('FC', '').strip())
                    except: return 0
                try: return int(f_str)
                except: return 0

            def sort_key(row):
                # row[0] is UID, row[2] is Power, row[3] is Furnace, row[9] is Invited By (Alliance)
                # Sort alphabetically by alliance, pushing empty alliances to the end (using "~" which is a high ASCII value)
                alliance = row[9].strip().upper() if len(row) > 9 and row[9].strip() else "~"
                    
                furnace_val = parse_furnace(row[3]) if len(row) > 3 else 0
                power_val = parse_power(row[2]) if len(row) > 2 else 0
                
                # We sort alliance alphabetically (A-Z), and furnace and power DESCENDING (-val)
                return (alliance, -furnace_val, -power_val)
                
            valid_rows.sort(key=sort_key)
            
            # Pad rows back to 13 columns if they are short
            for i, r in enumerate(valid_rows):
                if len(r) < 13:
                    valid_rows[i] = r + [""] * (13 - len(r))
                    
            # Clear existing data in B2:N
            await asyncio.to_thread(self.worksheet.batch_clear, ["B2:N1000"])
            
            # Write sorted data back
            await asyncio.to_thread(self.worksheet.update, values=valid_rows, range_name='B2:N', value_input_option='USER_ENTERED')
            
            await interaction.followup.send("? Successfully sorted the transfer sheet by Alliance > Furnace Level > Power!")
        except Exception as e:
            logger.error(f"Error sorting transfers: {e}")
            await interaction.followup.send(f"?? Failed to sort sheet: {e}")

    async def _run_sheet_sync(self, sheet_id: str):
        # Authenticate with Google
        credentials = Credentials.from_service_account_file('credentials.json', scopes=self.scopes)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(sheet_id)
        self.worksheet = spreadsheet.sheet1
        
        # Read the sheet using asyncio.to_thread since it's blocking
        all_values = await asyncio.to_thread(self.worksheet.get_all_values)
        if len(all_values) <= 1:
            return # Only headers
            
        # all_values[0] is headers. Rows start at index 1
        rows = all_values[1:]
        
        # We need to process rows. Let's separate them into Priority (no Name/Power) and Regular
        to_process = []
        for i, row in enumerate(rows):
            # UID is column 1 (B)
            if len(row) > 1 and row[1].strip():
                uid = row[1].strip()
                # Check if Name (C) or Power (D) is blank
                name = row[2].strip() if len(row) > 2 else ""
                power = row[3].strip() if len(row) > 3 else ""
                
                is_priority = not name or not power
                # i + 2 because rows list is 0-indexed and starts after row 1 header
                to_process.append({'uid': uid, 'row_idx': i + 2, 'priority': is_priority, 'current_data': row})
                
        # Sort by priority
        to_process.sort(key=lambda x: not x['priority'])
        
        # Notify Admin
        admin_user = None
        if self.admin_id:
            try:
                admin_user = await self.bot.fetch_user(self.admin_id)
                if admin_user:
                    try:
                        await admin_user.send(f"?? Transfer Manager sync started! Fetching data for {len(to_process)} UIDs...")
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Failed to fetch admin for DM: {e}")

        lh = LoginHandler()
        updates = []
        failed_count = 0
        success_count = 0
        api_results = {}
        
        for item in to_process:
            uid = item['uid']
            
            # Fetch data using the existing login handler
            result = await lh.fetch_player_data(str(uid), retry=True)
            
            while result['status'] == 'rate_limited':
                wait_time = result.get('wait_time') or getattr(lh, '_get_wait_time', lambda: 30.0)()
                wait_time = max(5.0, wait_time) # Enforce min 5 seconds
                logger.warning(f"TransferManager hit rate limit. Waiting {wait_time:.1f}s before retrying UID {uid}.")
                await asyncio.sleep(wait_time)
                result = await lh.fetch_player_data(str(uid), retry=True)
                
            if result['status'] == 'success' and result.get('data'):
                data = result['data']
                nickname = data.get('nickname', '')
                state = data.get('kid', '')
                
                furnace_img = str(data.get('stove_lv_content', ''))
                stove_lv_int = data.get('stove_lv', 0)
                try: stove_lv_int = int(stove_lv_int)
                except: stove_lv_int = 0
                
                import re
                m = re.search(r'stove_lv_(\d+)\.png', furnace_img)
                if m:
                    lv = int(m.group(1))
                    furnace = f"FC {lv}" if lv <= 10 else str(lv)
                else:
                    if stove_lv_int > 34:
                        fc_level = (stove_lv_int - 30) // 5
                        furnace = f"FC {fc_level}"
                    elif stove_lv_int > 30:
                        furnace = "30"
                    elif stove_lv_int > 0:
                        furnace = str(stove_lv_int)
                    else:
                        furnace = ""
                existing_power = item['current_data'][3].strip() if len(item['current_data']) > 3 else ''
                existing_alliance = item['current_data'][6].strip() if len(item['current_data']) > 6 else ''
                
                alliance = existing_alliance
                power = existing_power
                
                # Power fallback is no longer supported without sqlite DB.
                # User must manually type it.
                pass
                
                api_results[uid] = {
                    'nickname': str(nickname),
                    'power': power,
                    'furnace': str(furnace),
                    'state': str(state),
                    'alliance': str(alliance)
                }
            elif result['status'] == 'not_found':
                api_results[uid] = 'not_found'
                failed_count += 1
            else:
                failed_count += 1
                
            # Sleep a tiny bit to avoid hammering the API if we process many rows
            await asyncio.sleep(0.5)

        # Re-read the sheet right before writing to ensure we have the correct row indices 
        # in case the user sorted the sheet while we were fetching API data!
        fresh_values = await asyncio.to_thread(self.worksheet.get_all_values)
        updates = []
        for idx, row in enumerate(fresh_values[1:], start=2):
            if len(row) < 2 or not row[1].strip():
                continue
                
            uid = row[1].strip()
            if uid in api_results:
                res = api_results[uid]
                if res == 'not_found':
                    updates.append({
                        'range': f'C{idx}:G{idx}',
                        'values': [["No ID exist", "", "", "", ""]]
                    })
                else:
                    updates.append({
                        'range': f'C{idx}:G{idx}',
                        'values': [[res['nickname'], res['power'], res['furnace'], res['state'], res['alliance']]]
                    })
                    
                    # Auto-update status to Transferred if they arrive in target state
                    if str(res['state']) == str(self.target_state):
                        current_status = row[11].strip() if len(row) > 11 else ""
                        if current_status == "Invite Sent":
                            updates.append({
                                'range': f'L{idx}',
                                'values': [["Transferred"]]
                            })
                            
                    success_count += 1
            
        if updates:
            # Perform a batch update
            await asyncio.to_thread(self.worksheet.batch_update, updates, value_input_option='USER_ENTERED')
            if admin_user:
                try:
                    await admin_user.send(f"? Sync complete! Updated {success_count} rows. (Failed/Missing: {failed_count})")
                except Exception:
                    pass
        elif admin_user:
            try:
                await admin_user.send(f"? Sync complete! No new updates were necessary.")
            except Exception:
                pass


async def setup(bot):
    await bot.add_cog(TransferManager(bot))
