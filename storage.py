import console
from console import bcolors
from log import Log
import atexit

class Storage:
    def __init__(self, gold, bank, normal_seeds, carrot_seeds, potato_seeds, bread_seeds, heal_potions):
        self.gold = gold
        self.bank = bank
        self.normal_seeds = normal_seeds
        self.carrot_seeds = carrot_seeds
        self.bread_seeds = bread_seeds
        self.potato_seeds = potato_seeds
        self.heal_potions = heal_potions
        self.logs = Log(self)
        atexit.register(self.logs.print, args=self)


    def add(self, field, amount = 1):
        if hasattr(self, field):
            setattr(self, field, getattr(self, field) + amount)
        else:
            console.log('Error: Invalid field name while using storage', bcolors.FAIL)

    def get(self, field):
        if field == 'nothing':
            return 1

        if hasattr(self, field):
            return getattr(self, field)
        else:
            console.log(f'Error: Trying to consume an empty resource ({field})', bcolors.FAIL)
            return -1

    def remove(self, field, amount = 1):
        if field == 'nothing':
            return

        setattr(self, field, getattr(self, field) - amount)
        console.log(f"Consumed {field}")

    def get_balance(self):
        bank = self.get('bank')
        gold = self.get('gold')
        return bank + gold

