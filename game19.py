#格闘アクション
import pyxel
import math
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
GRAVITY = 0.05
PLAYER_HP = 1
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
ENEMY_BULLET_SPEED = 0.5
STAGE_W = 128 * 2
SAGE_H = 128 * 1
LEFT_LIMIT = 40
RIGHT_LIMIT = WINDOW_W - 40 #調整項目
TILE_SIZE = 8
MAP_WIDTH = 16
MAP_HEIGHT = 16
#list用意
enemybullets = []
bullets = []
hitparticles = []
enemies = []
blasts = []
particles = []

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
        self.count_atk = 0  #攻撃入力制限用count
        self.isAtk = False  #攻撃中flag
        self.is_alive = True
    def update(self):
        #移動入力
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = PLAYER_SPEED
            self.direction = 1  #右向き
        elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -1 * PLAYER_SPEED
            self.direction = -1 #左向き
        else:
            self.dx = 0
        #攻撃入力
        if (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)):
            if self.isAtk == False:
                if self.direction == 1:
                    Bullet(self.x + 9, self.y, self.direction)
                elif self.direction == -1:
                    Bullet(self.x - 5, self.y, self.direction)
                self.isAtk = True
        #攻撃入力制限処理
        if self.isAtk == True:
            self.count_atk += 1
            if self.count_atk > 60:
                self.count_atk = 0
                self.isAtk = False

        #Playerの位置を更新
        self.x = self.x + self.dx

    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8 * self.direction, 8, 0)
#■Bullet
class Bullet:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.direction = dir
        self.count = 0
        self.is_alive = True
        bullets.append(self)
    def update(self):
        self.count += 1
        #一定時間で消去
        if self.count > 2:            
            self.is_alive = False   #消去
    def draw(self):
        pyxel.rect(self.x, self.y, 4, 8, 7)
#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.countHit = 0       #ヒットストップ時間
        self.isHit = False
        self.isFire = False
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #enemyの仮移動
        if self.isHit == False:
            self.x += self.speed
        #ヒットストップ時間
        else:
            self.countHit += 1
            if self.countHit > 30:
                self.countHit = 0
                self.isHit = False
        #攻撃
        if pyxel.frame_count % 60 == 0:
            self.isFire = True
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 8, 8, 0)
#■EnemyBullet
class EnemyBullet:
    def __init__(self, x, y, speed, aim):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 1
        self.color = 10         #colorは0～15
        self.count = 0
        self.aim = aim          #攻撃角度
        self.is_alive = True
        enemybullets.append(self)
    def update(self):
        #弾用座標
        self.x += self.speed * math.cos(self.aim)
        self.y += self.speed * -math.sin(self.aim)
        #一定時間で消去
        self.count += 1
        if self.count > 160:
            self.is_alive = False   #消去
    def draw(self):
        pyxel.circ(self.x, self.y, 1, self.color)
#■HitParticle
class HitParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0
        self.is_alive = True
        hitparticles.append(self)
    def update(self):
        self.count += 1
        if self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.circb(self.x, self.y, 2, 7)
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
#■Particle
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.count = 0
        self.speed = 0.2    #速度
        self.aim = 0        #攻撃角度
        self.is_alive = True
        particles.append(self)
    def update(self):
        #一定間隔で角度決定→消滅
        self.count += 1
        if self.count == 1:
            self.aim = pyxel.rndf(0, 2 * math.pi)
        if self.count >= 30 + pyxel.rndi(1, 50):
            self.is_alive = False
        #座標
        self.x += self.speed * math.cos(self.aim)
        self.y += self.speed * -math.sin(self.aim)
    def draw(self):
        pyxel.pset(self.x + 4, self.y + 4, 7)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="2D ACT", fps = 60)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource19.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(36, 104)

        #BG表示用の座標
        self.scroll_x = 0
        self.scroll_y = 0
        #仮配置
        Enemy(16, 70, 0.1, 1, 20)
