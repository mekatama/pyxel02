#スキマ通過ゲー
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PlAYER_W = 2
ENEMY_W = 2
PLAYER_HP = 1
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
#list用意
enemies = []
enemiesUI = []
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
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.size = size
        self.color = 10 #colorは0～15
        self.hp = PLAYER_HP
        self.direction = 1
        self.inputCount = 0
        self.is_alive = True
    def update(self):
        self.inputCount += 1
        #入力タイミングに制限入れる
        if self.inputCount % 1 == 0:
            #size入力
            if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                self.size += 2
                if self.size >= 80:
                    self.size = 80
            if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.size -= 2
                if self.size <= 4:
                    self.size = 4
#            print(self.y - self.size / 2)
    def draw(self):
        pyxel.rect(self.x, self.y - self.size / 2, PlAYER_W, self.size, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, size,):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.is_scoreUI = False
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #移動
        self.x -= self.speed
    def draw(self):
        pyxel.rect(self.x, self.y,                      ENEMY_W, self.size, 3)
        pyxel.rect(self.x, self.y + 100 - self.size,    ENEMY_W, self.size, 3)

#■Enemy_UI
class EnemyUI:
    def __init__(self, x, y, score, color):
        self.x = x
        self.y = y
        self.score = score
        self.color =color
        self.count = 0
        self.is_alive = True
        enemiesUI.append(self)
    def update(self):
        self.count += 1
        if self.count < 20:
            self.y -= 1
        elif self.count >= 20:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", self.color)

#■Blust
class Blast:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.r += 9    #円の半径大きくする用
        if self.r >= 200:
            self.is_alive = False
    def draw(self):
        pyxel.circb(self.x, self.y, self.r, 10)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        self.highScore = 0
        self.spawntime = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2, 60, 10)

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
            self.spawntime = 30
        elif self.score >= 30 and self.score < 70:
            self.spawntime = 25
        elif self.score >= 70:
            self.spawntime = 20

        if pyxel.frame_count < 600:
            self.spawntime = 60
            speed = 1
        elif pyxel.frame_count >= 600 and pyxel.frame_count < 1200:
            self.spawntime = 40
            speed = 1.5
        elif self.score >= 1200:
            self.spawntime = 20
            speed = 2

        #一定時間でenemy出現判定
        if pyxel.frame_count % self.spawntime == 0:
            #enemy sizeランダム
            spawn_size = pyxel.rndi(20, 48)
            #仮配置
            Enemy(130, 10, speed, spawn_size)

        #Player制御
        self.player.update()
        #EnemyとPlayerの当たり判定
        for enemy in enemies:
            if (self.player.x + PlAYER_W                > enemy.x and
                self.player.x                           < enemy.x + ENEMY_W and
                self.player.y + self.player.size / 2    > enemy.y and
                self.player.y - self.player.size / 2    < enemy.y + enemy.size):
                #Hit時の処理
                self.player.hp -= 1
#                pyxel.play(3, 1, loop=False)    #SE再生
                #player残りHP判定
                if self.player.hp <= 0:
                    pyxel.stop()
                    self.scene = SCENE_GAMEOVER

        #EnemyとPlayerの距離判定
        for enemy in enemies:
            if (self.player.x + PlAYER_W                > enemy.x and
                self.player.x                           < enemy.x + ENEMY_W):
                if enemy.is_scoreUI == False:
                    score = (enemy.y + enemy.size) - (self.player.y - self.player.size / 2)
                    score_bonus = 0
                    color = 13
                    if score == 0:
                        #ボーナス発生
                        score_bonus = 50
                        color = 10
                        #bonus effect
                        blasts.append(
                            Blast(self.player.x - 1, self.player.y, 0)
                        )

                    self.score += (30 + score + self.player.size + score_bonus)
                    enemiesUI.append(
                        EnemyUI(self.player.x - 26, self.player.y, 30 + score + self.player.size, color)
                    )
                    enemy.is_scoreUI = True

        #High Score
        if self.score >= self.highScore:
            self.highScore = self.score

        #list実行
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        #list更新
        cleanup_list(enemies)
        cleanup_list(blasts)
        cleanup_list(enemiesUI)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        #list更新
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            self.spawntime = 0
            #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                     #list全要素削除
            blasts.clear()

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
        pyxel.text(48, 28, "GIRI !!?", 7)
        pyxel.text(32, 58, "- PRESS  ENTER -", 7)
        pyxel.text(0, 76, "--------------------------------", 7)
        pyxel.text(40, 82, "HOW TO PLAY", 7)
        pyxel.text(4, 94, "LENGTH : UP or DOWN ARROW KEY", 7)
        pyxel.text(20, 100, "GO THROUGH THE HOLE !!", 7)
        pyxel.text(16, 106, "PERFECT FIT AND BONUS !!", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        self.player.draw()
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()