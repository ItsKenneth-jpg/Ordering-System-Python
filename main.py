import os
import sys
from datetime import datetime

# ==========================================
# 1. GLOBAL DATA & CONFIGURATION
# ==========================================

# Menu items stored in a nested dictionary

DRINK_MENU = {
    1: {"name": "Cappuccino", "price": 69.00},
    2: {"name": "Latte", "price": 59.00},
    3: {"name": "Caramel", "price": 49.00},
    4: {"name": "Mocha", "price": 75.00},
    5: {"name": "Espresso", "price": 45.00},
    6: {"name": "Macchiato", "price": 65.00},
    7: {"name": "Whole Milk", "price": 35.00}
}

# Add-ons stored in a dictionary

ADDON_MENU = {
    1: {"name": "Chocolate Syrup", "price": 15.00},
    2: {"name": "Strawberry Syrup", "price": 15.00},
    3: {"name": "Caramel Drizzle", "price": 10.00},
    4: {"name": "Whipped Cream", "price": 20.00}
}

# Discount Configuration

DISCOUNT_RATES = {
    "1": ("None", 0.0),
    "2": ("Senior/PWD 20%", 0.20),
    "3": ("Student 10%", 0.10)
}

# Global order tracking counter

order_counter = 125
MAX_ATTEMPTS = 5


# ==========================================
# 2. HELPER & DISPLAY FUNCTIONS
# ==========================================

