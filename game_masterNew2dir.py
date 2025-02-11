#重力無し2Dact master
import pyxel

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
        pyxel.blt(0, 0, 1, 0, 0, 120, 160)

# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(120, 160, title="Mega Wing")
        # リソースファイルを読み込む
        pyxel.load("mega_wing.pyxres")
        # ゲームの状態を初期化する
        self.score = 0  # スコア
        self.background = None  # 背景
        # 背景を生成する(背景はシーンによらず常に存在する)
        Background(self)
        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # ゲーム全体を更新する
    def update(self):
        # 背景を更新する
        self.background.update()

    # ゲーム全体を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)

        # 背景を描画する
        self.background.draw()

        # スコアを描画する
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

# ゲームを生成して開始する
Game()
