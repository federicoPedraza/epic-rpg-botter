import pyautogui
import threading
import time
import console
from log import Log
from console import bcolors

lock = threading.Lock()

protection_cd = 5
antispam_cd = 2
postlock_cd = 5

def tryspell(spell_tag, inventory, requirement):
    # Check if there are any requirements
    requirement_count = inventory.get(str(requirement))
    if (requirement_count <= 0):
        console.log(f"There are no more resources for {spell_tag} ({requirement})")
        return

    # Take if untaken
    if lock.acquire(blocking=False):
        pyautogui.typewrite(spell_tag)
        pyautogui.press('enter')
        inventory.logs.log(spell_tag)
        inventory.remove(requirement)
        time.sleep(antispam_cd)
        lock.release()
    else:
        # Retry if already taken
        console.log(f"The following spell couldn't be spelled since it was locked: {spell_tag}", bcolors.WARNING)
        time.sleep(postlock_cd)
        tryspell(spell_tag, inventory, requirement)

def spell(mode, cooldown, inventory, requirement = 'nothing'):
    try:
        while True:
            time.sleep(cooldown + (protection_cd - antispam_cd))
            spell_tag = 'rpg ' + mode
            tryspell(spell_tag, inventory, requirement)
    except Exception as error:
        console.log(f"FATAL ERROR while spelling {mode}: {error}", bcolors.FAIL)
        exit()

def spell_and_heal(mode, cooldown, inventory):
    spell_tag = 'rpg ' + mode
    heal_potions = inventory.get('heal_potions')
    if (heal_potions <= 0):
        console.log(f"There are no more heal potions for {spell_tag}")
        return

    try:
        while True:
            time.sleep(cooldown + (protection_cd - antispam_cd))
            tryspell(spell_tag, inventory, 'heal_potions')
            tryspell('rpg heal', inventory, 'heal_potions')
    except Exception as error:
        print("There was an error while spelling: ", mode, error)
        exit()

def buy_and_open_lootbox(lootbox, cost, cooldown, inventory):
    try:
        while True:
            time.sleep(cooldown + ((protection_cd - antispam_cd) * 3))
            # Check balance
            bank = inventory.get('bank')
            gold = inventory.get('gold')
            balance = bank + gold
            if balance <= cost:
                console.log(f"You don't have enough money for the choosen lootbox (balance: {balance}", bcolors.WARNING)
                return
            
            # Retrieve gold if it's not enough
            if (gold <= cost):
                needed = cost - gold
                if needed > 0:
                    if bank >= needed:
                        tryspell(f'rpg withdraw {needed}', inventory, 'nothing')
                        inventory.remove('bank', needed)
                        inventory.add('gold', needed)
                    else:
                        console.log(f"You don't have enough money in the bank for the choosen lootbox (balance: {balance}", bcolors.WARNING)
                        return
            
            # Use gold

            tryspell(f'rpg buy {lootbox}', inventory, 'nothing')
            inventory.remove('gold', cost)
            tryspell(f'rpg open {lootbox}', inventory, 'nothing')
    except Exception as error:
        console.log(f"There was an error while buying lootboxes: {error}", bcolors.FAIL)
        exit()