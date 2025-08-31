import pyxel
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_BOMB, TILE_SPIKE, TILE_WALL, TILE_ROAD

from .bomb import Bomb                  # ボムクラス
from .player_bullet import PlayerBullet # playerのBulletクラス 

# プレイヤークラス
class Player:
    #定数
    MOVE_SPEED = 2          # 移動速度
    DASH_SPEED = 10         # 特殊移動速度
    SHOT_INTERVAL = 20      # 弾の発射間隔
    DASH_INTERVAL = 2       # dash間隔
    HP = 3                  # 初期HP

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.dir = 1            # 1:right -1:left
        self.type = 0           # 0:横 1:上 2:下
        self.isBomb = False     # Bomb所持flag
        self.isDash = False     # Dash flag
        self.isDashInput = False# Dash入力 flag
        self.shot_timer = 0     # 弾発射までの残り時間
        self.dash_timer = 0     # dash時間
        self.hp = Player.HP     # HP
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # プレイヤーを更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.isDash == False:
                self.x -= Player.MOVE_SPEED
            else:
                self.x -= Player.DASH_SPEED
            self.dir = -1
            self.type = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.isDash == False:
                self.x += Player.MOVE_SPEED
            else:
                self.x += Player.DASH_SPEED
            self.dir = 1
            self.type = 0
        if pyxel.btn(pyxel.KEY_UP):
            if self.isDash == False:
                self.y -= Player.MOVE_SPEED
            else:
                self.y -= Player.DASH_SPEED
            self.type = 1
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.isDash == False:
                self.y += Player.MOVE_SPEED
            else:
                self.y += Player.DASH_SPEED
            self.type = 2
        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_DOWN):
            self.type = 0

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1
        
        # dash時間の制御
        if self.dash_timer > 0:
            self.dash_timer -= 1
        else:
            self.isDash = False
        
        # dash入力の制御
        if self.dash_timer > -15:
            self.dash_timer -= 1
        else:
            self.isDashInput = False

        # auto攻撃
        if self.shot_timer == 0:
            self.game.player_bullets.append(
                PlayerBullet(self.game, self.x, self.y, self.dir, self.type)
            )
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

        # 爆弾所持で、Sキー入力で爆弾発射
        if pyxel.btnp(pyxel.KEY_S) and self.isBomb == True:
            self.game.bombs.append(
                Bomb(self.game, self.x, self.y)
            )
            self.isBomb = False
        # 爆弾未所持で、Sキー入力で特殊移動
        if pyxel.btnp(pyxel.KEY_S) and self.isBomb == False:
            if self.isDashInput == False:
                self.isDash = True
                self.isDashInput = True
                self.dash_timer = Player.DASH_INTERVAL

        # test、Dキー入力で爆弾発射
        if pyxel.btnp(pyxel.KEY_D):
            print("d push")
            self.game.player_bullets.append(
                PlayerBullet(self.game, self.x, self.y, self.dir, self.type)
            )

        """
        # 自機が画面外に出ないようにする(一画面用)
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う
        """
        # タイルとの当たり判定
        for i in [1, 6]:
            for j in [1, 6]:
                x = self.x + j
                y = self.y + i
                tile_type = get_tile_type(x, y)

                if tile_type == TILE_GEM:  # 宝石に触れた時
                    # スコアを加算する
                    self.game.score += 10
                    # 宝石タイルを消す
                    pyxel.tilemaps[0].pset(x // 8, y // 8, (0, 0))
                    # 効果音を再生する
#                    pyxel.play(3, 1)

                if tile_type == TILE_BOMB:  # BOMBに触れた時
                    self.isBomb = True
                    # タイルを消す
                    pyxel.tilemaps[0].pset(x // 8, y // 8, (0, 0))

#                if tile_type == TILE_EXIT:  # 出口に到達した時
#                    self.game.change_scene("clear")
#                    return

                if tile_type == TILE_ROAD:  # 滑走路に触れた時
                    print("kaifuku")
                    return

                if tile_type == TILE_SPIKE:  # トゲ又に触れた時
                    self.game.change_scene("gameover")
                    return

                if tile_type == TILE_WALL:  # 壁に触れた時
                    self.game.change_scene("gameover")
                    return

    # プレイヤーを描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8 * self.dir, 8, 0)
        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)
