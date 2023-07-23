#円と矩形の当たる判定テスト
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
TILE_SIZE = 8
MAP_WIDTH = 16
MAP_HEIGHT = 16
PLAYER_SPEED = 0.5
PLAYER_BULLET_SPEED = 4
#list用意
bullets = []
enemies = []

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
        self.direction = 1
        self.target_dir = 6
        self.isStop = False
        self.is_alive = True
    def update(self):
        #移動入力
        if self.isStop == False:
            if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dx = -PLAYER_SPEED
                self.dy = 0
                self.vh = 0
                self.direction = -1
                self.target_dir = 4
            elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                self.dx = PLAYER_SPEED
                self.dy = 0
                self.vh = 0
                self.direction = 1
                self.target_dir = 6
            elif (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                self.vh = 1
                self.dx = 0
                self.dy = -PLAYER_SPEED
                self.direction = 1
                self.target_dir = 8
            elif (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.vh = 1
                self.dx = 0
                self.dy = PLAYER_SPEED
                self.direction = -1
                self.target_dir = 2
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A):
            if self.direction == 1:
                if self.vh == 0:    #右向き
                    Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, 6)
                elif self.vh == 1:  #上向き
                    Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8)
            elif self.direction == -1:
                if self.vh == 0:    #左向き
                    Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, 4)
                elif self.vh == 1:  #下向き
                    Bullet(self.x + 4, self.y + 6, PLAYER_BULLET_SPEED, 2)
        #Playerの位置を更新
        new_player_x = self.x + self.dx
        new_player_y = self.y + self.dy

        #仮制御
        self.x = new_player_x
        self.y = new_player_y
    def draw(self):
        #editorデータ描画(player)
        pyxel.circ(self.x, self.y, 16, 1)

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
        self.count += 0
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Tank", fps = 60, display_scale = 3)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 -8, pyxel.height / 2 -8)

        #仮
#        Enemy(64, 32, 0, 0,3)

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
        #Player制御
        self.player.update()
#        #Target制御
#        self.target.x = self.player.x
#        self.target.y = self.player.y
#        self.target.direction = self.player.target_dir
#        self.target.update()

#        self.target = Target(self.player.x + 32, self.player.y, 0)


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
#                        blasts.append(
#                            Blast(enemy.x, enemy.y)
#                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生
#                        enemiesUI.append(
#                            EnemyUI(enemy.x, enemy.y, 10)
#                        )

        #list実行
        update_list(bullets)
        update_list(enemies)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        #list更新
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list更新
            bullets.clear()                     #list全要素削除

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

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #BG描画
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        self.player.draw()
#        self.target.draw()
        draw_list(bullets)
        draw_list(enemies)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
App()