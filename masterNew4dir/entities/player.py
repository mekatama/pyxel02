import pyxel
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_BOMB, TILE_SPIKE, TILE_WALL, TILE_ROAD
 
# プレイヤークラス
class Player:
    #定数
    MOVE_SPEED = 2          # 移動速度
    SHOT_INTERVAL = 20      # 弾の発射間隔
    HP = 3                  # 初期HP
    player_bullets = []     # 自機の弾のリスト
    player_bombs = []       # 自機の爆弾のリスト

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.dir = 1            # 1:right -1:left
        self.type = 0           # 0:横 1:上 2:下
        self.isBomb = False     # Bomb所持flag
        self.shot_timer = 0     # 弾発射までの残り時間
        self.hp = Player.HP     # HP
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # プレイヤーを更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
            self.dir = -1
            self.type = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED
            self.dir = 1
            self.type = 0
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= Player.MOVE_SPEED
            self.type = 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += Player.MOVE_SPEED
            self.type = 2
        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_DOWN):
            self.type = 0

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        # auto攻撃
        if self.shot_timer == 0:
            BulletPlayer(self.game, self.x, self.y, self.dir, self.type)
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

        # Sキー入力で爆弾発射
        if pyxel.btn(pyxel.KEY_S) and self.isBomb == True:
            BombPlayer(self.game, self.x, self.y)
            self.isBomb = False
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

# 弾クラス
class BulletPlayer:
    #定数
    SHOT_SPEED_X = 4        # shot speed x
    SHOT_SPEED_Y = 4        # shot speed y
    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dir, type):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
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
        # 弾の座標を更新する(type 0:横 1:上 2:下)
        if self.type == 0:
            self.x += BulletPlayer.SHOT_SPEED_X * self.dir
        elif self.type == 1:
            self.x += BulletPlayer.SHOT_SPEED_X * self.dir
            self.y -= BulletPlayer.SHOT_SPEED_Y
        elif self.type == 2:
            self.x += BulletPlayer.SHOT_SPEED_X * self.dir
            self.y += BulletPlayer.SHOT_SPEED_Y
        """
        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.player_bullets.remove(self)
        """
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)

# BOMBクラス
class BombPlayer:
    #定数

    # 爆弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hit_area = (2, 1, 5, 6)  # 当たり判定領域
        game.player_bombs.append(self)

    """
     # 爆弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
            self.game.player_bullets.remove(self)
    """

   # 爆弾を更新する
    def update(self):
        #生存時間カウント
#        self.life_time += 1
        # 弾の座標を更新する
#        self.x += 2
        self.y += 2
        print(self.y)
        
    # 爆弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)
