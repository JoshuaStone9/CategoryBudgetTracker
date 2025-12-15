class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": float(amount), "description": description})

    def withdraw(self, amount, description=""):
        amount = float(amount)
        if not self.check_funds(amount):
            return False
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category):
        amount = float(amount)
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, "Transfer to " + category.name)
        category.deposit(amount, "Transfer from " + self.name)
        return True

    def check_funds(self, amount):
        return float(amount) <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*")
        lines = [title]
        for item in self.ledger:
            desc = item["description"][:23]
            amt = item["amount"]
            lines.append("{:<23}{:>7.2f}".format(desc, amt))
        lines.append("Total: {:.2f}".format(self.get_balance()))
        return "\n".join(lines)


def create_spend_chart(categories):
    spent = []
    for c in categories:
        total = 0
        for item in c.ledger:
            if item["amount"] < 0:
                total += -item["amount"]
        spent.append(total)

    total_spent = 0
    for s in spent:
        total_spent += s

    percentages = []
    for s in spent:
        pct = (s / total_spent) * 100
        rounded = int(round(pct / 10.0) * 10)
        percentages.append(rounded)

    lines = ["Percentage spent by category"]

    for level in range(100, -1, -10):
        line = "{:>3}|".format(level)
        for p in percentages:
            if p >= level:
                line += " o "
            else:
                line += "   "
        line += " "
        lines.append(line)

    lines.append("    " + "-" * (3 * len(categories) + 1))

    names = []
    for c in categories:
        names.append(c.name)

    max_len = 0
    for n in names:
        if len(n) > max_len:
            max_len = len(n)

    for i in range(max_len):
        row = "     "
        for n in names:
            if i < len(n):
                row += n[i] + "  "
            else:
                row += "   "
        lines.append(row.rstrip())

    return "\n".join(lines)


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")

clothing = Category("Clothing")
food.transfer(50, clothing)

auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15, "gas")

print(food)
print()
print(create_spend_chart([food, clothing, auto]))
