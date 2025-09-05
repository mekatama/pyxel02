import pyxel

#■ParticleHit
class ParticleHit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0
        self.is_alive = True
    def update(self):
        self.count += 1
        if self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.circb(self.x, self.y, 2, 7)
