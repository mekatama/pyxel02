import pyxel
"""
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_LAVA, TILE_MUSHROOM, TILE_SPIKE
"""

# プレイヤークラス
class Player:
    #定数
    MOVE_SPEED = 2          # 移動速度
    SHOT_INTERVAL = 10      # 弾の発射間隔
    HP = 3                  # 初期HP
    player_bullets = []     # 自機の弾のリスト

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.shot_timer = 0     # 弾発射までの残り時間
        self.hp = Player.HP     # HP
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # プレイヤーを更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += Player.MOVE_SPEED

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        # Aキー入力で攻撃
        if pyxel.btn(pyxel.KEY_A) and self.shot_timer == 0:
            BulletPlayer(self.game, self.x, self.y)
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う

    # プレイヤーを描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8, 8, 0)
        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)

# 弾クラス
class BulletPlayer:
    #定数

    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.life_time = 0  #生存時間
        self.hit_area = (2, 1, 5, 6)  # 当たり判定領域
        game.player_bullets.append(self)

     # 弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
            self.game.player_bullets.remove(self)

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
            self.game.player_bullets.remove(self)
        
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)
