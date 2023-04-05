import os
import requests
import asyncio
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv('.env')
api_key = os.getenv('API')


def get_headers():
    return {
        'apikey': api_key,
    }


def get_valid_symbols():
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    data = response.json()
    valid_symbols = data["symbols"]
    return valid_symbols


def get_payload(valid_symbols):
    while True:
        currency1 = input("Enter the currency you want to convert from: ").upper().strip()
        currency2 = input("Enter the currency you want to convert to: ").upper().strip()

        # Check if the currency symbols are valid
        if currency1 in valid_symbols and currency2 in valid_symbols:
            break
        else:
            currencies(valid_symbols)
            print("\033[31m" + "Invalid currency symbols. Please enter valid symbols from the list above.\n" + "\033[0m")

    amount = float(input("Amount: "))

    return {
        'from': currency1,
        'to': currency2,
        'amount': amount,
    }


def convert(valid_symbols):
    payload = get_payload(valid_symbols)

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = get_headers()

    response = requests.get(url, headers=headers, params=payload)
    data = response.json()
    result = data["result"]
    print("\n\033[32m" + f"{payload['from']} -> {payload['to']} = ${round(result, 2)}" + "\033[0m")



def currencies(valid_symbols):
    for code, name in valid_symbols.items():
        print(f"\n{code} -> {name}")
        print('-' * 50)


async def main():
    valid_symbols = get_valid_symbols()
    first_run = True
    while True:
        if first_run:
            print("\nWelcome to the Currency Converter!")
            print("\033[33m" + "\nHere are the available commands: " + "\033[0m")
            first_run = False
        else:
            print("\033[33m" + "\nHere are the available commands: " + "\033[0m")
        print("1. List of Currencies")
        print("2. Convert Currencies")
        print("3. Exit")
        print('-' * 50)

        command = input("Enter a command: ")
        if command == "1":
            currencies(valid_symbols)
        elif command == "2":
            convert(valid_symbols)
        elif command == "3":
            exit()


if __name__ == "__main__":
    asyncio.run(main())
