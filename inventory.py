from weapons import Sword, Club, Fists
from armor import Leather, HalfPlate
from consumables import HealthPotion, StrengthPotion, VampirismAntidote

def findInList(item, listOfItems):
  for i, sublist in enumerate(listOfItems):
    if item in sublist:
      return i
  return -1

weapons = {'sword' : Sword, 'club' : Club, 'fists' : Fists}
armors = {'leather' : Leather, 'half plate' : HalfPlate}
consumables = {'health potion' : HealthPotion,'strength potion' : StrengthPotion, 'vampirism antidote' : VampirismAntidote}

class Inventory(object):
    def __init__(self):
        self.equippedWeapon = Fists()
        self.equippedArmor = HalfPlate()
        self.weapons = [[" ", 0] for i in range(len(weapons))]
        self.armor = [[" ", 0] for i in range(len(armors))]
        self.consumables = [[" ", 0] for i in range(len(consumables))]

        for i, weapon in enumerate(weapons):
            self.weapons[i][0] = weapon

        for i, armor in enumerate(armors):
          self.armor[i][0] = armor

        for i, consumable in enumerate(consumables):
          self.consumables[i][0] = consumable

        self.finalAttackBonus = 0
        self.consumedItem = [None] * len(consumables)

    def displayWeapons(self):
        print("Weapons:")
        x = 0
        for i in range(len(self.armor)):
            if self.weapons[i][1] != 0:
                print(self.weapons[i][0] + "(x" + str(self.weapons[i][1]) + ")")
                x += 1
        if x == 0:
            print('You have no weapons in your inventory.')

        return x

    def displayArmor(self):
        print("Armor:")
        x = 0
        for i in range(len(self.armor)):
            if self.armor[i][1] != 0:
                print(self.armor[i][0] + "(x" + str(self.armor[i][1]) + ")")
                x += 1
        if x == 0:
            print('You have no armor in your inventory.')

        return x

    def displayConsumables(self):
        print("Consumables:")
        x = 0
        for i in range(len(self.consumables)):
            if self.consumables[i][1] != 0:
                print(self.consumables[i][0] + "(x" + str(self.consumables[i][1]) + ")")
                x += 1
        if x == 0:
            print('You have no consumables in your inventory.')

        return x

    def equipWeapon(self):
        hasWeapons = self.displayWeapons()

        if hasWeapons > 0:
            tmp = self.equippedWeapon

            selection = input("Select the weapon you would like to equip. ").lower()
            try:
                if self.weapons[findInList(selection, self.weapons)][1] > 0:
                    self.equippedWeapon = selection
                    self.weapons[findInList(selection, self.weapons)][1] -= 1

                    self.weapons[findInList(tmp, self.weapons)][1] += 1

                    print("You have equipped your " + selection + ".")
                    return
                else:
                    return
            except KeyError:
              print('Exiting inventory.')
              return
            except ValueError:
              print('Exiting inventory.')
              return

        else:
            print('Exiting inventory.')
            return

    def equipArmor(self):
        hasArmor = self.displayArmor()

        if hasArmor > 0:
            tmp = self.equippedArmor

            selection = input("Select the armor you would like to equip. ").lower()
            try:
                if self.armor[findInList(selection, self.armor)][1] > 0:
                    self.equippedArmor = selection
                    self.armor[findInList(selection, self.armor)][1] -= 1

                    self.armor[findInList(tmp, self.armor)][1] += 1

                    print("You have equipped your " + selection + ".")
                    return
                else:
                    return
            except KeyError:
                print("Exiting inventory.")
                return

        else:
            print('Exiting inventory.')

    def useConsumable(self):
        hasConsumable = self.displayConsumables()

        if hasConsumable > 0:
            selection = input("Select the consumable you would like to use. ").lower()
            flag = 0
            try:
                if self.consumables[findInList(selection, self.consumables)][1] > 0:
                    for slot in range(len(self.consumedItem)):
                        if self.consumedItem[slot] is None and flag == 0:
                            self.consumedItem[slot] = consumables[selection]()
                            flag = 1
                    self.consumables[findInList(selection, self.consumables)][1] -= 1
                    print('You have consumed a ' + selection + '.')
                    return
                else:
                    return

            except KeyError:
              print('Exiting inventory.')
              return

        else:
            print('Exiting inventory.')
            return

    def consumableEffect(self):
        potiontype = []
        bonusAmount = []
        for slot in range(len(self.consumedItem)):
            if self.consumedItem[slot] is None:
                potiontype.append(" ")
                bonusAmount.append(0)
            elif self.consumedItem[slot].duration > 0:
                self.consumedItem[slot].duration -= 1
                if self.consumedItem[slot].statBonus == "Health":
                    print('Health increased by ' + str(self.consumedItem[slot].bonusAmount) + '.')
                    potiontype.append("Health")
                    bonusAmount.append(self.consumedItem[slot].bonusAmount)
                elif self.consumedItem[slot].statBonus == "Strength":
                    print('Strength increased by ' + str(self.consumedItem[slot].bonusAmount) + '.')
                    potiontype.append("Strength")
                    bonusAmount.append(self.consumedItem[slot].bonusAmount)
                elif self.consumedItem[slot].statBonus == "Cure":
                    print('You are cured of your vampiritis.')
                    potiontype.append("Cure")
                    bonusAmount.append(self.consumedItem[slot].bonusAmount)
            else:
                self.consumedItem[slot] is None
                print('No Bonus')
                potiontype.append(" ")
                bonusAmount.append(0)

        return potiontype, bonusAmount
