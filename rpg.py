#region imports
import threading
import time
import command
import os
import console
import atexit
from log import Log
from storage import Storage
from console import bcolors
#endregion

os.system('clear')
console.log('Welcome.', bcolors.HEADER)
console.separate()

#Cooldowns
hunt_cd = 60
farm_cd = 390
work_cd = 200
lootbox_cd = 10800
adventure_cd = 2340
guild_cd = 7200

console.log('Is this a test? y/X ', bcolors.BOLD)
is_test = input() == 'y'
if is_test:
    hunt_cd = 10
    farm_cd = 25
    work_cd = 15
    lootbox_cd = 60
    adventure_cd = 40
    guild_cd = 120

#region Inventory --
console.log('Please fill the required information: ', bcolors.WARNING)

gold = int(input('Gold: '))
bank = int(input('Bank: '))
normal_seeds = int(input('Seeds: '))
carrot_seeds = int(input('Carrot Seeds: '))
potato_seeds = int(input('Potato Seeds: '))
bread_seeds = int(input('Bread Seeds: '))
heal_potions = int(input('Heal Potions: '))

inventory = Storage(gold, bank, normal_seeds, carrot_seeds, potato_seeds, bread_seeds, heal_potions)
#endregion

#region Working options --
work_options = {
    1: "Axe",
    2: "Net",
    3: "Pickup",
    4: "Ladder",
    5: "Mine",
    6: "Bowsaw",
    7: "Boat",
    8: "Pickaxe",
    9: "Tractor",
    10: "Chainsaw",
    11: "bigboat",
    12: "Drill",
    13: "Greenhouse",
    14: "Dynamite",
}

work_command = console.multiple_choise(work_options)
console.separate()
#endregion

#region Hunting --
is_married = input('Are you married? y/X ')
together_command = ''

if is_married == 'y':
    together_command = 'together'
hunt_command = f'hunt {together_command}'
console.separate()
#endregion

#region Farming --

has_seeds = carrot_seeds > 0 or bread_seeds > 0 or normal_seeds > 0 or potato_seeds > 0

if has_seeds == False:
    console.log("You can't farm since you don't have any seeds", bcolors.WARNING)

seed_types = {
    0: "normal seeds",
    1: "carrot seeds",
    2: "bread seeds",
    3: "potato seeds"
}

seed_type = ""
if has_seeds:
    seed_type = console.multiple_choise(seed_types)

seed_type = seed_type.replace(' ', '_')
seed_command = 'farm ' + seed_type
console.separate()
#endregion

#region Guild --
has_guild = input('Are you in a guild? y/X ') == 'y'

guild_options = {
    1: 'Raid',
    2: 'Upgrade'
}
guild_command = "raid"

if has_guild:
    guild_command = console.multiple_choise(guild_options)
console.separate()
#endregion

#region Adventure --
console.log('Please, consider having heal potions for adventures, since they can take out hp and end up killing you multiple times', bcolors.WARNING)
if heal_potions <= 5:
    console.log(f'You have {heal_potions} heal potions', bcolors.FAIL)
does_adventures = input('Do you wanna do adventures? y/X ') == 'y'
console.separate()
#endregion

#region Lootboxes --
balance = inventory.get_balance()
if balance < 800:
    console.log(f"You won't be able to buy lootboxes, since you've {balance} coins in total", bcolors.WARNING)

does_lootboxes = balance >= 800

if does_lootboxes:
    does_lootboxes = input('Do you wanna buy lootboxes? y/X ') == 'y'


lootbox_options = {
    800: 'common lootbox',
    6000: 'uncommon lootbox',
    40000: 'rare lootbox',
    150000: 'epic lootbox',
    420666: 'edgy lootbox',
}

lootbox_command = ""

if does_lootboxes:
    console.log('Please, keep in mind that the money used for lootboxes will be withdrawn from the bank.', bcolors.WARNING)
    lootbox_command = console.multiple_choise_lootboxes(lootbox_options, balance)
    lootbox_cost = [k for k,v in lootbox_options.items() if v == lootbox_command][0]
console.separate()
#endregion

#Spelling --

console.log(f"Starting" , bcolors.OKGREEN)
current_time = time.ctime()
console.log(f"Time: {current_time}", bcolors.OKGREEN)

console.log(f"Hunting {together_command}", bcolors.OKGREEN)
hunt_thread = threading.Thread(target=command.spell, args=(hunt_command, hunt_cd, inventory))
hunt_thread.start()

if has_seeds:
    console.log(f"Farming ({seed_type})", bcolors.OKGREEN)
    farm_thread = threading.Thread(target=command.spell, args=(seed_command, farm_cd, inventory, seed_type))
    farm_thread.start()
else:
    console.log("Farming", bcolors.FAIL)

console.log(f"Working ({work_command})", bcolors.OKGREEN)
pickup_thread = threading.Thread(target=command.spell, args=(work_command, work_cd, inventory))
pickup_thread.start()

if does_adventures:
    console.log("Adventure", bcolors.WARNING)
    adventure_thread = threading.Thread(target=command.spell_and_heal, args=('adventure', adventure_cd, inventory))
    adventure_thread.start()
else:
    console.log("Adventure", bcolors.FAIL)

if has_guild:
    console.log("Guild", bcolors.OKGREEN)
    guild_thread = threading.Thread(target=command.spell, args=(guild_command, guild_cd, inventory))
    guild_thread.start()
else:
    console.log("Guild", bcolors.FAIL)

if does_lootboxes:
    console.log(f"Lootboxes ({lootbox_command}, cost: {lootbox_cost})", bcolors.OKGREEN )
    lootbox_thread = threading.Thread(target=command.buy_and_open_lootbox, args=(lootbox_command, lootbox_cost, lootbox_cd, inventory))
    lootbox_thread.start()
else:
    console.log("Lootboxes", bcolors.FAIL)

console.log("Starting next hunt, cheers!", bcolors.OKGREEN)
console.separate()
console.log("Logs: ", bcolors.HEADER)