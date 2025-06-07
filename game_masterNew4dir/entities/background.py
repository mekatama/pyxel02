import pyxel
#from collision import in_collision, push_back

# 背景クラス
class Background:
    # 背景を初期化してゲームに登録する
    def __init__(self, game):
        self.game = game  # ゲームへの参照
        # ゲームに背景を登録する()
        self.game.background = self

    # 背景を更新する
    def update(self):
        pass

    # 背景を描画する
    def draw(self):
        pyxel.blt(0, 0, 2, 0, 0, 128, 128)
        # タイトル画面以外で背景画像を描画する
#        if self.game.scene != Game.SCENE_TITLE:
#            pyxel.blt(0, 0, 2, 0, 0, 128, 128)
