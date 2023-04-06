import pyxel

# ゲームウィンドウの大きさを定義
WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120

class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = [0, 0]
        # マウスの位置を取得
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y

    def update(self):

        # 弾の移動方向を計算
        dx = self.mouse_x - self.x
        dy = self.mouse_y - self.y
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            self.direction[0] = dx / length
            self.direction[1] = dy / length

        # 弾を移動させる
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw(self):
        pyxel.circ(self.x, self.y, 2, 8)

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Pyxel Bullet Example")
        self.bullets = []

        # マウスカーソルを非表示にする
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        # スペースキーが押されたら新しい弾を発射する
        if pyxel.btnp(pyxel.KEY_SPACE):
            x = WINDOW_WIDTH // 2
            y = WINDOW_HEIGHT // 2
            speed = 2
            self.bullets.append(Bullet(x, y, speed))

        # すべての弾を更新する
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        pyxel.cls(0)

        # すべての弾を描画する
        for bullet in self.bullets:
            bullet.draw()

App()