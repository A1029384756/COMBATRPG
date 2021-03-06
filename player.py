import random
import engine
from inventory import Inventory

class Player(object):
    def __init__(self, x, y, playerMaxDist):
      #Location and movment
      self.x = x
      self.y = y
      self.directions = dict(w=(0,-1), s=(0,1), d=(1,0), a=(-1,0))
      self.playerMaxDist = playerMaxDist

      #Stats
      self.maxHealth = 35
      self.maxStamina = 10
      self.dexterity = 3
      self.strength = 6
      self.armorClass = 10 + self.dexterity

      #Placeholder Stats
      self.health = self.maxHealth
      self.stamina = self.maxStamina

      #Conditions
      self.burning = False
      self.burnDuration = 0
      self.paralyzed = False
      self.paralyzeDuration = 0
      self.infected = False
      self.infectedDuration = 0
      self.persistentPoisoned = False
      self.persistentPoisonDuration = 0

      self.inventory = Inventory()

      self.counter = 0

    def movement(self):
        self.counter += 1
        self.applyPotions()

        self.statusEffects(1)

        print('W. | North')
        print('S. | South')
        print('D. | East')
        print('A. | West')
        movementInput = input("Input the direction you would like to travel. ").lower()
        #Compare it to the dictionary of moves
        if movementInput in self.directions:
            #Move
            direction = self.directions[movementInput]
            self.x, self.y = self.x + direction[0], self.y + direction[1]
            self.worldBounds()
        else:
            #Return exception
            print('Invalid Input')

    def worldBounds(self):
        if self.x >= self.playerMaxDist:
            self.x = self.playerMaxDist - 1
            print("You have gone too far, turning you around.")
        if self.x < 0:
            self.x = 0
            print("You have gone too far, turning you around.")
        if self.y >= self.playerMaxDist:
            self.y = self.playerMaxDist - 1
            print("You have gone too far, turning you around.")
        if self.y < 0:
            self.y = 0
            print("You have gone too far, turning you around.")

    def attack(self):
        #engine.clearScreen()
        self.armorClass = 10 + self.dexterity
        self.armorClass = self.inventory.equippedArmor.modifier + self.armorClass
        #Apply Conditions
        self.applyPotions()

        self.statusEffects(0)

        if self.paralyzed:
            return 0,0

        self.displayStats()

        print('1. Light Attack')
        print('2. Heavy Attack')
        print('3. Rest')
        print('4. Use Potion')
        print('5. Run Away')
        attacktype = input('Input the attack you would like to make. ').lower()
        if attacktype == '1' or attacktype == 'light' or attacktype == 'light attack':
            if self.stamina >= 1:
                print('You light attack.')
                self.stamina -= 1
                return random.randrange(1, 20) + (self.strength/2), random.randrange(1, 8) + (self.strength/2) + self.inventory.finalAttackBonus
            else:
                print('Not enough stamina! You rest.')
                self.stamina += 1
                return 0,0
        if attacktype == '2' or attacktype == 'heavy' or attacktype == 'heavy attack':
            if self.stamina >= 2:
                print('You heavy attack.')
                self.stamina -= 2
                return random.randrange(1, 20) + (self.strength/2), random.randrange(1, 8) + (self.strength) + self.inventory.finalAttackBonus
            else:
                print('Not enough stamina! You rest.')
                self.stamina += 1
                return 0, 0
        if attacktype == '3' or attacktype == 'rest':
            print('You rest.')
            self.stamina += 2
            if self.stamina > self.maxStamina:
                self.stamina = self.maxStamina
                print('Stamina at max.')
            return 0, 0
        if attacktype == '4' or attacktype == 'potion' or attacktype == 'use potion':
            self.inventory.useConsumable()
            return 0, 0
        if attacktype == '5' or attacktype == 'run' or attacktype == 'run away':
            if self.stamina >= 4:
                self.stamina -= 4
                print('You try to run away and...')
                return -1, 0
            else:
                self.stamina += 1
                print("Not enough stamina, you decide to rest.")
                return 0, 0

        else:
            print('Invalid input.')
            return self.attack()

    def statusEffects(self, type):
        if type == 0: #Combat statusEffect
            if self.burning:
                if self.burnDuration > 0:
                    self.health -= 5
                    self.burnDuration -= 1
                    print("You take 5 points of fire damage.")
                else:
                    self.burning = False

            if self.paralyzed:
                if self.paralyzeDuration <= 0:
                    self.paralyzed = False
                    print("You are paralyzed and cannot move.")
                else:
                    self.paralyzeDuration -= 1

        if type == 1: #Movement statusEffect
            if self.infectedDuration <= 0:
                self.infected = False
            else:
                self.infectedDuration -= 1
                print("You have " + str(self.infectedDuration) + " days until you succumb to vampiritis.")

        if self.persistentPoisoned:
            if self.persistentPoisonDuration <= 0:
                self.persistentPoisoned = False
            else:
                self.health -= 5
                self.persistentPoisonDuration -= 1
                print("You take 5 points of poison damage.")

    def decision(self):
        print("1. Move")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Use Consumable")
        print("5. View Stats")
        selection = input('What would you like to do? ').lower()

        if selection == '1' or selection == 'move':
            self.movement()

        elif selection == '2' or selection == 'equip weapon':
            self.inventory.equipWeapon()

        elif selection == '3' or selection == 'equip armor':
            self.inventory.equipArmor()

        elif selection == '4' or selection == 'use consumable':
            self.inventory.useConsumable()

        elif selection == '5' or selection == 'view stats':
            engine.clearScreen()
            self.displayStats()

        else:
            print('Invalid input')

    def getDrops(self, world):
      return world.drops_array[self.x][self.y][0], world.drops_array[self.x][self.y][1]

    def pickupDrops(self, world, itemType):
        droppedItem = world.drops_array[self.x][self.y][itemType]
        if droppedItem == ' ':
            return
        print('You found a ' + droppedItem + '.')
        playerChoice = input('Would you like to pick it up? ').lower()
        if playerChoice == 'yes':
            if itemType == 0:
                for i in range(len(self.inventory.weapons)):
                    if self.inventory.weapons[i][0] == droppedItem:
                        self.inventory.weapons[i][1] += 1
            elif itemType == 1:
                for i in range(len(self.inventory.consumables)):
                    if self.inventory.consumables[i][0] == droppedItem:
                        self.inventory.consumables[i][1] += 1
            print('You picked up the ' + droppedItem + '.')
            world.drops_array[self.x][self.y][itemType] = ' '
            return
        elif playerChoice == 'no':
            print('You decided to move on.')
            return
        else:
            print('Invalid input.')

    def applyPotions(self):
        potiontype, bonusAmount = self.inventory.consumableEffect()
        for i in range(len(potiontype)):
            if potiontype[i] == "Health":
                self.health += bonusAmount[i]
                if self.health > self.maxHealth:
                    self.health = self.maxHealth
                print("Your health: " + str(self.health))
            elif potiontype[i] == "Cure":
                self.infected = False
                self.infectedDuration = 0
                print("You are cured of vampirism.")
            elif potiontype[i] == "Strength":
                self.strength += bonusAmount[i]
                print("Your strength: " + str(self.strength))

    def displayStats(self):
        print("Stats:")
        print("Health: " + str(self.health))
        print("Stamina: " + str(self.stamina))
        print("Dexterity: " + str(self.dexterity))
        print()
        input()
