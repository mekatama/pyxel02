import pyxel

# 爆弾クラス
class Bomb:
    #定数

    # 爆弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域

    """
    # 爆弾にダメージを与える
    def add_damage(self):
        # 爆弾をリストから削除する
        if self in self.game.bombs:  # 爆弾リストに登録されている時
            self.game.bombs.remove(self)
    """
    # 爆弾を更新するgame.
    def update(self):
        #生存時間カウント
#        self.life_time += 1
        # 弾の座標を更新する
#        self.x += 2
        self.y += 2

    # 爆弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 40, 40, 8, 8, 0)
