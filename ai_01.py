import pyxel

# ゲーム画面のサイズを設定
WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120

class Game:
    def __init__(self):
        # Pyxelを初期化
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Shoot the Cursor")

        # 弾の速度を設定
        self.bullet_speed = 5

        # グラフィックを読み込む
        pyxel.load("my_resource.pyxres")

        # カーソルの初期位置を設定
        self.cursor_x = WINDOW_WIDTH // 2
        self.cursor_y = WINDOW_HEIGHT // 2

        # 弾の初期位置を設定
        self.bullet_x = -1
        self.bullet_y = -1

        pyxel.run(self.update, self.draw)

    def update(self):
        # カーソルの位置を更新
        self.cursor_x = pyxel.mouse_x
        self.cursor_y = pyxel.mouse_y

        # スペースキーが押されたら弾を発射
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bullet_x = self.cursor_x
            self.bullet_y = self.cursor_y

        # 弾の位置を更新
        if self.bullet_y >= 0:
            self.bullet_y -= self.bullet_speed

    def draw(self):
        # 画面をクリア
        pyxel.cls(0)

        # カーソルを描画
        pyxel.blt(self.cursor_x, self.cursor_y, 0, 0, 0, 8, 8, 0)

        # 弾を描画
        if self.bullet_y >= 0:
            pyxel.blt(self.bullet_x, self.bullet_y, 0, 8, 0, 8, 8, 0)

# ゲームを開始
Game()