def clear_screen():
    """Clears console screen for Windows, Linux, and macOS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_drink_menu():
    """Prints the drink menu using a for loop over the DRINK_MENU dictionary."""
    print("\n+**************************************+")
    print("|            Select Drink              |")
    print("+**************************************+")
    print(f"| {'No':<5} | {'Item':<15} | {'Price':<10} |")
    print("+--------------------------------------+ ")

    # Printing drink items using for loop

    for item_id in DRINK_MENU:
        item = DRINK_MENU[item_id]
        print(f"| {item_id:<5} | {item['name']:<15} | {item['price']:<10.2f} |")

    print("+**************************************+\n")


def print_addon_menu():
    """Prints the additionals menu using a for loop over the ADDON_MENU dictionary."""
    print("\n+**************************************+")
    print("|          Select Additionals          |")
    print("+**************************************+")
    print(f"| {'No':<5} | {'Item':<18} | {'Price':<8} |")
    print("+--------------------------------------+ ")

    # Printing addon items using for loop

    for addon_id in ADDON_MENU:
        addon = ADDON_MENU[addon_id]
        print(f"| {addon_id:<5} | {addon['name']:<18} | {addon['price']:<8.2f} |")

    print("+**************************************+\n")


def print_cart_summary(cart_drinks, cart_addons):
    """Displays current items in order using for loops."""
    print("\n-------------------------------------------------------------")
    print(f"| {'Product':<18} | {'Price':<7} | {'Quantity':<8} | {'Total':<10} |")
    print("-------------------------------------------------------------")

    # Loop to print ordered drinks

    for item_id in cart_drinks:
        item_data = DRINK_MENU[item_id]
        qty = cart_drinks[item_id]
        line_total = item_data['price'] * qty
        print(f"| {item_data['name']:<18} | {item_data['price']:<7.2f} | {qty:<8d} | {line_total:<10.2f} |")

    print("-------------------------------------------------------------")

    # Loop to print ordered add-ons if present

    if any(qty > 0 for qty in cart_addons.values()):
        print("| ADD-ONS:")
        for addon_id in cart_addons:
            qty = cart_addons[addon_id]
            if qty > 0:
                addon_data = ADDON_MENU[addon_id]
                line_total = addon_data['price'] * qty
                print(f"| - {addon_data['name']:<16} | {addon_data['price']:<7.2f} | {qty:<8d} | {line_total:<10.2f} |")
        print("-------------------------------------------------------------")


def print_receipt(cart_drinks, cart_addons, subtotal, discount_amt, discount_label, final_total):
    """Prints realistic itemized thermal receipt using for loops."""
    global order_counter
    now_str = datetime.now().strftime("%m/%d/%Y  %I:%M %p")

    print("================================")
    print("        Kenchi's Cafe           ")
    print("      Minglanilla, Cebu         ")
    print("        0912-345-6789           ")
    print("================================")
    print(f"Date: {now_str}")
    print(f"Order No: {order_counter:05d}")
    print("--------------------------------")
    print(f"{'ITEM':<18} {'QTY':<4} {'PRICE':>8}")
    print("--------------------------------")

    # Print drinks in receipt using for loop

    for item_id in cart_drinks:
        qty = cart_drinks[item_id]
        if qty > 0:
            item = DRINK_MENU[item_id]
            line_total = item['price'] * qty
            print(f"{item['name']:<18} {qty:<4} {line_total:>7.2f}")

    # Print add-ons in receipt using for loop

    for addon_id in cart_addons:
        qty = cart_addons[addon_id]
        if qty > 0:
            addon = ADDON_MENU[addon_id]
            line_total = addon['price'] * qty
            print(f"{addon['name']:<18} {qty:<4} {line_total:>7.2f}")

    print("--------------------------------")
    print(f"{'Subtotal:':<23} {subtotal:>7.2f}")
    if discount_amt > 0:
        print(f"Discount ({discount_label}): -{discount_amt:>7.2f}")
    print("--------------------------------")
    print(f"{'TOTAL AMOUNT DUE:':<23} {final_total:>7.2f}\n")
    print("================================")
    print("       THANK YOU FOR ORDERING!  ")
    print("          Please come again!    ")
    print("================================\n")

    order_counter += 1


# ==========================================
# 3. MAIN LOGIC
# ==========================================

def main():
    # Initial program startup prompt

    while True:

        print("\n***********************************************")
        print("             Welcome to Kenchi's Cafe          ")
        print("***********************************************")

        initial_ask = input("Would you like to place an order? (y/n): ").strip().lower()
        if initial_ask in ['y', 'n']:
            break
        print("Invalid input! Please type 'y' or 'n'.")

    if initial_ask == 'n':
        print("\nThank you for visiting Kenchi's Cafe!\n")
        sys.exit(0)

    spam_count_choice = 0
    spam_count_quan = 0
    spam_count_again = 0

    cart_drinks = {i: 0 for i in DRINK_MENU}
    cart_addons = {i: 0 for i in ADDON_MENU}

    # Ordering loop (up to 4 menu selections max)

    for _ in range(4):
        clear_screen()
        print_drink_menu()

        # Choice validation

        while True:
            choice_input = input("Enter product choice: ").strip()
            if not choice_input.isdigit():
                clear_screen()
                print_drink_menu()
                print("Invalid input! Please enter numbers only (1-7).")
                choice = 0
            else:
                choice = int(choice_input)
                if choice not in DRINK_MENU:
                    clear_screen()
                    print_drink_menu()
                    print("The choice customer wants is not available in the menu.")
                    choice = 0

            if choice == 0:
                spam_count_choice += 1
                if spam_count_choice >= MAX_ATTEMPTS:
                    print("\nToo many attempts. Try again later.")
                    sys.exit(0)
            else:
                break

        # Quantity validation

        while True:
            quan_input = input("Enter Quantity: ").strip()
            if not quan_input.isdigit():
                clear_screen()
                print("Invalid input! Please enter whole number only.")
                quan = 0
            else:
                quan = int(quan_input)
                if quan <= 0:
                    clear_screen()
                    print("Invalid Input")
                    quan = 0

            if quan == 0:
                spam_count_quan += 1
                if spam_count_quan >= MAX_ATTEMPTS:
                    clear_screen()
                    print("\nToo many attempts. Try again later.")
                    sys.exit(0)
            else:
                break

        # Accumulate item into cart dictionary

        cart_drinks[choice] += quan

        # Add-ons prompt with human error handling

        spam_count_addon = 0
        while True:
            add_option = input("\nWould you like to add Additionals/Syrups? (y/n): ").strip().lower()
            if add_option in ['y', 'n']:
                break
            print("Invalid input! Please type 'y' or 'n'.")
            spam_count_addon += 1
            if spam_count_addon >= MAX_ATTEMPTS:
                clear_screen()
                print("\nToo many attempts. Try again later.")
                sys.exit(0)

        if add_option == 'y':
            print_addon_menu()
            spam_count_addon_choice = 0
            while True:
                addon_choice_input = input("Enter additional choice (1-4): ").strip()
                if addon_choice_input.isdigit() and int(addon_choice_input) in ADDON_MENU:
                    addon_choice = int(addon_choice_input)

                    # Quantity loop for additionals
                    while True:
                        addon_quan_input = input("Enter Quantity for additional: ").strip()
                        if addon_quan_input.isdigit() and int(addon_quan_input) > 0:
                            add_quan = int(addon_quan_input)
                            cart_addons[addon_choice] += add_quan
                            break
                        else:
                            print("Invalid quantity! Please enter a whole number greater than 0.")
                    break
                else:
                    print("Invalid choice! Please select an option between 1 and 4.")
                    spam_count_addon_choice += 1
                    if spam_count_addon_choice >= MAX_ATTEMPTS:
                        clear_screen()
                        print("\nToo many attempts. Try again later.")
                        sys.exit(0)

        clear_screen()
        print_cart_summary(cart_drinks, cart_addons)

        # Prompt to continue ordering

        while True:
            response = input("\nDo you want to order another item? (y/n): ").strip().lower()
            if response not in ['y', 'n']:
                clear_screen()
                print_cart_summary(cart_drinks, cart_addons)
                print("Invalid input! Please type only 'y' or 'n'.")

                spam_count_again += 1
                if spam_count_again >= MAX_ATTEMPTS:
                    clear_screen()
                    print("\nToo many attempts. Try again later.")
                    sys.exit(0)
            else:
                break

        if response == 'n':
            break

    # Check if any items were ordered

    if not any(qty > 0 for qty in cart_drinks.values()):
        print("\nNo items selected. Exiting system...")
        sys.exit(0)

    # Calculate Subtotal using for loops

    subtotal_val = 0.0
    for item_id in cart_drinks:
        subtotal_val += DRINK_MENU[item_id]['price'] * cart_drinks[item_id]
    for addon_id in cart_addons:
        subtotal_val += ADDON_MENU[addon_id]['price'] * cart_addons[addon_id]

    # Apply discount option with human error handling

    print("\n--- Discount Options ---")
    print("[1] Regular Customer (No Discount)")
    print("[2] Senior Citizen / PWD (20% Discount)")
    print("[3] Student (10% Discount)")

    spam_count_disc = 0
    while True:
        disc_choice = input("Select Discount Option (1-3): ").strip()
        if disc_choice in DISCOUNT_RATES:
            break
        print("Invalid option! Please enter 1, 2, or 3.")
        spam_count_disc += 1
        if spam_count_disc >= MAX_ATTEMPTS:
            clear_screen()
            print("\nToo many attempts. Try again later.")
            sys.exit(0)

    discount_label, rate = DISCOUNT_RATES[disc_choice]
    discount_amt = subtotal_val * rate
    totaltotal = subtotal_val - discount_amt

    # Print Order Receipt

    clear_screen()
    print_receipt(cart_drinks, cart_addons, subtotal_val, discount_amt, discount_label, totaltotal)


if __name__ == "__main__":
    main()