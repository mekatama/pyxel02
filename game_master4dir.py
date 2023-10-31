#４方向移動アクションmaster
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
        self.vh = 0 #上下と左右移動の判定用
        self.hp = PLAYER_HP
        self.reversal = 1
        self.direction = 6
        self.is_alive = True
    def update(self):
        #移動入力
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -PLAYER_SPEED
            self.dy = 0
            self.vh = 0
            self.reversal = -1
            self.direction = 4
        elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = PLAYER_SPEED
            self.dy = 0
            self.vh = 0
            self.reversal = 1
            self.direction = 6
        elif (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            self.vh = 1
            self.dx = 0
            self.dy = -PLAYER_SPEED
            self.reversal = 1
            self.direction = 8
        elif (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            self.vh = 1
            self.dx = 0
            self.dy = PLAYER_SPEED
            self.reversal = -1
            self.direction = 2
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A):
            if self.reversal == 1:
                if self.vh == 0:    #右向き
                    Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, 6)
                elif self.vh == 1:  #上向き
                    Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8)
            elif self.reversal == -1:
                if self.vh == 0:    #左向き
                    Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, 4)
                elif self.vh == 1:  #下向き
                    Bullet(self.x + 4, self.y + 6, PLAYER_BULLET_SPEED, 2)
        #Playerの位置を更新
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        #移動停止
        self.dx = 0
        self.dy = 0
    def draw(self):
        #editorデータ描画(player)
        if self.vh == 0:
            pyxel.blt(self.x, self.y, 0, 8, 0, 8 * self.reversal, 8, 0)
        elif self.vh == 1:
            pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8 * self.reversal, 0)

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
        #弾移動
        if self.direction == 6:     #右向き
            self.x += self.speed
        elif self.direction == 4:   #左向き
            self.x -= self.speed
        elif self.direction == 8:   #上向き
            self.y -= self.speed
        elif self.direction == 2:   #下向き
            self.y += self.speed
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
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
#        elif self.count >= 10:
#            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0 + (8 * self.motion), 8, 8, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2, pyxel.height / 2)

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

        #ItemとPlayerの当たり判定
        for item in items:
            if (self.player.x + 12  > item.x + 4 and
                self.player.x + 4   < item.x + 12 and
                self.player.y + 12  > item.y + 4 and
                self.player.y + 4   < item.y + 12):
                #Hit時の処理
                self.score += 10
                item.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

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
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "TITLE", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "GAME OVER", 7)
App()