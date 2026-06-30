import gspread
from google.oauth2.service_account import Credentials
import json
import os
from dotenv import load_dotenv

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    load_dotenv()
    sheet_identifier = os.getenv("SHEET_ID")
    
    if not sheet_identifier:
        print("Error: SHEET_ID not found in .env file.")
        print("Please run 'python setup.py' first.")
        return
        
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found.")
        print("Please run 'python setup.py' first.")
        return

    alliances = config.get("alliances", [])
    limits = config.get("limits", {})

    try:
        credentials = Credentials.from_service_account_file('credentials.json', scopes=scopes)
        gc = gspread.authorize(credentials)
        
        if "http" in sheet_identifier:
            sheet = gc.open_by_url(sheet_identifier)
        else:
            sheet = gc.open_by_key(sheet_identifier)

        worksheet = sheet.sheet1

        print("Writing headers...")
        headers = [
            "Note", "ID", "Power", "Furnace", "State", "Alliance", "Discord Username",
            "Role", "Type of Invite", "Invited By", "Status", "Comment"
        ]
        
        worksheet.update(values=[headers], range_name='B1:M1', value_input_option='USER_ENTERED')
        
        # Dashboard
        dashboard = [
            ["Ordinary Invites Used", '=COUNTIFS(J:J,"Ordinary", L:L, "<>Rejected", L:L, "<>Reviewing", L:L, "<>")', "", ""],
            ["Ordinary Invites Left", '=50-P1', "", ""],
            ["Special Invites Used", '=COUNTIFS(J:J,"Special", L:L, "<>Rejected", L:L, "<>Reviewing", L:L, "<>")', "", ""],
            ["Special Invites Left", '=30-P3', "", ""],
            ["Alliance", "Limit", "Requested", "Approved", "Left"]
        ]
        
        dashboard_row = 6
        for alliance in alliances:
            limit = limits.get(alliance, "-")
            req = f'=COUNTIF(K:K, "{alliance}")'
            app = f'=COUNTIFS(K:K, "{alliance}", L:L, "<>Rejected", L:L, "<>Reviewing", L:L, "<>")'
            left = f'=IF(Q{dashboard_row}="-", "-", Q{dashboard_row}-S{dashboard_row})'
            dashboard.append([alliance, limit, req, app, left])
            dashboard_row += 1
            
        dashboard_end = 5 + len(alliances)
        
        worksheet.update(values=dashboard, range_name=f'P1:T{dashboard_end}', value_input_option='USER_ENTERED')
        
        # Formatting
        worksheet.format("P1:P4", {"textFormat": {"bold": True}})
        worksheet.format("P5:T5", {"textFormat": {"bold": True}})
        
        # Clear existing validation if any, then apply new
        # State validation
        rule_state = {
            "condition": {
                "type": "NUMBER_GREATER",
                "values": [{"userEnteredValue": "0"}]
            },
            "showCustomUi": True
        }
        
        # Type of Invite validation
        rule_invite = {
            "condition": {
                "type": "ONE_OF_LIST",
                "values": [{"userEnteredValue": "Ordinary"}, {"userEnteredValue": "Special"}]
            },
            "showCustomUi": True
        }
        
        # Invited By validation (dynamic based on alliances)
        rule_invited_by = {
            "condition": {
                "type": "ONE_OF_LIST",
                "values": [{"userEnteredValue": a} for a in alliances]
            },
            "showCustomUi": True
        }
        
        # Status validation
        rule_status = {
            "condition": {
                "type": "ONE_OF_LIST",
                "values": [
                    {"userEnteredValue": "Reviewing"},
                    {"userEnteredValue": "Invite Sent"},
                    {"userEnteredValue": "Transferred"},
                    {"userEnteredValue": "Rejected"}
                ]
            },
            "showCustomUi": True
        }
        
        requests = [
            {
                "setDataValidation": {
                    "range": {"sheetId": worksheet.id, "startRowIndex": 1, "startColumnIndex": 5, "endColumnIndex": 6},
                    "rule": rule_state
                }
            },
            {
                "setDataValidation": {
                    "range": {"sheetId": worksheet.id, "startRowIndex": 1, "startColumnIndex": 9, "endColumnIndex": 10},
                    "rule": rule_invite
                }
            },
            {
                "setDataValidation": {
                    "range": {"sheetId": worksheet.id, "startRowIndex": 1, "startColumnIndex": 10, "endColumnIndex": 11},
                    "rule": rule_invited_by
                }
            },
            {
                "setDataValidation": {
                    "range": {"sheetId": worksheet.id, "startRowIndex": 1, "startColumnIndex": 11, "endColumnIndex": 12},
                    "rule": rule_status
                }
            }
        ]

        # Colors for alliances - cycle through some preset pastel colors
        preset_colors = [
            {"red": 1.0, "green": 0.8, "blue": 0.8}, # Light Red
            {"red": 0.9, "green": 0.8, "blue": 0.95}, # Light Purple
            {"red": 0.8, "green": 0.9, "blue": 1.0}, # Light Blue
            {"red": 0.8, "green": 1.0, "blue": 0.8}, # Light Green
            {"red": 1.0, "green": 0.9, "blue": 0.8}, # Light Orange
            {"red": 1.0, "green": 1.0, "blue": 0.8}, # Light Yellow
            {"red": 0.8, "green": 0.95, "blue": 0.95}, # Light Cyan
            {"red": 0.95, "green": 0.85, "blue": 0.75}, # Light Brown
        ]
        
        for idx, alliance in enumerate(alliances):
            if alliance.upper() == "SELF REQ":
                color = {"red": 0.9, "green": 0.9, "blue": 0.9} # Light Grey
            else:
                color = preset_colors[idx % len(preset_colors)]
                
            requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{"sheetId": worksheet.id, "startRowIndex": 1, "startColumnIndex": 1, "endColumnIndex": 13}],
                        "booleanRule": {
                            "condition": {
                                "type": "CUSTOM_FORMULA",
                                "values": [{"userEnteredValue": f'=$K2="{alliance}"'}]
                            },
                            "format": {"backgroundColor": color}
                        }
                    },
                    "index": 0
                }
            })
            
        sheet.batch_update({"requests": requests})
        print("Successfully built the spreadsheet layout!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
