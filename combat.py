from enemy import Orc, Goblin, Dragon, Vampire
import random

enemies = {'orc' : Orc, 'goblin' : Goblin, 'dragon' : Dragon, 'vampire' : Vampire}

def combatLoop(type, player, world):
    enemy = enemies[type]()
    playerTurn = player.dexterity > enemy.dexterity
    while enemy.health > 0 and player.health > 0:
        playerTurn = combatOrder(playerTurn, player, enemy, type)

        if enemy.health <= 0:
            print('You won!')
            world.drops_array[player.x][player.y][0] = enemy.dropItem()
            return 1

        elif player.health <= 0:
            print('You lost!')
            return 0

        elif playerTurn == -1:
            return -1

def combatOrder(playerTurn, player, enemy, type):
    if playerTurn == 1:

        playerTurn = 0

        if player.health > 0:
            attackStat, damage = player.attack()
            if attackStat >= enemy.armorClass:
              print('You hit.')
              enemy.health -= damage
              return playerTurn


            elif attackStat == 0:
                return playerTurn

            elif attackStat == -1:
                playerEscape = random.randrange(0,20) + player.dexterity
                enemyCatch = random.randrange(0,20) + enemy.dexterity
                if playerEscape > enemyCatch:
                    print('You managed to escape!')
                    playerTurn = -1
                    return playerTurn
                else:
                    print('The ' + type + ' managed to catch up.')
                    return playerTurn

            else:
              print('You miss.')

        else:
            return playerTurn

    else:
        playerTurn = 1

        if enemy.health > 0:
            attackStat, damage = enemy.attack(player)
            if attackStat >= player.armorClass:
                print("The " + type + " hits.")
                player.health -= damage
                player.inventory.equippedArmor.durability -= int(damage * 0.166)
                if player.inventory.equippedArmor.durability <= 0:
                    player.inventory.equippedArmor = None

            elif attackStat == 0:
                return playerTurn

            else:
              print("The " + type + " misses.")
              return playerTurn

        elif playerTurn == 0:
            return playerTurn

    return playerTurn
