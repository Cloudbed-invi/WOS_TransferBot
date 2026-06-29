import json
import os

def main():
    print("========================================")
    print("  WOS Transfer Bot - Initial Setup")
    print("========================================")
    
    print("\n[1] Discord & Google Sheets Setup")
    discord_token = input("Enter your Discord Bot Token: ").strip()
    admin_id = input("Enter your Discord User ID (for admin DMs): ").strip()
    sheet_id = input("Enter your Google Sheet ID (from the URL): ").strip()
    
    with open(".env", "w") as f:
        f.write(f"DISCORD_TOKEN={discord_token}\n")
        f.write(f"ADMIN_ID={admin_id}\n")
        f.write(f"SHEET_ID={sheet_id}\n")
    print("Saved to .env!")

    print("\n[2] Alliance Setup")
    target_state = input("Enter your State Number (e.g., 3693): ").strip()
    
    print("\nEnter your Alliances separated by commas (e.g., WAR, EVL, RAW).")
    print("Note: We recommend adding 'SELF REQ' at the end for individual applications.")
    alliances_input = input("Alliances: ").strip()
    alliances = [a.strip() for a in alliances_input.split(",") if a.strip()]
    
    limits = {}
    print("\nEnter the transfer limits for each alliance (type '-' for unlimited):")
    for alliance in alliances:
        limit = input(f"Limit for {alliance}: ").strip()
        if not limit:
            limit = "-"
        limits[alliance] = limit
        
    config = {
        "target_state": target_state,
        "alliances": alliances,
        "limits": limits
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    print("\nSaved to config.json!")
    print("\n========================================")
    print("Setup Complete! You can now run:")
    print("1. python setup_sheet.py (To build the Google Sheet layout)")
    print("2. python bot.py (To start the Discord bot)")
    print("========================================")

if __name__ == "__main__":
    main()
