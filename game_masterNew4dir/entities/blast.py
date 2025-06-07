import pyxel
#from collision import in_collision, push_back

# 爆発エフェクトクラス
class Blast:
    #定数
    START_RADIUS = 1    # 開始時の半径
    END_RADIUS = 8      # 終了時の半径

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = Blast.START_RADIUS  # 爆発の半径
        # ゲームの爆発エフェクトリストに登録する
        game.blasts.append(self)

    # 爆発エフェクトを更新する
    def update(self):
        # 半径を大きくする
        self.radius += 1
        # 半径が最大になったら爆発エフェクトリストから登録を削除する
        if self.radius > Blast.END_RADIUS:
            self.game.blasts.remove(self)

    # 爆発エフェクトを描画する
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)

