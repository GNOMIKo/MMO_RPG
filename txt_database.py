class txt_database:
    def read(self):
        self.mass = []
        with open('base.txt', 'r+') as txt:
            self.mass = [line.strip() for line in txt]
        self.username = self.mass[0]
        self.lvl = int(self.mass[1])
        self.gold = int(self.mass[2])
        self.damage = int(self.mass[3])
        self.health = int(self.mass[4])
        #print("DEVELOPER:",self.username, self.lvl, self.gold, self.damage)
        #print("DEVELOPER:",self.mass)

    def write(self):
        self.mass[0] = self.username
        self.mass[1] = self.lvl
        self.mass[2] = self.gold
        self.mass[3] = self.damage
        self.mass[4] = self.health
        with open('base.txt', 'w') as txt:
            for i in self.mass:
                txt.write(str(i) + '\n')

def printd(string):
    print(f'\033[1;32m!!!DevInfo!!!\n{string}\n!!!DevInfo!!!\033[0m')  # Green text