import requests

def get_exchange_rate(base="USD", target="EUR"):
    url = "https://api.frankfurter.dev/v1/latest"
    params = {"from": base, "to": target}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "rates" not in data or target not in data["rates"]:
            raise ValueError("نرخ موردنظر در پاسخ API پیدا نشد.")

        return data["rates"][target]

    except requests.exceptions.Timeout:
        print("خطا: درخواست بیش از حد طول کشید.")
    except requests.exceptions.ConnectionError:
        print("خطا: اتصال به اینترنت برقرار نشد.")
    except requests.exceptions.HTTPError as e:
        print(f"خطای HTTP: {e}")
    except ValueError as e:
        print(f"خطای داده: {e}")
    except Exception as e:
        print(f"خطای ناشناخته: {e}")

    return None

def main():
    rate = get_exchange_rate("USD", "EUR")
    if rate is not None:
        print(f"1 USD = {rate} EUR")

if __name__ == "__main__":
    main()
