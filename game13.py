#左右移魂斗羅もどき
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PLAYER_HP = 1
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
PLAYER_X = 32
PLAYER_Y = 80
#list用意
bullets = []
enemies = []
enemiesUI = []
blasts = []
items = []

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
        self.dx = 0
        self.dy = 0
        self.hp = PLAYER_HP
        self.direction = 1
        self.directionMove = 1
        self.is_right = False
        self.is_up = False
        self.is_down = False
        self.is_alive = True
    def update(self):
        #方向入力
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.is_right = True
            self.directionMove = 1
            self.dx = 1
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
#            self.is_right = False
            self.directionMove = -1
            self.dx = -1
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            self.is_up = True
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            self.is_down = True
        #ボタン入力終了判定
        if pyxel.btnr(pyxel.KEY_RIGHT) == True:
            self.is_right = False
        if pyxel.btnr(pyxel.KEY_UP) == True:
            self.is_up = False
        if pyxel.btnr(pyxel.KEY_DOWN) == True:
            self.is_down = False

        #右上向き方向入力
        if self.is_right == True and self.is_up == True:
            self.direction = 4  #右上向き
        #上向き方向入力
        elif self.is_up == True:
            self.direction = 3 #上向き
        #下向き方向入力
        elif self.is_down == True:
            self.direction = 5 #下向き
        #右向き方向入力
        else:
            self.direction = 1  #右向き
#        print(self.is_right, self.is_up, self.is_down)

        #一定時間で自動射撃
        if pyxel.frame_count % 8 == 0:
            #弾生成
            if self.direction == 1:
                Bullet(self.x + 5, self.y + 8, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == 4:
                Bullet(self.x + 3, self.y + 6, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == 3:
                Bullet(self.x + 3, self.y + 2, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == 5:
                Bullet(self.x + 13, self.y + 12, PLAYER_BULLET_SPEED, self.direction)
        #Playerの位置を更新
        self.x = self.x + self.dx
        #移動停止
        self.dx = 0
    def draw(self):
        #editorデータ描画(player)
        if self.direction == 1:
            pyxel.blt(self.x, self.y,       0, 8, 0, 8 * self.directionMove, 16, 0)
        elif self.direction == 4:
            pyxel.blt(self.x, self.y,       0, 8, 16, 8 * self.directionMove, 16, 0)
        elif self.direction == 3:
            pyxel.blt(self.x, self.y,       0, 8, 32, 8 * self.directionMove, 16, 0)
        elif self.direction == 5:
            pyxel.blt(self.x, self.y + 8,   0, 0, 48, 16 * self.directionMove, 8, 0)

class Bullet:
    def __init__(self, x, y, speed, dir):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = dir
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.is_alive = True
        bullets.append(self)
    def update(self):
        if self.direction == 1:
            #右
            self.x += self.speed
        if self.direction == 4:
            #右上
            self.x += self.speed
            self.y -= self.speed
        if self.direction == 3:
            #上
#            self.x = 50
            self.y -= self.speed
        if self.direction == 5:
            #下
            self.x += self.speed
#            self.y = 77
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #移動
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 8, 8, 0)

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
        pyxel.blt(self.x, self.y, 0, 16, 0 + (8 * self.motion), 8, 8, 0)

#■Item
class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = 0
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.x = self.x
        self.y = self.y
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 8, 8, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource13.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(PLAYER_X, PLAYER_Y)

        #仮配置
        Enemy(32, pyxel.height / 2, 0, 0,3)

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

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)    #BGM再生
            self.scene = SCENE_PLAY

    #ゲーム画面処理用update
    def update_play_scene(self):
        #scoreで生成間隔を制御
        if self.score < 30:
            spawntime = 30
        elif self.score >= 30 and self.score < 70:
            spawntime = 25
        elif self.score >= 70:
            spawntime = 20

        #Player制御
        self.player.update()
        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x + 8    > bullet.x and
                    enemy.x         < bullet.x + 2 and
                    enemy.y + 8    > bullet.y and
                    enemy.y         < bullet.y + 2):
                    #Hit時の処理
                    enemy.hp -= 1
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        items.append(
                            Item(enemy.x, enemy.y)
                        )
                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生

        #EnemyとPlayerの当たり判定
        for enemy in enemies:
            if (self.player.x + 12  > enemy.x + 4 and
                self.player.x + 4   < enemy.x + 12 and
                self.player.y + 12  > enemy.y + 4 and
                self.player.y + 4   < enemy.y + 12):
                #Hit時の処理
                self.player.hp -= 1
                enemy.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生
                #player残りHP判定
                if self.player.hp <= 0:
                    blasts.append(
                        Blast(enemy.x, enemy.y)
                    )
                    pyxel.stop()
                    self.scene = SCENE_GAMEOVER

        #ItemとPlayerの処理
        for item in items:
            #Itemの動き
            ex = (self.player.x - item.x)
            ey = (self.player.y - item.y)
            Kp = 0.2
            if ex != 0 or ey != 0:
                item.x = item.x + ex * Kp
                item.y = item.y + ey * Kp

            #ItemとPlayerの当たり判定
            if (self.player.x + 12  > item.x + 4 and
                self.player.x + 4   < item.x + 12 and
                self.player.y + 12  > item.y + 4 and
                self.player.y + 4   < item.y + 12):
                #Hit時の処理
                self.score += 10
                item.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

        #High Score
        if self.score >= self.highScore:
            self.highScore = self.score

        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(items)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(items)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        #list更新
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list全要素削除
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                     #list全要素削除
            blasts.clear()                     #list全要素削除
            items.clear()                     #list全要素削除

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
        pyxel.text(4, 4, f"SCORE {self.score:5}", 7)
        pyxel.text(60, 4, f"HIGH SCORE {self.highScore:5}", 6)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "TITLE", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        draw_list(bullets)
        self.player.draw()
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "GAME OVER", 7)
App()