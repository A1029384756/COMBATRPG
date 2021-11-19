import os

terrainMappings = {'Giant Mushroom Forest':'gmf', 'Tornado-Ravaged Desert':'d', 'Forest':'f','Bleak Tundra':'t', 'Ancient Jungle':'j'}

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def drawWorld(world, player):
    for y in range(int(world.scale)):
        for x in range(int(world.scale)):
            if player.x == x and player.y == y:
                tile = "X"
            else:
                tile = terrainMappings[world.world_array[x][y]]
            tile = textSpacing(tile, 3)
            print(tile, end = " ")
        print()
    return 0

def textSpacing(text, maxLength):
    textLength = len(text)

    for i in range(maxLength - textLength):
        if (i % 2) != 0:
            text = ' ' + text
        else:
            text = text + ' '
    return text
