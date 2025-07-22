import pyxel
#from collision import in_collision, push_back

# 爆弾クラス
class Bomb:
    #定数

    # 爆弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.isBomb = False             # 
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域

    # 爆弾にダメージを与える
    def add_damage(self):
        # 爆弾をリストから削除する
        if self in self.game.bombs:  # 爆弾リストに登録されている時
            self.game.bombs.remove(self)

    # 爆弾にダメージを与える
    def bomb_get(self):
        if self.isBomb == False:
            self.isBomb = True

    # 爆弾を更新するgame.
    def update(self):
        if self.isBomb == True:
            self.x = self.game.player.x
#            self.x = self.game.screen_x
            self.y = self.game.player.y + 8
#        print(self.x)

    # 爆弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 40, 8, 8, 0)
