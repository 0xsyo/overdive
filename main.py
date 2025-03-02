import requests
import json
import time
import random
from fake_useragent import UserAgent
from colorama import init, Fore, Style, Back
from web3 import Web3
import os
import sys
import threading
from datetime import datetime

# Initialize colorama
init()

# Constants
WALLET_API_URL = "https://overdive.xyz/api/membership/wallet/create/"
QUEST_API_URL = "https://overdive.xyz/api/membership/wallet-quests/?wallet_address={}"
TWITTER_AUTH_URL = "https://overdive.xyz/api/membership/twitter-auth-init/?wallet={}"
COMPLETE_QUEST_URL = "https://overdive.xyz/api/membership/wallet-quests/{}/complete/"
REFERRAL_URL = "https://fun.overdive.xyz/invitation/{}"
PROXY_FILE = "proxy.txt"
PRIVATE_KEY_FILE = "pk.txt"
REFCODE_FILE = "refcode.txt"
BALANCE_API_URL = "https://mainnet.base.org/"

# Function to generate proper request headers
def generate_request_headers(wallet_address=""):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id-ID,id;q=0.7",
        "content-type": "application/json",
        "origin": "https://fun.overdive.xyz",
        "referer": "https://fun.overdive.xyz/",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Brave\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

# Improved banner display with smooth animation
def rainbow_banner():
    os.system("clear" if os.name == "posix" else "cls")
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    banner = """
  _______                          
 |     __|.--.--.---.-.-----.---.-.
 |__     ||  |  |  _  |-- __|  _  |
 |_______||___  |___._|_____|___._|
          |_____|                   
    """
    
    banner_lines = banner.split('\n')
    
    # Print the entire banner with smooth color transition
    for line in banner_lines:
        color_line = ""
        for i, char in enumerate(line):
            color_line += colors[i % len(colors)] + char
        sys.stdout.write(color_line + "\n")
        sys.stdout.flush()
        time.sleep(0.05)
    
    # Loading animation
    loading_text = "Starting Overdive Bot..."
    sys.stdout.write(Fore.LIGHTYELLOW_EX + "\n" + loading_text)
    sys.stdout.flush()
    
    for _ in range(3):
        for char in [".", "..", "..."]:
            sys.stdout.write("\r" + loading_text + char.ljust(3))
            sys.stdout.flush()
            time.sleep(0.3)
    
    print("\n" + Fore.LIGHTYELLOW_EX + "Ready!" + Style.RESET_ALL)
    time.sleep(0.5)
    
    # Clear and redisplay static banner
    os.system("clear" if os.name == "posix" else "cls")
    for line in banner_lines:
        color_line = ""
        for i, char in enumerate(line):
            color_line += colors[i % len(colors)] + char
        print(color_line)
    print(Fore.LIGHTYELLOW_EX + "\nOverdive Quest Bot" + Style.RESET_ALL)
    print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)

