import requests
import time
import os
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

URL = "https://www.tgju.org/profile/price_dollar_rl"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    price_span = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
    
    if price_span:
        price = price_span.text.replace(",", "")
        return int(price)

    return None


previous_price = None

while True:
    try:
        price = get_price()

        clear()
        print(Fore.CYAN + "💵 قیمت لحظه‌ای دلار (بازار ایران)")
        print("-" * 40)

        if price:

            if previous_price is None:
                print(Fore.YELLOW + f"{price:,} تومان")

            else:
                diff = price - previous_price

                if diff > 0:
                    print(Fore.GREEN + f"{price:,} تومان ▲ +{diff:,}")
                elif diff < 0:
                    print(Fore.RED + f"{price:,} تومان ▼ {diff:,}")
                else:
                    print(Fore.WHITE + f"{price:,} تومان (بدون تغییر)")

            previous_price = price

        else:
            print(Fore.RED + "نتوانستم قیمت را دریافت کنم")

        print("-" * 40)
        print("آپدیت بعدی: 10 ثانیه دیگر")

        time.sleep(10)

    except KeyboardInterrupt:
        print("\nخروج از برنامه")
        break

    except Exception as e:
        print("خطا:", e)
        time.sleep(10)
