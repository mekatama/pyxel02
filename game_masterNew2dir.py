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
        # タイトル画面以外で背景画像を描画する
        if self.game.scene != Game.SCENE_TITLE:
            pyxel.blt(0, 0, 1, 0, 0, 120, 160)

# 自機クラス
class Player:
    #定数
    MOVE_SPEED = 2  # 移動速度

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game    # ゲームへの参照
        self.x = x          # X座標
        self.y = y          # Y座標
        # ゲームに自機を登録する
        self.game.player = self

    # 自機を更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う

    # 自機を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)

# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    #定数
    SCENE_TITLE = 0     # タイトル画面
    SCENE_PLAY = 1      # プレイ画面
    SCENE_GAMEOVER = 2  # ゲームオーバー画面

    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(120, 160, title="Mega Wing")
        # リソースファイルを読み込む
        pyxel.load("mega_wing.pyxres")
        # ゲームの状態を初期化する
        self.score = 0          # スコア
        self.scene = None       # 現在のシーン
        self.background = None  # 背景

        # 背景を生成する(背景はシーンによらず常に存在する)
        Background(self)
        # シーンをタイトル画面に変更する
        self.change_scene(Game.SCENE_TITLE)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する関数
    def change_scene(self, scene):
        self.scene = scene

        # タイトル画面
        if self.scene == Game.SCENE_TITLE:
            # 自機を削除する
            self.player = None  # プレイヤーを削除
            # BGMを再生する
            pyxel.playm(0, loop=True)
        # プレイ画面
        elif self.scene == Game.SCENE_PLAY:
            # プレイ状態を初期化する
            self.score = 0  # スコアを0に戻す
            # BGMを再生する
            pyxel.playm(1, loop=True)
            # 自機を生成する
            Player(self, 56, 140)
        # ゲームオーバー画面
        elif self.scene == Game.SCENE_GAMEOVER:
            # 画面表示時間を設定する
            self.display_timer = 60
            # 自機を削除する
            self.player = None  # プレイヤーを削除

    # ゲーム全体を更新する
    def update(self):
        # 背景を更新する
        self.background.update()

        # 自機を更新する
        if self.player is not None: #NONE使用時は判定方法が特殊
            self.player.update()

        # シーンを更新する
        if self.scene == Game.SCENE_TITLE:  # タイトル画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                pyxel.stop()  # BGMの再生を止める
                self.change_scene(Game.SCENE_PLAY)

        elif self.scene == Game.SCENE_PLAY:  # プレイ画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.change_scene(Game.SCENE_GAMEOVER)

        elif self.scene == Game.SCENE_GAMEOVER:  # ゲームオーバー画面
            if self.display_timer > 0:  # 画面表示時間が残っている時
                self.display_timer -= 1
            else:                       # 画面表示時間が0になった時
                self.change_scene(Game.SCENE_TITLE)

    # ゲーム全体を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)

        # 背景を描画する
        self.background.draw()

        # 自機を描画する
        if self.player is not None:
            self.player.draw()

        # スコアを描画する
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        # シーンを描画する
        if self.scene == Game.SCENE_TITLE:      # タイトル画面
            pyxel.blt(0, 18, 2, 0, 0, 120, 120, 15)
            pyxel.text(31, 148, "- PRESS ENTER -", 6)
        elif self.scene == Game.SCENE_GAMEOVER: # ゲームオーバー画面
            pyxel.text(43, 78, "GAME OVER", 8)

# ゲームを生成して開始する
Game()
