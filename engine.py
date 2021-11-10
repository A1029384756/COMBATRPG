import os

terrainMappings = {'Giant Mushroom Forest':'gmf', 'Tornado-Ravaged Desert':'d', 'Forest':'f','Bleak Tundra':'t', 'Ancient Jungle':'j'}

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def drawWorld(world, player):
    for i in range(int(world.scale)):
        for j in range(int(world.scale)):
            terrain = terrainMappings[world.world_array[i][j]]
            terrain = textSpacing(terrain, 3)
            print(terrain, end = " ")
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
