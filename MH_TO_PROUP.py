from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl import functions
import time
import os
import asyncio
import random  # បន្ថែមសម្រាប់ពន្យារពេលចៃដន្យ

api_id = 23877053 
api_hash = '989c360358b981dae46a910693ab2f4c' 

def print_colored(text, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'white': '\033[97m',  # បន្ថែមពណ៌ white
        'reset': '\033[0m'
    }
    print(f"{colors[color]}{text}{colors['reset']}")


def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = r"""
███╗   ███╗██╗  ██╗    ████████╗ ██████╗     ██████╗ ██████╗  ██████╗ ██╗   ██╗██████╗ 
████╗ ████║██║  ██║    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔══██╗
██╔████╔██║███████║       ██║   ██║   ██║    ██████╔╝██████╔╝██║   ██║██║   ██║██████╔╝
██║╚██╔╝██║██╔══██║       ██║   ██║   ██║    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔═══╝ 
██║ ╚═╝ ██║██║  ██║       ██║   ╚██████╔╝    ██║     ██║  ██║╚██████╔╝╚██████╔╝██║     
╚═╝     ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     
"""
    print_colored(banner, 'cyan')
    print_colored("                           TOOL MADE BY @mengheang25", 'green')
    print()
    print_colored("=" * 60, 'yellow')
    print_colored("Telegram Member Transfer Tool MH TO PROUP", 'magenta')
    print()
    print_colored("Purpose:", 'cyan')
    print_colored("• Scrape members from one Telegram group", 'white')
    print_colored("• Automatically add them to another group", 'white')
    print()
    print_colored("Key Features:", 'cyan')
    print_colored("• Login via phone number + OTP", 'white')
    print_colored("• Random delay (10-30 seconds)", 'white')
    print_colored("• Skip bots and deleted accounts", 'white')
    print()
    print_colored("Warning:", 'red')
    print_colored("• Use only on groups you have permission for", 'white')
    print_colored("• Use sufficient delay to avoid account ban", 'white')
    print_colored("=" * 60, 'yellow')
    print()

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    print_banner()

    group_to_scrape = input("Enter the username of the group to scrape members from (without @): ")
    group_to_add = input("Enter the username of the group to add members to (without @): ")

    if not await client.is_user_authorized():
        # បង្ហាញព័ត៌មានជំនួយ
        print_colored("\n📱 IMPORTANT: Phone number must include country code!", 'yellow')
        print("Examples:")
        print("  Cambodia: +855101034566 (from 0101034566)")
        print("  Thailand: +66812345678  (from 0812345678)")
        print("  Vietnam:  +84912345678  (from 0912345678)")
        print("  USA:      +12345678900")
        print()
        
        phone_number = input("Enter your phone number (with +): ").strip()
        
        # ធានាថាមានសញ្ញា +
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            print_colored(f"Auto-corrected to: {phone_number}", 'cyan')
        
        print_colored("Sending code request...", 'cyan')
        
        try:
            await client.send_code_request(phone_number)
            print_colored("✓ Code sent successfully!", 'green')
        except Exception as e:
            print_colored(f"✗ Error sending code: {e}", 'red')
            return
        
        otp = input("Enter the OTP you received: ")
        
        try:
            await client.sign_in(phone_number, otp)
            print_colored("✓ Login successful.", "green")
        except SessionPasswordNeededError:
            print_colored("2FA password required.", "yellow")
            password = input("Enter your 2FA password: ")
            await client.sign_in(password=password)
            print_colored("✓ Login with 2FA successful.", "green")
        except Exception as e:
            print_colored(f"✗ Login failed: {e}", "red")
            return
    else:
        print_colored("✓ Already logged in.", "green")

    try:
        group_to_scrape = await client.get_entity(group_to_scrape)
        group_to_add = await client.get_entity(group_to_add)
    except Exception as e:
        print_colored(f"✗ Error getting groups: {e}", "red")
        return

    print_colored(f"\n📊 Scraping members from: {group_to_scrape.title}", 'cyan')
    members = await client.get_participants(group_to_scrape)
    print_colored(f"✓ Found {len(members)} members", 'green')
    
    print_colored(f"\n🚀 Starting to add members to: {group_to_add.title}", 'cyan')
    print_colored("⚠️  WARNING: Add delay between 10-30 seconds to avoid ban!", 'yellow')
    
    added_count = 0
    error_count = 0
    
    for i, member in enumerate(members):
        if member.bot:
            print_colored(f"[{i+1}/{len(members)}] Skipping bot: {member.username}", "red")
            continue
        if member.username is None:
            print_colored(f"[{i+1}/{len(members)}] Skipping deleted account: {member.id}", "red")
            continue  

        try:
            await client(functions.channels.InviteToChannelRequest(
                group_to_add, [member]
            ))
            added_count += 1
            print_colored(f"[{i+1}/{len(members)}] ✓ {member.username} added successfully.", "green")
            
            # ពន្យារពេលចៃដន្យ (យូរជាងមុន ដើម្បីកុំឲ្យគេដឹងថាជា bot)
            delay = random.randint(10, 30)  # 10-30 វិនាទី
            print_colored(f"    Waiting {delay} seconds...", "cyan")
            time.sleep(delay)
            
        except FloodWaitError as e:
            print_colored(f"[{i+1}/{len(members)}] ⚠️ Rate limit! Wait {e.seconds} seconds", "red")
            time.sleep(e.seconds + 10)  # បន្ថែម 10 វិនាទី
        except Exception as e:
            error_count += 1
            print_colored(f"[{i+1}/{len(members)}] ✗ Failed to add {member.username}: {e}", "red")
            time.sleep(5)  # ពន្យារពេល 5 វិនាទីបន្ទាប់ពីមានកំហុស
    
    print_colored(f"\n✅ Process completed!", 'green')
    print_colored(f"📊 Results:", 'cyan')
    print_colored(f"   Total members: {len(members)}", 'cyan')
    print_colored(f"   Successfully added: {added_count}", 'green')
    print_colored(f"   Errors: {error_count}", 'red' if error_count > 0 else 'green')

# ប្រើ asyncio.run() ជំនួសឲ្យ with client:
async def start():
    async with client:
        await main()

if __name__ == "__main__":
    asyncio.run(start())