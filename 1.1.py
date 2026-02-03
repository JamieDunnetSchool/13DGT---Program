"""This program is a for a menu."""


Bread = {
        "Wholemeal": 1.00,
        "White": 0.80,
        "Cheesy White": 1.20,
        "Gluten Free": 1.40
    }
Meat ={
        "Chicken": 2.69,
        "Beef": 3.00,
        "Salami": 4.00,
        "Vegan Slice": 3.30
    }
Garnish = {
        "Onion": 1.69,
        "Tomato": 1.00,
        "Lettuce": 2.00,
        "Cheese": 2.50
    }



welcome = input("Welcome to online samwichs a subway rip off would you like to order? Yes/No")

def intro():
    if welcome == "No" or "no":
        print("If you did not want to order why did you start this?") 

    elif welcome == "Yes" or "yes":
        print("What kind of bread do you want?")

    else:
        print("You must say yes or no.") 
        