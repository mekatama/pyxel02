#格闘アクション
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
    MOVE_SPEED = 2      # 移動速度
    SHOT_INTERVAL = 6   # 弾の発射間隔

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game    # ゲームへの参照
        self.x = x          # X座標
        self.y = y          # Y座標
        self.direction = 1  # 1:右向き -1:左向き
        self.shot_timer = 0 # 弾発射までの残り時間
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 
        # ゲームに自機を登録する
        self.game.player = self

    # 自機を更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
            self.direction = -1 #左向き
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED
            self.direction = 1  #右向き

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

    # 自機を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)

# 敵クラス
class Enemy:
    #定数
    KIND_A = 0  # 敵A
    KIND_B = 1  # 敵B
    KIND_C = 2  # 敵C

    # 敵を初期化してゲームに登録する
    def __init__(self, game, kind, level, x, y):
        self.game = game
        self.kind = kind                # 敵の種類
        self.level = level              # 強さ
        self.x = x
        self.y = y
        self.life_time = 0              # 生存時間
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域
        self.armor = self.level - 1     # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        # ゲームの敵リストに登録する
        self.game.enemies.append(self)

    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.life_time += 1

        # 敵Aを更新する
        if self.kind == Enemy.KIND_A:
            pass

        # 敵Bを更新する
        elif self.kind == Enemy.KIND_B:
            pass

        # 敵Cを更新する
        elif self.kind == Enemy.KIND_C:
            pass

    # 敵を描画する
    def draw(self):
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 8, 0, 8, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 8, 0, 8, 8, 0)

# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    #定数
    SCENE_TITLE = 0     # タイトル画面
    SCENE_PLAY = 1      # プレイ画面
    SCENE_GAMEOVER = 2  # ゲームオーバー画面

    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(128, 128, title="Mega Wing")
        # リソースファイルを読み込む
        pyxel.load("mega_wing.pyxres")
        # ゲームの状態を初期化する
        self.score = 0          # スコア
        self.scene = None       # 現在のシーン
        self.background = None  # 背景
        self.player = None      # 自機
        self.enemies = []       # 敵のリスト

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
            # 全ての弾と敵を削除する
            self.enemies.clear()

        # プレイ画面
        elif self.scene == Game.SCENE_PLAY:
            # プレイ状態を初期化する
            self.score = 0      # スコアを0に戻す
            # 自機を生成する
            Player(self, 56, 100)
            #仮の敵を生成する
            kind = pyxel.rndi(Enemy.KIND_A, Enemy.KIND_C)
            Enemy(self, kind, 1, pyxel.rndi(0, 112), 40)


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

        # 敵を更新する
        # ループ中に要素の追加・削除が行われても問題ないようにコピーしたリストを使用する
        for enemy in self.enemies.copy():
            enemy.update()

        # シーンを更新する
        if self.scene == Game.SCENE_TITLE:  # タイトル画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.change_scene(Game.SCENE_PLAY)
        elif self.scene == Game.SCENE_PLAY:  # プレイ画面
            # 敵を出現させる予定
            pass
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

        # 敵を描画する
        for enemy in self.enemies:
            enemy.draw()

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
