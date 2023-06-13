#ベルトスクロールアクション01
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PLAYER_SPEED = 1
#list用意
playerbullets = []
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
        self.direction = 1  #playerの向き
        self.isAtk = True   #playerの攻撃flag
        self.motion = 0   #playerのmotion(歩行motion制御用)
        self.count = 0      #時間計測用
        self.aniCount = 0   #アニメ用カウント
        self.is_alive = True
    def update(self):
        self.aniCount += 1
        #歩行アニメ切り替え
        if self.aniCount % 4 == 0: #一定時間表示
            if self.motion == 0:
                self.motion = 1
            elif self.motion == 1:
                self.motion = 0
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A) and (self.isAtk == True):
            #弾生成
            if self.direction == 1:
                PlayerBullet(self.x + 13, self.y + 13)
            elif self.direction == -1:
                PlayerBullet(self.x - 1,  self.y + 13)
            self.isAtk = False
            self.isMotion = 1
        #攻撃間隔
        if self.isAtk == False:
            self.count += 1
        else:
            self.count = 0  #リセット
        #一定時間攻撃不可判定(8がよさそう)
        if self.count % 8 == 0 and self.isAtk == False:
            self.isAtk = True
            self.isMotion = 0
        #移動入力
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and (self.isAtk == True):
            self.x -= PLAYER_SPEED
            self.direction = -1
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and (self.isAtk == True):
            self.x += PLAYER_SPEED
            self.direction = 1
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and (self.isAtk == True):
            self.y -= PLAYER_SPEED
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and (self.isAtk == True):
            self.y += PLAYER_SPEED
    def draw(self):
        #editorデータ描画(player)
        if self.isAtk == True:
            pyxel.blt(self.x, self.y, 0, 16 * self.motion, 0, 16 * self.direction, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 16, 16 * self.direction, 16, 0)

#■PlayerBullet
class PlayerBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 2
        self.color = 10     #colorは0～15
        self.count = 0      #時間計測用
        self.is_alive = True
        playerbullets.append(self)
    def update(self):
        self.count += 1
        #一定時間表示(8がよさそう)
        if self.count % 8 == 0:
            self.is_alive = False       #消去
    def draw(self):
        pyxel.rectb(self.x, self.y, 4, 3, 5)

#■Enemy
class Enemy:
    def __init__(self, x, y, hp, img, speed):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.speed = speed
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #移動
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 0)
        #当たり判定
        pyxel.rectb(self.x + 4, self.y + 13, 8, 3, 5)


class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource07.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 -8, pyxel.height / 2 -8)

        #仮の敵配置
        Enemy(100, 60, 3, 0, 0)

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

        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in playerbullets:
                if (enemy.x + 12    > bullet.x and
                    enemy.x + 4     < bullet.x + 4 and
                    enemy.y + 16    > bullet.y and
                    enemy.y + 13    < bullet.y + 3):
                    #Hit時の処理
                    print("hit!")
                    pyxel.play(1, 1, loop=False)    #SE再生
                    bullet.is_alive = False
                    enemy.hp -= 1
                    cleanup_list(playerbullets)
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        self.score += 10
                        pyxel.play(1, 0, loop=False)    #SE再生

        #list実行
        update_list(playerbullets)
        update_list(enemies)
        #list更新
        cleanup_list(playerbullets)
        cleanup_list(enemies)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        update_list(playerbullets)
        update_list(enemies)
        #list更新
        cleanup_list(playerbullets)
        cleanup_list(enemies)
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list更新
            playerbullets.clear()          #list全要素削除
            enemies.clear()                #list全要素削除

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

        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #score表示(f文字列的な)
        pyxel.text(0, 0, f"isAtk {self.player.isAtk}", 7)

        self.player.draw()
        draw_list(playerbullets)
        draw_list(enemies)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        draw_list(playerbullets)
        draw_list(enemies)
App()