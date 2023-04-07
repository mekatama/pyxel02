#画面中央からSTG
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
BULLET_SPEED = 2
ENEMY_SPEED = 1.5
#list用意
enemies = []
enemiesUI = []
bullets = []
blasts = []

#関数(List実行)
def update_list(list):
    for elem in list:
        elem.update()   #listの各要素に対してupdate()実行
#関数(List描画)
def draw_list(list):
    for elem in list:
        elem.draw()     #listの各要素に対してdraw()実行
#関数(List更新)
def cleanup_list(list):
    i = 0
    while i < len(list):        #listに要素が入っている間loops
        elem = list[i]          #要素取得
        if not elem.is_alive:   #死亡の場合
            list.pop(i)         #要素削除
        else:                   #生存の場合
            i += 1              #スルー

#■Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 3
        self.is_alive = True
    def update(self):
        # スペースキーが押されたら新しい弾を発射する
        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(WINDOW_W // 2, WINDOW_H // 2, BULLET_SPEED)
    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        #当たり判定
        pyxel.rectb(self.x, self.y, 16, 16, 10)

#■Bullet
class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = [0, 0]
        self.is_alive = True
        self.count = 0
        # マウスの位置を取得
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        # 弾の移動方向を計算
        dx = self.mouse_x - self.x
        dy = self.mouse_y - self.y
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            self.direction[0] = dx / length
            self.direction[1] = dy / length
        bullets.append(self)
    def update(self):
        self.count += 1
        # 弾を移動させる
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        if self.count >= 50: #一定時間表示
            self.is_alive = False       #消去
    def draw(self):
        pyxel.circ(self.x, self.y, 2, 8)

#■Enemy
class Enemy:
    def __init__(self, x, y, hp, img, speed):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.addSpeed = speed   #追加speed
        self.direction = [0, 0]
        self.is_alive = True
        # 敵の移動方向を計算
        dx = WINDOW_W / 2 - self.x
        dy = WINDOW_H / 2 - self.y
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            self.direction[0] = dx / length
            self.direction[1] = dy / length
        enemies.append(self)
    def update(self):
        #移動
        self.x += self.direction[0] * self.addSpeed
        self.y += self.direction[1] * self.addSpeed
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 0)
        #当たり判定
        pyxel.rectb(self.x + 2, self.y,12, 16, 10)

#■Enemy_UI
class EnemyUI:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.count = 0
        self.is_alive = True
        enemiesUI.append(self)
    def update(self):
        self.count += 1
        if self.count < 10:
            self.y -= 1
        elif self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", 13)

#■Blust
class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
        elif self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 32 + (16 * self.motion), 16, 16, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pysel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        # マウスカーソル表示
        pyxel.mouse(True)
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 -8, pyxel.height / 2 -8)
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新関数
    def update(self):
        #処理の画面分岐
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        pass

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    #ゲーム画面処理用update
    def update_play_scene(self):
        #一定時間でenemy出現判定
        if pyxel.frame_count % 60 == 0:
            #enemy生成
            Enemy(100, 20, 1, 1, 1)
        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x + 16    > bullet.x and
                    enemy.x         < bullet.x + 2 and
                    enemy.y + 16    > bullet.y and
                    enemy.y         < bullet.y + 2):
                    #Hit時の処理
                    enemy.hp -= 1
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        self.score += 10
                        pyxel.play(1, 0, loop=False)    #SE再生
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
        #Player制御
        self.player.update()

        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_TITLE
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                   #list全要素削除
            blasts.clear()                      #list全要素削除

	#描画関数
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #描画の画面分岐
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        #score表示(f文字列的な)
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(70, 40, "Title", 7)
        pyxel.text(50, 80, "- PRESS ENTER -", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        pyxel.text(55, 40, "GAME OVER", 7)
        pyxel.text(50, 80, "- PRESS ENTER -", 7)
App()