#        Enemy(16, 104, 0.1, 1, 20)

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
                if (enemy.x + 8    > bullet.x  and
                    enemy.x        < bullet.x + 4 and
                    enemy.y + 8    > bullet.y  and
                    enemy.y        < bullet.y + 8):
                    #Hit時の処理
                    enemy.hp -= 1
                    enemy.isHit = True
                    #HitParticle
                    hitparticles.append(
                        HitParticle(bullet.x, bullet.y)
                    )
                    #Particle
                    for i in range(2):
                        particles.append(
                            Particle(enemy.x, enemy.y)
                        )
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0 and enemy.is_alive == True:
                        enemy.is_alive = False
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        #Particle
                        for i in range(10):
                            particles.append(
                                Particle(enemy.x, enemy.y)
                            )

                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生
        #EnemyのPlayer狙い処理
        for enemy in enemies:
            #攻撃タイミング
            if enemy.isFire == True:
                dx = self.player.x - enemy.x
                dy = self.player.y - enemy.y
                enemy.aim = math.atan2(-dy, dx)
                #敵弾生成
                enemybullets.append(
                    EnemyBullet(enemy.x, enemy.y, ENEMY_BULLET_SPEED, enemy.aim)
                )
                enemy.isFire = False

        #High Score
        if self.score >= self.highScore:
            self.highScore = self.score

        #画面スクロール処理
        #左へスクロール
        if self.player.x < self.scroll_x + LEFT_LIMIT:  #左判定ライン到達
            self.scroll_x = self.player.x - LEFT_LIMIT  #BG用座標更新
            if self.scroll_x < 0:                       #BGの端到達判定
                self.scroll_x = 0                       #スクロール停止
        #右へスクロール
        if self.scroll_x + RIGHT_LIMIT < self.player.x: #右判定ライン到達
            self.scroll_x = self.player.x - RIGHT_LIMIT #BG用座標更新
            if STAGE_W - pyxel.width < self.scroll_x:   #BGの端到達判定
                self.scroll_x = STAGE_W - pyxel.width   #スクロール停止
        #list実行
        update_list(bullets)
        update_list(enemybullets)
        update_list(hitparticles)
        update_list(enemies)
        update_list(blasts)
        update_list(particles)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemybullets)
        cleanup_list(hitparticles)
        cleanup_list(enemies)
        cleanup_list(blasts)
        cleanup_list(particles)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list全要素削除
            bullets.clear()         #list全要素削除
            enemybullets.clear()    #list全要素削除
            hitparticles.clear()    #list全要素削除
            enemies.clear()         #list全要素削除
            blasts.clear()          #list全要素削除
            particles.clear()       #list全要素削除

	#描画関数
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #cameraリセット
        pyxel.camera()  #左上隅の座標を(0, 0)にリセット処理
        #描画の画面分岐
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        #score表示(f文字列的な)
#        pyxel.text(4, 4, f"SCORE {self.score:5}", 7)
#        pyxel.text(60, 4, f"HIGH SCORE {self.highScore:5}", 6)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(48, 28, "________", 7)
        pyxel.text(32, 58, "- PRESS  ENTER -", 7)
        pyxel.text(0, 76, "--------------------------------", 7)
        pyxel.text(40, 82, "HOW TO PLAY", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #BG描画
        pyxel.bltm(0, 0, 0, self.scroll_x, self.scroll_y, 128, 128, 0)
        #camera再セット
        pyxel.camera(self.scroll_x, self.scroll_y)

        pyxel.text(0,  24, "    y:%f" %self.player.y, 7)
        pyxel.text(0,  30, "   dy:%f" %self.player.dy, 7)

        self.player.draw()
        draw_list(bullets)
        draw_list(enemybullets)
        draw_list(enemies)
        draw_list(hitparticles)
        draw_list(blasts)
        draw_list(particles)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()