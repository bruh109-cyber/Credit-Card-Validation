import argparse
import re


def check_credit_card_number(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0


def get_card_type(card_number):
    card_number = card_number.replace(' ', '')
    card_types = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "MasterCard": r"^5[1-5][0-9]{14}$",
        "American Express": r"^3[47][0-9]{13}$",
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$",
        "JCB": r"^(?:2131|1800|35\d{3})\d{11}$",
        "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
        "Maestro": r"^(5018|5020|5038|56|57|58|6304|6759|676[1-3])\d{8,15}$",
        "Verve": r"^(506[01]|507[89]|6500)\d{12,15}$"
    }
    
    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            return card_type
        return "Unknown"
            
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            card_numbers = file.readlines()
        results = {}
        for card_number in card_numbers:
            card_number = card_number.strip()
            is_valid = check_credit_card_number(card_number)
            card_type = get_card_type(card_number)
            results[card_number] = (is_valid, card_type)
        return results
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def main():
    parser = argparse.ArgumentParser(description="Check if a credit card number is legitimate and identify its type using the Luhn algorithm.")
    parser.add_argument('-n', '--number', type=str, help="A single credit card number to validate.")
    parser.add_argument('-f', '--file', type=str, help="A file containing multiple credit card numbers to validate.")
    args = parser.parse_args()
    if  args.number:
        is_valid = check_credit_card_number(args.number)
        card_type = get_card_type(args.number)
        print(f"[!] Credit card number {args.number} is {'valid' if is_valid else 'invalid'} and is of type {card_type}.")
    if args.file:
        results = process_file(args.file)
        if results:
            for card_number, (is_valid, card_type) in results.items():
                print(f"[!] Credit card number {card_number} is {'valid' if is_valid else 'invalid'} and is of type {card_type}.")

if __name__ == '__main__':
    main()









































