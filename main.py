import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Tuple
from itertools import cycle
from threading import Lock
from data.logger import NovaLogger
from colorama import Fore, Style

banner = f"""
{Fore.CYAN}
                        █████▒██▓ ██▓     ██▓   ▓██   ██▓
                        ▓██   ▒▓██▒▓██▒    ▓██▒    ▒██  ██▒
                        ▒████ ░▒██▒▒██░    ▒██░     ▒██ ██░
                        ░▓█▒  ░░██░▒██░    ▒██░     ░ ▐██▓░
                        ░▒█░   ░██░░██████▒░██████▒ ░ ██▒▓░
                        ▒ ░   ░▓  ░ ▒░▓  ░░ ▒░▓  ░  ██▒▒▒ 
                        ░      ▒ ░░ ░ ▒  ░░ ░ ▒  ░▓██ ░▒░ 
                        ░ ░    ▒ ░  ░ ░     ░ ░   ▒ ▒ ░░  
                                ░      ░  ░    ░  ░░ ░     
                                                ░ ░     

                        {Fore.LIGHTCYAN_EX}https://discord.gg/api{Style.RESET_ALL}
"""


class DecorationClaimer:
    def __init__(self):
        self.avatar_decoration_id = '1144058522808614924'
        self.avatar_decoration_sku_id = '1144058522808614923'
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        self.tokens = self._load_tokens()
        self.proxies = self._load_proxies()
        self.proxy_cycle = cycle(self.proxies) if self.proxies else None
        self.failed_proxies = set()
        self.proxy_lock = Lock()

    def _load_tokens(self) -> list:
        with open("input/tokens.txt") as f:
            return [line.strip().split(':')[2] for line in f if line.strip()]

    def _load_proxies(self) -> list:
        try:
            with open("input/proxies.txt") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def _get_headers(self, token: str) -> Dict:
        return {
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/shop',
            'user-agent': self.user_agent
        }

    def _get_next_valid_proxy(self) -> Optional[str]:
        with self.proxy_lock:
            for _ in range(len(self.proxies)):
                proxy = next(self.proxy_cycle)
                if proxy not in self.failed_proxies:
                    return proxy
            self.failed_proxies.clear()
            return next(self.proxy_cycle) if self.proxies else None


    def _claim_decoration(self, token: str, proxy: Optional[str] = None) -> bool:
        headers = self._get_headers(token)
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy} if proxy else None
        claim_payload = {'sku_id': self.avatar_decoration_sku_id}

        try:
            response = session.put(
                'https://discord.com/api/v9/users/@me/claim-premium-collectibles-product',
                headers=headers,
                json=claim_payload
            )
            
            if response.status_code in [200, 201, 204]:
                NovaLogger.win("Successfully claimed decoration", token=token[:25])
                return True
            else:
                NovaLogger.fail(f"Claim failed: {response.text}", token=token[:25])
                return False
        except Exception as e:
            NovaLogger.fail(f"Claim request error: {str(e)}", token=token[:25])
            return False

    def _equip_decoration(self, token: str, proxy: Optional[str] = None) -> bool:
        headers = self._get_headers(token)
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy} if proxy else None
        equip_payload = {'avatar_decoration': self.avatar_decoration_id}

        try:
            response = session.patch(
                'https://discord.com/api/v9/users/@me/profile',
                headers=headers,
                json=equip_payload
            )

            if response.status_code in [200, 201, 204]:
                NovaLogger.win("Successfully equipped decoration", token=token[:25])
                return True
            else:
                NovaLogger.fail(f"Equip failed: {response.text}", token=token[:25])
                return False
        except Exception as e:
            NovaLogger.fail(f"Equip request error: {str(e)}", token=token[:25])
            return False

    def process_token(self, token: str) -> None:
        proxy = self._get_next_valid_proxy() if self.proxies else None
        if self._claim_decoration(token, proxy):
            time.sleep(2)  # Small delay before equipping
            self._equip_decoration(token, proxy)

    def start(self) -> None:
        print(f"{Fore.CYAN}Starting Decoration Claimer & Equipper...{Style.RESET_ALL}")
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(self.process_token, self.tokens)

if __name__ == "__main__":
    print(banner)
    claimer = DecorationClaimer()
    claimer.start()
