import csv
from datetime import date


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount should be over 0")
                continue
            return round(amount, 2)
        except ValueError:
            print("Try different amount")


def get_int(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number <= 0:
                print("Number should be over 0")
                continue
            return number
        except ValueError:
            print("Enter a whole number")


CATEGORIES = ("Food", "Transport", "Entertainment", "Bills", "Other")
LIMITS = {name: 0 for name in CATEGORIES}


def get_category():
    print("Categories:")
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"{number}-{name}")
    while True:
        try:
            choice = int(input("Choose a category number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print("Choose a number from the list")
        except ValueError:
            print("Enter a number")


def get_item_name():
    while True:
        item = input("What do you want to buy: ").strip().replace("|", "")
        if item:
            return item
        print("Item name can not be empty")


def get_limit(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                print("Limit can not be negative")
                continue
            return round(amount, 2)
        except ValueError:
            print("Try different amount")


def get_cost(purchase):
    return purchase["Cost"]


class BudgetAnalyser:
    def __init__(self):
        self.bank_account = 0.0
        self.expenses = 0.0
        self.inventory = []
        self.cash = 0.0

    # ---------- helpers for the two payment methods ----------
    def get_balance(self, method):
        if method == "cash":
            return self.cash
        return self.bank_account

    def set_balance(self, method, value):
        if method == "cash":
            self.cash = round(value, 2)
        else:
            self.bank_account = round(value, 2)

    # ---------- money in / out ----------
    def deposit(self):
        amount_deposit = get_amount("How much money you want to deposit: ")

        self.bank_account = round(self.bank_account + amount_deposit, 2)
        print()
        print()
        print(f"Current Balance {self.bank_account:.2f}$")

    def withdraw(self):
        amount_withdraw = get_amount("How much money you want to withdraw: ")
        if round(self.bank_account - amount_withdraw, 2) >= 0:
            self.bank_account = round(self.bank_account - amount_withdraw, 2)
            self.cash = round(self.cash + amount_withdraw, 2)
        else:
            print()
            print()
            print("Not enough balance")
        print()
        print()
        print(f"Current balance: {self.bank_account:.2f}$")
        print(f"Current cash: {self.cash:.2f}$")

    # ---------- limits ----------
    def get_category_total(self, category):
        total = 0
        for purchase in self.inventory:
            if purchase["Category"] == category:
                total += purchase["Cost"]
        return round(total, 2)

    def check_limit(self, category):
        spent = self.get_category_total(category)
        limit = LIMITS[category]
        if limit > 0 and spent > limit:
            print()
            print(f"WARNING: {category} limit exceeded! Spent {spent:.2f}$ of {limit}$")

    def set_limits(self):
        print()
        print()
        print("Setting limits")
        category = get_category()
        current = LIMITS[category]
        if current > 0:
            print(f"Current {category} limit: {current:.2f}$")
        else:
            print(f"No limit set for {category}")
        LIMITS[category] = get_limit(f"Enter new limit for {category} (0 = no limit): ")
        if LIMITS[category] > 0:
            print(f"{category} limit is now {LIMITS[category]:.2f}$")
        else:
            print(f"{category} limit removed")

    # ---------- shopping ----------
    def shopping(self):
        print()
        print()
        print("How do you want to pay")
        print("Cash-1")
        print("Bank account-2")
        choice = input("Which one you want to use: ")

        if choice == "1":
            self.buy_items("cash")
        elif choice == "2":
            self.buy_items("bank")
        else:
            print("Wrong command")

    def buy_items(self, method):
        item_count = get_int("How many items you want to buy: ")
        for _ in range(item_count):
            spend_amount = get_amount("how much it cost: ")
            balance = self.get_balance(method)
            if round(balance - spend_amount, 2) < 0:
                print()
                print()
                print("Not enough balance")
                print(f"Current balance is:{balance:.2f}$")
                break

            item = get_item_name()
            category = get_category()
            self.inventory.append({
                "Date": date.today().isoformat(),
                "Item": item,
                "Category": category,
                "Cost": spend_amount,
                "Method": method,
            })
            self.set_balance(method, balance - spend_amount)
            self.expenses = round(self.expenses + spend_amount, 2)

            print()
            print()
            print(f"You bought {item} ({category}) for {spend_amount:.2f}$")
            print(f"Current balance:{self.get_balance(method):.2f}$")
            self.check_limit(category)

    # ---------- search / undo ----------
    def search(self):
        keyword = input("Item name to search: ").strip().lower()
        if not keyword:
            print("Search word cannot be empty")
            return
        found = False
        for purchase in self.inventory:
            if keyword in purchase["Item"].lower():
                print()
                print()
                print(f"{purchase['Item']} | {purchase['Category']} | "
                      f"{purchase['Cost']:.2f}$ | paid by {purchase['Method']}")
                found = True
        if not found:
            print()
            print()
            print("No purchase found")

    def undo(self):
        if not self.inventory:
            print("Nothing to undo")
            return
        last = self.inventory.pop()
        method = last["Method"]
        self.set_balance(method, self.get_balance(method) + last["Cost"])
        self.expenses = round(self.expenses - last["Cost"], 2)
        print()
        print()
        print(f"Undone: {last['Item']} ({last['Cost']:.2f}$), refunded to {method}")
        print(f"Current balance in {method}: {self.get_balance(method):.2f}$")

    # ---------- summary ----------
    def summary(self):
        print()
        print()
        print(f"Money in bank: {self.bank_account:.2f}$")
        print(f"Money in cash: {self.cash:.2f}$")
        print(f"Expenses: {self.expenses:.2f}$")
        print("Purchases")

        for purchase in self.inventory:
            print(f"{purchase['Item']} ({purchase['Category']}): {purchase['Cost']:.2f}$")
        used = {purchase["Category"] for purchase in self.inventory}
        if used:
            print("Categories used:", ", ".join(sorted(used)))

        totals = {}
        for purchase in self.inventory:
            category = purchase["Category"]
            totals[category] = round(totals.get(category, 0) + purchase["Cost"], 2)
        if totals:
            print("Spending by category:")
            for category, total in totals.items():
                percent = total / self.expenses * 100
                limit = LIMITS[category]
                limit_text = f"{limit:.2f}$" if limit > 0 else "not set"
                line = f"{category}: {total:.2f}$ ({percent:.1f}%) | limit {limit_text}"
                if limit > 0 and total > limit:
                    line += " - EXCEEDED"
                print(line)

        if self.inventory:
            biggest = max(self.inventory, key=get_cost)
            print(f"Biggest expense: {biggest['Item']} ({biggest['Cost']:.2f}$)")

    # ---------- export ----------
    def export_csv(self, filename="expenses.csv"):
        if not self.inventory:
            print("Nothing to export")
            return
        columns = ["Date", "Item", "Category", "Cost", "Method"]
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(self.inventory)
        except OSError:
            print(f"Could not write {filename}. Close it if it is open in another program.")
            return
        print()
        print()
        print(f"Saved {len(self.inventory)} purchases to {filename}")


def main():
    budget = BudgetAnalyser()

    actions = {
        "1": budget.deposit,
        "2": budget.withdraw,
        "3": budget.shopping,
        "4": budget.summary,
        "5": budget.search,
        "6": budget.undo,
        "7": budget.set_limits,
        "8": budget.export_csv,
    }

    while True:
        print()
        print("Deposit money-1")
        print("Withdraw money-2")
        print("Shopping-3")
        print("Summary-4")
        print("Search purchase-5")
        print("Undo last purchase-6")
        print("Setting limits-7")
        print("Export purchases to CSV-8")
        print("Finishing the program-9")
        user_input = input("What do you want to do: ")

        if user_input == "9":
            break

        action = actions.get(user_input)
        if action:
            action()
        else:
            print("Wrong command")

    budget.summary()


if __name__ == "__main__":
    main()
