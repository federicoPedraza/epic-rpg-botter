import console
import atexit
import time
import datetime
from console import bcolors

date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = f'logs/log_{date}.txt'

class Log:
    def __init__(self, inventory):
        self.gold = inventory.gold
        self.bank = inventory.bank
        self.basic = inventory.basic
        self.carrot = inventory.carrot,
        self.potato = inventory.potato,
        self.bread = inventory.bread,
        self.heal_potions = inventory.heal_potions

    def start_log(self):
        with open(filename, "w") as file:
            file.write('Run input: ')

    def log(self, message):
        time = datetime.datetime.now().strftime("%H-%M-%S")
        with open(filename, "a") as file:
            file.write(f'\n[{message.lower()}] -- {time}')

    def add(self, field, amount = 1):
        if hasattr(self, field):
            setattr(self, field, getattr(self, field) + amount)
        else:
            console.log(f'Error: Error on log {field}', bcolors.FAIL)

    def get(self, field):
        if hasattr(self, field):
            return getattr(self, field)
        else:
            console.log('Error: Trying to consume an empty resource', bcolors.FAIL)
            return -1

    def remove(self, field, amount = 1):
        setattr(self, field, getattr(self, field) - amount)

    def print(self, inventory):
        console.separate()
        current_time = time.ctime()
        console.log(f"Time: {current_time}", bcolors.BOLD)
        console.log('Official Log =) Thanks for using me! Here are your results', bcolors.HEADER)

        console.log(f'Gold: {self.gold} (of {inventory.gold})', self.get_difference_severity(inventory.gold, self.gold))
        console.log(f'Bank: {self.bank} (of {inventory.bank})', self.get_difference_severity(inventory.bank, self.bank))
        console.log(f'Normal Seeds: {self.basic} (of {inventory.basic})', self.get_difference_severity(inventory.basic, self.basic))
        console.log(f'Carrot Seeds: {self.carrot} (of {inventory.carrot})', self.get_difference_severity(inventory.carrot, self.carrot))
        console.log(f'Potato Seeds: {self.potato} (of {inventory.potato})', self.get_difference_severity(inventory.potato, self.potato))
        console.log(f'Bread Seeds: {self.bread} (of {inventory.bread})', self.get_difference_severity(inventory.bread, self.bread))
        console.log(f'Heal Potions: {self.heal_potions} (of {inventory.heal_potions})', self.get_difference_severity(inventory.heal_potions, self.heal_potions))
        console.log('There is more information about this last run in the logs folder.', bcolors.HEADER)
        console.separate()

    def get_difference_severity(before, after):
        return bcolors.OKGREEN if after > before else bcolors.FAIL
    