import random

class WorldSpace(object):
  worldBiomes = ['Giant Mushroom Forest', 'Tornado-Ravaged Desert', 'Forest','Bleak Tundra', 'Ancient Jungle']

  enemies = [' ', 'orc', 'goblin', 'dragon', 'vampire']

  consumables = [' ', 'health potion', 'vampirism antidote']


  def __init__(self, scale):
    self.scale = scale
    self.time = 0
    self.night = False

  def worldGen(self):
    self.world_array = [[0]*self.scale for i in range(self.scale)]
    self.enemy_array = [[0]*self.scale for i in range(self.scale)]
    self.drops_array = [[[0 for col in range(2)] for col in range(self.scale)] for row in range(self.scale)]

  def terrainGen(self):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        self.world_array[i][p] = random.randrange(100)
    self.terrainAssignment()

  def terrainAssignment(self):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        self.world_array[i][p] = self.worldBiomes[int(int(self.world_array[i][p])/20)]

  def enemyGeneration(self, player):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        if i == player.x and p == player.y:
          self.enemy_array[i][p] = 0
        else:
          self.enemy_array[i][p] = random.randrange(100)
    self.enemyAssignment()

  def enemyAssignment(self):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        if int(self.enemy_array[i][p]) > 98:
          self.enemy_array[i][p] = self.enemies[3]
        elif int(self.enemy_array[i][p]) > 88:
          self.enemy_array[i][p] = self.enemies[4]
        elif int(self.enemy_array[i][p]) > 78:
          self.enemy_array[i][p] = self.enemies[2]
        elif int(self.enemy_array[i][p]) > 50:
          self.enemy_array[i][p] = self.enemies[1]
        else:
          self.enemy_array[i][p] = self.enemies[0]

  def consumablesGen(self):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        for j in range(2):
          self.drops_array[i][p][1] = random.randrange(100)
    self.consumablesAssignment()

  def consumablesAssignment(self):
    for i in range(int(self.scale)):
      for p in range(int(self.scale)):
        for j in range(2):
            if int(self.drops_array[i][p][j]) > 90:
                self.drops_array[i][p][j] = self.consumables[2]
            elif int(self.drops_array[i][p][j]) > 70:
                self.drops_array[i][p][j] = self.consumables[1]
            else:
                self.drops_array[i][p][j] = self.consumables[0]

  def getTerrain(self, player):
    return self.world_array[player.x][player.y]

  def getEnemy(self, player):
    return self.enemy_array[player.x][player.y]

  def clearEnemy(self, player):
    self.enemy_array[player.x][player.y] = ' '
    return

    def timeOfDay(self):
        self.time += 1
        if self.time == 12:
            print('Night has fallen, be prepared.')
            self.night = True

        if self.time == 24:
            print("Day has arrived.")
            self.night = False
            self.time = 0
