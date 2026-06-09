import requests
import time
import os
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

URL = "https://www.tgju.org/profile/price_dollar_rl"

CSV_FILE = "price_history.csv"
UPDATE_INTERVAL = 10
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
MAX_ARCHIVES = 5  # فقط 5 آرشیو نگه داریم


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def get_archives():
    """لیست فایل‌های آرشیو که شبیه price_history_*.csv هستند"""
    archives = []
    for f in os.listdir("."):
        if f.startswith("price_history_") and f.endswith(".csv"):
            archives.append(f)
    # از قدیمی به جدید مرتب کنیم
    archives.sort()
    return archives


def cleanup_archives():
    """قدیمی‌ترهای آرشیو حذف شوند تا فقط 5 تا بمانند"""
    archives = get_archives()

    if len(archives) > MAX_ARCHIVES:
        extra = len(archives) - MAX_ARCHIVES
        for i in range(extra):
            os.remove(archives[i])  # قدیمی‌ترین‌ها
            print(f"حذف آرشیو قدیمی: {archives[i]}")


def rotate_file_if_needed():
    """اگر فایل بزرگ شد، آرشیو بساز و فایل جدید شروع کن"""
    if os.path.exists(CSV_FILE):
        file_size = os.path.getsize(CSV_FILE)
        if file_size >= MAX_FILE_SIZE:

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"price_history_{timestamp}.csv"

            os.rename(CSV_FILE, new_name)
            print(f"ساخت آرشیو جدید: {new_name}")

            cleanup_archives()  # بعد از ساخت آرشیو، قدیمی‌ها را پاک کن


def save_to_csv(price):
    rotate_file_if_needed()

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "price_toman"])

        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price])


def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    price_span = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
    if not price_span:
        return None

    txt = price_span.text.strip().replace(",", "")
    return int(txt) // 10  # تبدیل ریال به تومان


def print_price(price, previous_price):
    clear()
    now = datetime.now().strftime("%H:%M:%S")

    print(Fore.CYAN + "💵 قیمت لحظه‌ای دلار (بازار ایران)")
    print("-" * 45)

    if previous_price is None:
        print(Fore.YELLOW + f"{price:,} تومان")
    else:
        diff = price - previous_price
        percent = (diff / previous_price) * 100 if previous_price else 0

        if diff > 0:
            print(Fore.GREEN + f"{price:,} تومان ▲ +{diff:,} ({percent:+.2f}%)")
        elif diff < 0:
            print(Fore.RED + f"{price:,} تومان ▼ {diff:,} ({percent:+.2f}%)")
        else:
            print(Fore.WHITE + f"{price:,} تومان (بدون تغییر)")

    print("-" * 45)
    print(Fore.MAGENTA + f"آخرین بروزرسانی: {now}")
    print(f"آپدیت بعدی: {UPDATE_INTERVAL} ثانیه دیگر")


def main():
    previous_price = None

    while True:
        try:
            price = get_price()

            if price is not None:

                print_price(price, previous_price)

                # فقط هنگام تغییر قیمت ذخیره کن
                if previous_price is None or price != previous_price:
                    save_to_csv(price)

                previous_price = price

            else:
                clear()
                print(Fore.RED + "نتوانستم قیمت را دریافت کنم")

            time.sleep(UPDATE_INTERVAL)

        except KeyboardInterrupt:
            print("\nخروج از برنامه")
            break

        except Exception as e:
            clear()
            print(Fore.RED + f"خطا: {e}")
            print(f"تلاش دوباره تا {UPDATE_INTERVAL} ثانیه دیگر...")
            time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
