# Budget Analyser

A console budget tracker written in Python with an object-oriented design. It tracks a bank balance and cash, records purchases by category, warns when a category limit is exceeded, and exports all purchases to a CSV file for further analysis.

Built as a project for the *Application of Advanced Programming Languages* course at Sejong University.

## Features

- Deposit money to the bank account and withdraw cash from it
- Buy several items at once, paid by cash or bank, with balance checks
- Five spending categories (Food, Transport, Entertainment, Bills, Other)
- Per-category spending limits with a warning when a limit is exceeded
- Search purchases by item name
- Undo the last purchase (the money is refunded to the account it was paid from)
- Summary: balances, total expenses, spending by category (amount and percent), biggest expense
- Export purchases to `expenses.csv` (columns: `Date, Item, Category, Cost, Method`)
- Input validation everywhere: wrong or empty input never crashes the program

## How to run

Requires Python 3.8 or newer. No external libraries are needed.

```bash
python budget_analyser.py
```

## Menu

```
Deposit money-1
Withdraw money-2
Shopping-3
Summary-4
Search purchase-5
Undo last purchase-6
Setting limits-7
Export purchases to CSV-8
Finishing the program-9
```

## Example session

```
What do you want to do: 1
How much money you want to deposit: 100
Current Balance 100.00$

What do you want to do: 3
How do you want to pay
Cash-1
Bank account-2
Which one you want to use: 2
How many items you want to buy: 1
how much it cost: 10
What do you want to buy: Bread
Choose a category number: 1
You bought Bread (Food) for 10.00$
Current balance:90.00$
```

## Python concepts used

- Classes and methods (`BudgetAnalyser`)
- `while` loops and `for` loops
- Dictionaries (menu actions, category limits, purchase records) and tuples
- Exception handling (`try/except`) for input validation
- File handling with the `csv` module
- Helper methods to avoid duplicate code (`buy_items`, `get_balance`, `set_balance`)

## Project structure

```
budget-analyser/
├── budget_analyser.py
├── README.md
└── .gitignore
```
