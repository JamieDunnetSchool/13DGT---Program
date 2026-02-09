Bread = {
    "1": ("Wholemeal", 1.00),
    "2": ("White", 0.80),
    "3": ("Cheesy White", 1.20),
    "4": ("Gluten Free", 1.40)
}
Meat = {
    "1": ("Chicken", 2.69),
    "2": ("Beef", 3.00),
    "3": ("Salami", 4.00),
    "4": ("Vegan Slice", 3.30)
}
Garnish = {
    "1": ("Onion", 1.69),
    "2": ("Tomato", 1.00),
    "3": ("Lettuce", 2.00),
    "4": ("Cheese", 2.50),
}

print("Welcome to online samwichs a subway rip off would you like to order?")

def choose_item(category_name, options):
    print(f"\nChoose your {category_name}:")

    for key, value in options.items():
        name, price = value
        print(f"{key}. {name} - ${price:.2f}")

    while True:
        choice = input("Enter number: ")

        if choice in options:
            return options[choice]
        else:
            print("Invalid choice. Try again.")

def main():
    print("Welcome to online sandwiches, a Subway rip-off. Would you like to order?")

    while True:
        bread_name, bread_price = choose_item("Bread", Bread)
        meat_name, meat_price = choose_item("Meat", Meat)
        garnish_name, garnish_price = choose_item("Garnish", Garnish)

        overall_price = bread_price + meat_price + garnish_price

        confirm = input(
            f"Would you like to confirm this order?\n"
            f"Bread: {bread_name}\n"
            f"Meat: {meat_name}\n"
            f"Garnish: {garnish_name}\n"
            f"Total: ${overall_price:.2f}\n"
            f"1 = Yes, 2 = No\n"
        )

        if confirm == "1":
            print("Thank you for shoping at online samuchinces")
            break
        else:
            continue  # redo the order

main()