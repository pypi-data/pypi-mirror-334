from time import sleep
from random import randint
#import vvpet_draw

class VvPet:
    def __init__(self, name, type):
        self.name = name
        self.type = type

        self.health = 10
        self.hunger = 10
        self.thirst = 10
        self.fun = 10

class Food:
    def __init__(self, name, price, hunger, thirst, fun):
        self.name = name
        self.price = price
        self.hunger = hunger
        self.thirst = thirst
        self.fun = fun

#INIT
print("Hi, come get your pet")
input_type = input("What type of pet do you want? [smile] ")
input_name = input("What will be the name of your pet? ")
print(f"Great, your pet will be a {input_type} named {input_name}")

pet = VvPet(input_name, input_type)
money = 100


def pet_stats():
    print(f"""
{pet.name} has the current stats:
Health = {pet.health}

Hunger = {pet.hunger}
Thirst = {pet.thirst}
Entertainment = {pet.fun}
""")

def show_pet():
    typ = pet.type
    if typ == "smile":
        #vvpet_draw.smile()
        pass

def tick():
    pet.hunger -= randint(1,3)
    pet.thirst -= randint(1,3)
    pet.fun -= randint(1,3)
    check_max()
    mood()


apple = Food("Apple", 10, 2, 1, 1)
cake = Food("Cake", 25, 5, 0, 5)
juice = Food("Juice Packet", 10, 0, 3, 2)
steak = Food("Steak", 45, 7, 3, 2)

shop_list = [apple, cake, juice, steak]
inventory = []

def inventory_show():
    if len(inventory) > 0:
        print("Your inventory contains:")
        si = 0
        for i in inventory:
            print(f"{si+1}, {i.name}, providing {i.hunger} hunger, {i.thirst} thirst and {i.fun} entertainment")
            si += 1
    else:
        print("Your inventory is empty")


def shop(money):
    print("Welcome to the shop, we have:")
    si = 0
    for i in shop_list:
        print(f"{si+1}. {i.name} for {i.price} crowns, providing {i.hunger} hunger, {i.thirst} thirst and {i.fun} entertainment")
        si += 1
    purchase = input("What do you wanna purchase? (type 'no' to exit) [number] ")
    if purchase == "no":
        return
    else:
        purchase = int(purchase)

    if money >= shop_list[purchase-1].price:
        money -= shop_list[purchase-1].price
        inventory.append(shop_list[purchase-1])
        print(f"You purchased {shop_list[purchase-1].name}")
    else:
        print("You dont have enough crowns for this")

def check_max():
    if pet.hunger > 10:
        pet.hunger = 10
    if pet.thirst > 10:
        pet.thirst = 10
    if pet.fun > 10:
        pet.fun = 10

    if pet.hunger <= 0:
        pet.health -= 1
    if pet.thirst <= 0:
        pet.health -= 1
    if pet.fun <= 0:
        pet.hunger -= 1
        pet.thirst -= 1

def mood():
    sum_stats = pet.health + pet.thirst + pet.fun + pet.hunger

    if sum_stats > 30:
        mood = "Perfect"
    elif sum_stats > 20 and sum_stats <= 30:
        mood = "Good"
    elif sum_stats <= 20 and sum_stats > 10:
        mood = "Meh"
    elif sum_stats <= 10 and sum_stats > 4:
        mood = "Bad"
    else:
        mood = "Terrible"
def feed():
    if len(inventory) > 0:
        inventory_show()
    else:
        print(f"You have nothing to feed {pet.name}")
    feed_num = int(input(f"What do you wanna feed to {pet.name}? [number] "))
    pet.hunger += inventory[feed_num-1].hunger
    pet.thirst += inventory[feed_num-1].thirst
    pet.fun += inventory[feed_num-1].fun
    check_max()

def pet_pet():
    pet.fun += 5
    print(f"{pet.name} liked that very much")

play = True
while play:
    action = input("What will be your next action? Type 'help' for help ")
    action = action.lower()
    if action == "end" or action == "exit":
        play = False
    elif action == "help":
        print("""
        UTILITY
        stats = show pet stats
        balance = see your crowns balance
        inventory = see your inventory
        mood = show the mood of your pet
        
        ACTIONS
        shop = buy food for your pet
        feed = feed your pet
        pet = pet your pet
        
        end = end the game
        """)
    elif action == "stats":
        pet_stats()
    elif action == "show":
        show_pet()
    elif action == "balance":
        print(f"You have {money} crowns")
    elif action == "shop":
        shop(money)
        tick()
    elif action == "inventory":
        inventory_show()
    elif action == "feed":
        feed()
        mood()
    elif action == "mood":
        print(f"{pet.name} is doing {mood}")
    elif action == "pet":
        pet_pet()
