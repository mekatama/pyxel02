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

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.shot_timer = 0     # 弾発射までの残り時間
        self.hp = Player.HP     # HP
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 

    """
    # 自機にダメージを与える
    def add_damage(self):
        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)
        # BGMを止めて爆発音を再生する
        pyxel.stop()
        pyxel.play(0, 2)
        # 自機を削除する
        self.game.player = None
        # シーンをゲームオーバー画面に変更する
        self.game.change_scene("gameover")
    """

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

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        """
        # 弾を発射する
        if pyxel.btn(pyxel.KEY_SPACE) and self.shot_timer == 0:
            # 自機の弾を生成する(右方向は0度)
            Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 8, self.y, 0, 5)
            # 弾発射音を再生する
            pyxel.play(3, 0)
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL
        """
    # プレイヤーを描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8, 8, 0)
        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)

    """
    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game  # ゲームクラス
        self.x = x  # X座標
        self.y = y  # Y座標
        self.dx = 0  # X軸方向の移動距離
        self.dy = 0  # Y軸方向の移動距離
        self.direction = 1  # 左右の移動方向
        self.jump_counter = 0  # ジャンプ時間

    # プレイヤーを更新する
    def update(self):
        # キー入力に応じて左右に移動する
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
        ):  # 左キーまたはゲームパッド左ボタンが押されている時
            self.dx = -2
            self.direction = -1

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
        ):  # 右キーまたはゲームパッド右ボタンが押されている時
            self.dx = 2
            self.direction = 1

        # 下方向に加速する
        if self.jump_counter > 0:  # ジャンプ中
            self.jump_counter -= 1  # ジャンプ時間を減らす
        else:  # ジャンプしていない時
            self.dy = min(self.dy + 1, 4)  # 下方向に加速する

        # タイルとの接触処理
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
                    pyxel.play(3, 1)

                if self.dy >= 0 and tile_type == TILE_MUSHROOM:  # キノコに触れた時
                    # ジャンプの距離を設定する
                    self.dy = -6
                    self.jump_counter = 6

                    # 効果音を再生する
                    pyxel.play(3, 2)

                if tile_type == TILE_EXIT:  # 出口に到達した時
                    self.game.change_scene("clear")
                    return

                if tile_type in [TILE_SPIKE, TILE_LAVA]:  # トゲ又は溶岩に触れた時
                    self.game.change_scene("gameover")
                    return

        # ジャンプする
        if (
            self.dy >= 0
            and (
                in_collision(self.x, self.y + 8) or in_collision(self.x + 7, self.y + 8)
            )
            and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B))
        ):
            # 上昇中ではなく、プレイヤーの左下又は右下が床に接している状態で
            # スペースキーまたはゲームパッドのBボタンが押された時
            self.dy = -6
            self.jump_counter = 2
            pyxel.play(3, 0)

        # 押し戻し処理
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy)

        # 横方向の移動を減速する
        self.dx = int(self.dx * 0.8)

    # プレイヤーを描画する
    def draw(self):
        # 画像の参照X座標を決める
        u = pyxel.frame_count // 4 % 2 * 8 + 8
        # 4フレーム周期で0と8を交互に繰り返す

        # 画像の幅を決める
        w = 8 if self.direction > 0 else -8
        # 移動方向が正の場合は8にしてそのまま描画、負の場合は-8にして左右反転させる

        # 画像を描画する
        pyxel.blt(self.x, self.y, 0, u, 64, w, 8, 15)
    """