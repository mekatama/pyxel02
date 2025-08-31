import pyxel

# 弾クラス
class Enemy_Bullet:
    #定数

    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.life_time = 0  #生存時間
        self.hit_area = (2, 1, 5, 6)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self in self.game.enemy_bullets:    # 自機の弾リストに登録されている時
            self.game.enemy_bullets.remove(self)

   # 弾を更新する
    def update(self):

        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する
        self.x += 2
#        self.y += 2

        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.enemy_bullets.remove(self)
        
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)
