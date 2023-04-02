#左右から迫る敵を倒せ
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 120
WINDOW_W = 160
BULLET_SPEED = 0
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
        self.isAtk = True   #playerの攻撃flag
        self.is_alive = True
        self.isDir = 1      #playerの向き(右1 左-1)
        self.isMotion = 0   #playerのmotion(wait:0 attak:1)
    def update(self):
        #key入力(攻撃)
        if pyxel.btnp(pyxel.KEY_D) and (self.isAtk == True):
            #弾生成
            Bullet(self.x + 24, self.y + 8)
            self.isAtk = False
            self.isDir = 1
            self.isMotion = 1
        if pyxel.btnp(pyxel.KEY_A) and (self.isAtk == True):
            #弾生成
            Bullet(self.x - 8, self.y + 8)
            self.isAtk = False
            self.isDir = -1
            self.isMotion = 1
        #一定時間攻撃不可判定
        if pyxel.frame_count % 16 == 0 and (self.isAtk == False):
            self.isAtk = True
            self.isMotion = 0
    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 0, self.isMotion * 16, 16 * self.isDir, 16, 0)
        #当たり判定
        pyxel.rectb(self.x + 4, self.y, 8, 16, 10)

#■Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 2
        self.color = 10 #colorは0～15
        self.is_alive = True
        bullets.append(self)
    def update(self):
        self.y -= BULLET_SPEED          #弾移動
        if pyxel.frame_count % 16 == 0: #一定時間表示
            self.is_alive = False       #消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, hp, img, dir, speed):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.is_Right = dir     #移動方向flag(右:1 左:-1)
        self.addSpeed = speed   #追加speed
        self.aniCount = 0       #アニメ用カウント
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        enemies.append(self)
    def update(self):
        self.aniCount += 1
        #アニメ切り替え
        if self.aniCount % 8 == 0: #一定時間表示
            if self.motion == 0:
                self.motion = 1
            elif self.motion == 1:
                self.motion = 0
        #移動
        if self.is_Right == 1:
            self.x += (ENEMY_SPEED + self.addSpeed)           #右移動
        elif self.is_Right == -1:
            self.x -= (ENEMY_SPEED + self.addSpeed)           #左移動
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16 * self.img, 16 * self.motion, 16 * self.is_Right, 16, 0)
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

#ゲーム管理
class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        self.scene = SCENE_TITLE
        self.score = 0
        self.enemy_addSpeed = 0
        #インスタンス生成
        self.player = Player(pyxel.width / 2, pyxel.height - 20)
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        #画面遷移
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    #タイトル画面制御
    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY

    #ゲームプレイ画面
    def update_play_scene(self):
        #spawn位置
        enemy_spawn = pyxel.rndi(0, 1)
        #spawn間隔係数
        enemy_spawnspeed = 60 - (self.enemy_addSpeed * 15)
        #一定時間でenemy出現判定
        if pyxel.frame_count % enemy_spawnspeed == 0:
            #ScoreでEnemyのspeed変化
            if self.score <= 100:
                self.enemy_addSpeed = 0
            elif self.score > 100 and self.score <= 200:
                self.enemy_addSpeed = 2
            elif self.score > 200:
                self.enemy_addSpeed = 3
            #enemy生成
            if enemy_spawn == 0:
                Enemy(-16, 100, 1, 1, 1, self.enemy_addSpeed)
            elif enemy_spawn == 1: 
                Enemy(176, 100, 1, 1, -1, self.enemy_addSpeed)
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
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )

        #EnemyとPlayerの当たり判定
        for enemy in enemies:
            if (self.player.x + 12  > enemy.x + 2 and
                self.player.x + 4   < enemy.x + 14 and
                self.player.y + 16  > enemy.y and
                self.player.y       < enemy.y + 16):
                #Hit時の処理
                enemy.is_alive = False
                self.player.hp -= 1
                #player残りHP判定
                if self.player.hp <= 0:
                    blasts.append(
                        Blast(enemy.x, enemy.y)
                    )
                    self.scene = SCENE_GAMEOVER

        #Player制御
        self.player.update()
        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        #list更新
        cleanup_list(enemies)
        cleanup_list(bullets)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)

    #Gameover画面制御
    def update_gameover_scene(self):
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        cleanup_list(enemies)
        cleanup_list(bullets)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        #ボタン入力で再play
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2     #初期位置
            self.player.y = pyxel.height - 20   #初期位置
            self.player.isRight = True          #flag初期化
            self.player.isDir = 1               #flag初期化
            self.isMotion = 0                   #flag初期化
            self.player.hp = 3                  #HP初期化
            self.score = 0
            enemies.clear()                     #list全要素削除
            bullets.clear()                     #list全要素削除
            enemiesUI.clear()                   #list全要素削除
            blasts.clear()                      #list全要素削除

    def draw(self):
        pyxel.cls(0)    #画面クリア 0は黒
        #各画面の表示判定
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        #score表示(f文字列的な)
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    def draw_title_scene(self):
        pyxel.text(35, 66, "Pyxel Shooter", pyxel.frame_count % 16)
        pyxel.text(31, 74, "- PRESS ENTER -", 13)
        pyxel.text(31, 82, "D key : Right Punch", 13)
        pyxel.text(31, 90, "A key : Left Punch", 13)

    def draw_play_scene(self):
        pyxel.bltm(0, 0, 0, 0, 0, 160, 120)
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        pyxel.text(self.player.x, 90, f"HP:{self.player.hp:1}", 13)
    
    def draw_gameover_scene(self):
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        pyxel.text(43, 30, "GAME OVER", 8)
        pyxel.text(31, 60, "- PRESS ENTER -", 13)
App()