# Dynamic countdown timer
def countdown(seconds, message="Waiting"):
    start_time = time.time()
    end_time = start_time + seconds
    
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        sys.stdout.write(f"\r{Fore.YELLOW}{message}: {timer}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write(f"\r{Fore.GREEN}{message} completed!{' ' * 20}\n{Style.RESET_ALL}")
    sys.stdout.flush()

# Load private keys
def load_private_keys():
    try:
        with open(PRIVATE_KEY_FILE, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {PRIVATE_KEY_FILE} not found!{Style.RESET_ALL}")
        return []

# Load referral code
def load_referral_code():
    try:
        with open(REFCODE_FILE, 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        print(f"{Fore.YELLOW}Warning: {REFCODE_FILE} not found. No referral code will be used.{Style.RESET_ALL}")
        return ""

# Load proxies
def load_proxies():
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r') as f:
                proxies = [line.strip() for line in f.readlines()]
            print(f"{Fore.GREEN}Loaded {len(proxies)} proxies.{Style.RESET_ALL}")
            return proxies
        else:
            print(f"{Fore.YELLOW}Warning: {PROXY_FILE} not found. Running without proxies.{Style.RESET_ALL}")
            return []
    except Exception as e:
        print(f"{Fore.RED}Error loading proxies: {str(e)}{Style.RESET_ALL}")
        return []

# Function to get random proxy
def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None

# Function to connect wallet
def connect_wallet(private_key, proxies):
    try:
        web3 = Web3()
        account = web3.eth.account.from_key(private_key)
        wallet_address = web3.to_checksum_address(account.address)
        
        # Include viral_code in payload
        payload = {
            "wallet_address": wallet_address,
            "viral_code": load_referral_code()
        }
        
        # Get proper headers
        headers = generate_request_headers(wallet_address)
        
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        print(f"{Fore.YELLOW}Connecting wallet: {wallet_address[:6]}...{wallet_address[-4:]}{Style.RESET_ALL}")
        response = requests.post(WALLET_API_URL, json=payload, headers=headers, proxies=proxy_dict)
        
        if response.status_code == 200:
            response_data = response.json()
            if "wallet" in response_data:
                print(f"{Fore.GREEN}Wallet connected successfully!{Style.RESET_ALL}")
                return wallet_address, proxy
            else:
                print(f"{Fore.RED}Error: Invalid response data.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: {response.status_code} - {response.text}{Style.RESET_ALL}")
        
        return None, None
    except Exception as e:
        print(f"{Fore.RED}Error connecting wallet: {str(e)}{Style.RESET_ALL}")
        return None, None

# Function to get user quests and total points
def get_quests_and_points(wallet_address, proxies):
    try:
        headers = generate_request_headers(wallet_address)
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        print(f"{Fore.YELLOW}Fetching quests for wallet: {wallet_address[:6]}...{wallet_address[-4:]}{Style.RESET_ALL}")
        response = requests.get(QUEST_API_URL.format(wallet_address), headers=headers, proxies=proxy_dict)
        
        if response.status_code == 200:
            data = response.json()
            quests = data.get("quests", [])
            total_points = data.get("total_points", 0)
            print(f"{Fore.GREEN}Found {len(quests)} quests with {total_points} total points.{Style.RESET_ALL}")
            return quests, total_points
        else:
            print(f"{Fore.RED}Error fetching quests: {response.status_code} - {response.text}{Style.RESET_ALL}")
        
        return [], 0
    except Exception as e:
        print(f"{Fore.RED}Error getting quests: {str(e)}{Style.RESET_ALL}")
        return [], 0

# Function to get wallet balance
def get_wallet_balance(wallet_address, proxies):
    try:
        headers = generate_request_headers(wallet_address)
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [wallet_address, "latest"],
            "id": 0
        }
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        print(f"{Fore.YELLOW}Checking wallet balance...{Style.RESET_ALL}")
        response = requests.post(BALANCE_API_URL, json=payload, headers=headers, proxies=proxy_dict)
        
        if response.status_code == 200:
            response_data = response.json()
            if "result" in response_data:
                balance_wei = int(response_data["result"], 16)
                balance_eth = Web3.from_wei(balance_wei, 'ether')
                return balance_eth
            else:
                print(f"{Fore.RED}Error: Invalid balance response.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error checking balance: {response.status_code}{Style.RESET_ALL}")
        
        return None
    except Exception as e:
        print(f"{Fore.RED}Error getting balance: {str(e)}{Style.RESET_ALL}")
        return None

# Function to display user information
def display_user_info(wallet_address, twitter_handle, balance, proxy, total_points):
    print(Fore.CYAN + "┏" + "━" * 50 + "┓")
    print(Fore.CYAN + "┃" + " USER INFORMATION ".center(50) + "┃")
    print(Fore.CYAN + "┣" + "━" * 50 + "┫")
    print(Fore.CYAN + "┃" + f" Wallet   : {wallet_address[:6]}...{wallet_address[-4:]}".ljust(50) + "┃")
    print(Fore.CYAN + "┃" + f" Twitter  : {twitter_handle or 'Not connected'}".ljust(50) + "┃")
    print(Fore.CYAN + "┃" + f" Balance  : {balance if balance is not None else 'Unknown'} ETH".ljust(50) + "┃")
    print(Fore.CYAN + "┃" + f" Proxy    : {proxy or 'None'}".ljust(50) + "┃")
    print(Fore.CYAN + "┃" + f" Points   : {total_points}".ljust(50) + "┃")
    print(Fore.CYAN + "┗" + "━" * 50 + "┛")

# Function to complete a task
def complete_task(wallet_address, task_id, proxies):
    try:
        headers = generate_request_headers(wallet_address)
        payload = {
            "wallet_address": wallet_address
        }
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        print(f"{Fore.YELLOW}Completing quest ID: {task_id}...{Style.RESET_ALL}")
        response = requests.post(COMPLETE_QUEST_URL.format(task_id), json=payload, headers=headers, proxies=proxy_dict)
        
        if response.status_code == 200:
            response_data = response.json()
            points_earned = response_data.get('points_earned', 0)
            print(f"{Fore.GREEN}Task completed! Points earned: {points_earned}{Style.RESET_ALL}")
            return points_earned
        else:
            print(f"{Fore.RED}Error completing task: {response.status_code} - {response.text}{Style.RESET_ALL}")
        
        return 0
    except Exception as e:
        print(f"{Fore.RED}Error completing task: {str(e)}{Style.RESET_ALL}")
        return 0

# Function to authenticate Twitter
def twitter_auth(wallet_address, proxies):
    try:
        headers = generate_request_headers(wallet_address)
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        print(f"{Fore.YELLOW}Authenticating Twitter for wallet: {wallet_address[:6]}...{wallet_address[-4:]}{Style.RESET_ALL}")
        response = requests.get(TWITTER_AUTH_URL.format(wallet_address), headers=headers, proxies=proxy_dict)
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                twitter_handle = response_data.get("twitter_handle", "")
                print(f"{Fore.GREEN}Twitter authenticated: {twitter_handle}{Style.RESET_ALL}")
                return twitter_handle
            else:
                print(f"{Fore.YELLOW}Twitter not authenticated.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error authenticating Twitter: {response.status_code}{Style.RESET_ALL}")
        
        return None
    except Exception as e:
        print(f"{Fore.RED}Error authenticating Twitter: {str(e)}{Style.RESET_ALL}")
        return None

# Main function
def main():
    # Display banner
    rainbow_banner()
    
    # Load resources
    private_keys = load_private_keys()
    proxies = load_proxies()
    
    if not private_keys:
        print(f"{Fore.RED}No private keys found. Exiting.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}Loaded {len(private_keys)} wallet(s).{Style.RESET_ALL}")
    print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)
    
        # Process each account
    for idx, private_key in enumerate(private_keys):
        try:
            print(f"{Fore.MAGENTA}Processing wallet {idx + 1}/{len(private_keys)}{Style.RESET_ALL}")
            
            web3 = Web3()
            account = web3.eth.account.from_key(private_key)
            wallet_address = web3.to_checksum_address(account.address)
            
            # Connect wallet
            wallet_address, proxy = connect_wallet(private_key, proxies)
            if not wallet_address:
                print(f"{Fore.RED}Failed to connect wallet. Skipping to next account.{Style.RESET_ALL}")
                print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)
                continue
            
            # Authenticate Twitter
            twitter_handle = twitter_auth(wallet_address, proxies)
            
            # Get wallet balance
            balance = get_wallet_balance(wallet_address, proxies)
            
            # Get quests and total points
            quests, total_points = get_quests_and_points(wallet_address, proxies)
            
            # Display user information
            display_user_info(wallet_address, twitter_handle, balance, proxy, total_points)
            
            if quests:
                incomplete_quests = [q for q in quests if not q["is_completed"]]
                if incomplete_quests:
                    print(f"{Fore.GREEN}Found {len(incomplete_quests)} incomplete quests.{Style.RESET_ALL}")
                    
                    # Display quests
                    print(Fore.YELLOW + "┏" + "━" * 50 + "┓")
                    print(Fore.YELLOW + "┃" + " AVAILABLE QUESTS ".center(50) + "┃")
                    print(Fore.YELLOW + "┣" + "━" * 50 + "┫")
                    
                    for i, quest in enumerate(incomplete_quests):
                        print(Fore.YELLOW + "┃" + f" {i+1}. {quest['name']} ({quest['points']} pts)".ljust(50) + "┃")
                    
                    print(Fore.YELLOW + "┗" + "━" * 50 + "┛")
                    
                    # Complete tasks
                    for quest in incomplete_quests:
                        print(f"{Fore.CYAN}Starting quest: {quest['name']} (ID: {quest['id']}, Points: {quest['points']}){Style.RESET_ALL}")
                        points_earned = complete_task(wallet_address, quest["id"], proxies)
                        total_points += points_earned
                        
                        # Log completion time
                        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"{Fore.YELLOW}Completed at (UTC): {current_time}{Style.RESET_ALL}")
                        
                        # Delay before next task
                        if quest != incomplete_quests[-1]:  # Don't wait after the last task
                            delay = random.randint(7, 14)
                            countdown(delay, "Waiting before next task")
                else:
                    print(f"{Fore.GREEN}All quests are already completed!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No quests found for this wallet.{Style.RESET_ALL}")
            
            # Update user information with total points
            print(f"\n{Fore.GREEN}Finished processing tasks for this wallet.{Style.RESET_ALL}")
            display_user_info(wallet_address, twitter_handle, balance, proxy, total_points)
            
            # Delay between accounts
            if idx < len(private_keys) - 1:
                delay = random.randint(7, 30)
                countdown(delay, "Waiting before next account")
            
            print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)
        
        except Exception as e:
            print(f"{Fore.RED}Error processing wallet: {str(e)}{Style.RESET_ALL}")
            print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)
    
    # All accounts processed
    print(f"{Fore.GREEN}All accounts processed successfully!{Style.RESET_ALL}")
    
    # Log completion time
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Fore.YELLOW}Batch completed at (UTC): {current_time}{Style.RESET_ALL}")
    
    # Random looping delay
    loop_delay = random.randint(24 * 60 * 60, 24 * 60 * 60 + 77 * 60)
    hours = loop_delay // 3600
    minutes = (loop_delay % 3600) // 60
    print(f"{Fore.MAGENTA}Next loop scheduled in {hours} hours and {minutes} minutes{Style.RESET_ALL}")
    
    try:
        countdown(loop_delay, "Next run in")
        return True  # Signal to run again
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program stopped by user.{Style.RESET_ALL}")
        return False

# Entry point
if __name__ == "__main__":
    try:
        print(f"{Fore.GREEN}Starting Overdive Bot at (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Current User: {os.getenv('USER', 'Unknown')}{Style.RESET_ALL}")
        print(Fore.MAGENTA + "━" * 50 + Style.RESET_ALL)
        
        running = True
        while running:
            running = main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
    finally:
        print(f"{Fore.MAGENTA}Thank you for using Overdive Bot.{Style.RESET_ALL}")
