import pyxel
#from collision import in_collision, push_back

# アイテムクラス
class Item:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hit_area = (0, 0, 8, 8)    # 当たり判定の領域
        # アイテムリストに登録する
        game.items.append(self)

     # アイテムにダメージを与える
    def add_damage(self):
        player = self.game.player   # GAME内のplayerの情報にアクセス
        player.hp += 1              # HP回復
        print(player.hp)
        # アイテムをリストから削除する
        if self in self.game.items:    # アイテムリストに登録されている時
            self.game.items.remove(self)

    # アイテムを更新する
    def update(self):
        #空中に生成されたらy=100まで移動して停止
        if self.y < 100:
            self.y += 1

    # アイテムを描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 56, 32, 8, 8, 0)
