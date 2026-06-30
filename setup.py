import json
import os

def main():
    print("========================================")
    print("  WOS Transfer Bot - Initial Setup")
    print("========================================")
    
    while not os.path.exists("credentials.json"):
        print("\n[!] ERROR: credentials.json not found in this folder!")
        print("Please download your Google Service Account key, rename it to 'credentials.json', and place it in this folder.")
        input("Press Enter once you have placed the file in the folder...")
    
    print("\n[1] Discord Setup")
    discord_token = input("Enter your Discord Bot Token: ").strip()
    admin_id = input("Enter your Discord User ID (for admin DMs): ").strip()
    sheet_id = input("Enter your Google Sheet ID (from the URL): ").strip()
    
    with open(".env", "w") as f:
        f.write(f"DISCORD_TOKEN={discord_token}\n")
        f.write(f"ADMIN_ID={admin_id}\n")
        f.write(f"SHEET_ID={sheet_id}\n")
    print("Saved to .env!")

    print("\n[2] Target State")
    target_state = input("Enter your Target State number (e.g. 3693): ").strip()
    
    # Extract ID if URL was provided
    if "spreadsheets/d/" in sheet_id:
        sheet_id = sheet_id.split("spreadsheets/d/")[1].split("/")[0]

    config = {
        "target_state": target_state
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    print("\nSaved to config.json!")
    print("\n========================================")
    print("Setup Complete! You can now double-click:")
    print("2_Run_Bot.bat (To start the Discord bot)")
    print("========================================")

if __name__ == "__main__":
    main()
