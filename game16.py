#縦STGmaster
import pyxel
import math
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
ENEMY_SPEED = 1
ENEMY_BULLET_SPEED = 0.5
BG_SCROLL = 1
#list用意
bullets = []
enemybullets = []
enemies = []
enemiesUI = []
blasts = []
items = []
particles = []
hitparticles = []
options = []
bgs = []

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
        self.shotType = 0   #0:シングル 1:ダブル 2:レーザー 3:3way
        self.is_alive = True
    def update(self):
        #移動入力
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -PLAYER_SPEED
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = PLAYER_SPEED
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            self.dy = -PLAYER_SPEED
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            self.dy = PLAYER_SPEED
        #攻撃入力
        #一定時間で自動射撃
        if pyxel.frame_count % 6 == 0:
            if self.shotType == 0:
                Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8, 0, 1)
            elif self.shotType == 1:
                Bullet(self.x + 6, self.y + 2, PLAYER_BULLET_SPEED, 8, 1, 1)
                Bullet(self.x + 2, self.y + 2, PLAYER_BULLET_SPEED, 8, 1, 1)
            elif self.shotType == 2:
                Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8, 2, 1)
            elif self.shotType == 3:
                Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8, 3, 1)
                Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8, 3, 2)
                Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, 8, 3, 3)

        #Playerの位置を更新
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        #移動停止
        self.dx = 0
        self.dy = 0
    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 0)

#■Option
class Option:
    def __init__(self, x, y):
        self.x1 = x
        self.x2 = x
        self.y = y
        self.is_alive = True
        options.append(self)
    def update(self):
        #移動
        self.x1 = self.x
        self.x2 = self.x
        self.y = self.y
        #攻撃入力
        #一定時間で自動射撃
        if pyxel.frame_count % 6 == 0:
            Bullet(self.x1 + 12, self.y + 2, PLAYER_BULLET_SPEED, 7, 0, 1)
            Bullet(self.x2 -  5, self.y + 2, PLAYER_BULLET_SPEED, 7, 0, 1)
    def draw(self):
        pyxel.circb(self.x1 + 12, self.y + 4, 2, 7)
        pyxel.circb(self.x2 -  5, self.y + 4, 2, 7)

class Bullet:
    def __init__(self, x, y, speed, dir, type, way):
        self.x = x
        self.y = y
        self.direction = dir
        self.speed = speed
        self.type = type
        self.way = way
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.is_alive = True
        bullets.append(self)
    def update(self):
        #弾移動
        if self.type == 0 or self.type == 1 or self.type == 2:
            self.y -= self.speed
        elif self.type == 3:
            self.y -= self.speed
            if self.way == 1:
                self.x -= 1
            elif self.way == 2:
                self.x += 1
            elif self.way == 3:
                pass

        #一定時間で消去
        self.count += 1
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        if self.type == 0:
            pyxel.pset(self.x, self.y, self.color)
        elif self.type == 1:
            pyxel.pset(self.x, self.y, self.color)
        elif self.type == 2:
            pyxel.pset(self.x, self.y, self.color)
        elif self.type == 3:
            pyxel.pset(self.x, self.y, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, hp, atkType, moveType, isMoveStart):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.count = 0
        self.aim = 0
        self.aim2 = 0
        self.timer = 0              #円運動の
        self.r = 5                  #円運動の
        self.atkType = atkType      #攻撃type 0:真下 1:player狙う 2:途中で変化
        self.moveType = moveType    #移動Type 0:固定 1:真下 2:player狙う 3:三角関数
        self.isDamage = False
        self.isFire = False     #攻撃flag
        self.isMoveStart = isMoveStart  #生成時に指定位置まで移動するかどうかflag
        self.isMoveStop = False         #生成して移動後に停止したflag
        self.isMove = False             #通常移動開始flag
        self.isMoveSeach = False        #player狙う移動flag
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #初期位置への移動
        if self.isMoveStart == True:    #初期位置への移動
            if self.y <= 32:            #初期y座標判定
                self.y += self.speed
            else:
                if self.count == 0:
                    self.isMoveStop = True
                self.count += 1         #一時停止時間の設定
                if self.count >= 60:
                    self.isMove = True
        else:
            self.isMove = True

        #移動処理
        if self.isMove == True:         #通常移動の処理
            if self.moveType == 0:
                pass
            elif self.moveType == 1:
                self.y += self.speed
            elif self.moveType == 2:
                self.x += self.speed * math.cos(self.aim2)
                self.y += self.speed * -math.sin(self.aim2)
            elif self.moveType == 3:
                self.timer += 0.15
                self.x = self.x + self.r * math.cos(self.timer)
                self.y += self.speed

        
        #一定時間で自動射撃
        if pyxel.frame_count % 60 == 0:
            if self.isMoveStop == True:
                if self.atkType == 0:
                    enemybullets.append(
                        EnemyBullet(self.x + 4, self.y + 8, ENEMY_BULLET_SPEED, 0, 0, 1)
                    )
                elif self.atkType == 1:
                    self.isFire = True
                elif self.atkType == 2:
                    if self.hp > 100:
                        enemybullets.append(
                            EnemyBullet(self.x + 4, self.y + 8, ENEMY_BULLET_SPEED, 0, 0, 1)
                        )
                    elif self.hp <= 100:
                        self.isFire = True

    def draw(self):
        if self.isDamage == False:
            #通常
            pyxel.blt(self.x, self.y, 0, 24, 0, 8, 8, 0)
        else:
            #ダメージ発生
            pyxel.blt(self.x, self.y, 0, 24, 8, 8, 8, 0)
            self.isDamage = False

#■EnemyBullet
class EnemyBullet:
    def __init__(self, x, y, speed, aim, type, way):
        self.x = x
        self.y = y
        self.speed = speed
        self.type = type    #0:真下 1:player狙う
        self.way = way
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.is_alive = True
        self.aim = aim        #攻撃角度
        enemybullets.append(self)
    def update(self):
        #弾移動
        if self.type == 0:      #真下
            self.y += self.speed
        elif self.type == 1:   #player狙う
            #弾用座標
            self.x += self.speed * math.cos(self.aim)
            self.y += self.speed * -math.sin(self.aim)
            pass
        #一定時間で消去
        self.count += 1
        if self.count > 180:            
            self.is_alive = False   #消去
    def draw(self):
        if self.type == 0 or self.type == 1:
#            pyxel.pset(self.x + 4, self.y + 8, self.color)
            pyxel.circb(self.x, self.y, 1, self.color)

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
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.count += 1
        if self.count >= 13:
            self.is_alive = False
    def draw(self):
        pyxel.circb(self.x + 4, self.y + 4, self.count, 7)

#■Particle
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.count = 0
        self.speed = 0.2     #速度
        self.aim = 0        #攻撃角度
        self.is_alive = True
        particles.append(self)
    def update(self):
        #一定間隔で角度決定→消滅
        self.count += 1
        if self.count == 1:
            self.aim = pyxel.rndf(0, 2 * math.pi)
#            print(self.aim)
        if self.count >= 30 + pyxel.rndi(1, 50):
            self.is_alive = False
        #弾用aim移動ヒットeffectは円表示
        self.x += self.speed * math.cos(self.aim)
        self.y += self.speed * -math.sin(self.aim)
    def draw(self):
        pyxel.pset(self.x + 4, self.y + 4, 7)

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
        pyxel.circb(self.x - 1, self.y + 2, 2, 7)

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

#■BG
class Bg:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side
        self.is_nextBG = False
        self.is_alive = True
        bgs.append(self)
    def update(self):
        #BGスクロール
        self.y += BG_SCROLL
        if self.y == 0:
            self.is_nextBG = True
        if self.y >= 128:
            self.is_nextBG = False
            self.is_alive = False
    def draw(self):
        if self.side == 0:
            pyxel.blt(self.x, self.y, 0, 40, 0, -8, 128, 0)
        elif self.side == 1:
            pyxel.blt(self.x, self.y, 0, 40, 0, 8, 128, 0)
            

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="TATE STG", fps = 60)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource16.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2, pyxel.height / 2)
        #[debug]Option表示
        options.append(
            Option(self.player.x + 8, self.player.y)
        )
        options.append(
            Option(self.player.x - 8, self.player.y)
        )
        #BGs初期化
        bgs.append(
            Bg(0, -128, 0)
        )
        bgs.append(
            Bg(120, -128, 1)
        )
        #仮
        Enemy(pyxel.rndi(8, 112), -8, ENEMY_SPEED, 200, 2, 0, True)
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
        '''
        #scoreで生成間隔を制御
        if self.score < 30:
            spawntime = 30
        elif self.score >= 30 and self.score < 70:
            spawntime = 25
        elif self.score >= 70:
            spawntime = 20
        '''

        spawntime = 60
        #一定時間でenemy出現判定
        if pyxel.frame_count % spawntime == 0:
            #enemy生成
#            Enemy(pyxel.rndi(8, 112), -8, ENEMY_SPEED, 10, 1, 1, True)
            pass

        #Player制御
        self.player.update()
        #BG制御 表示するグループ単位で判定する
        for bg in bgs:
            if bg.is_nextBG == True and bg.is_alive == True and bg.side == 0:
                bgs.append(
                    Bg(0, -128, 0)
                )
                bg.is_nextBG = False
            if bg.is_nextBG == True and bg.is_alive == True and bg.side == 1:
                bgs.append(
                    Bg(120, -128, 1)
                )
                bg.is_nextBG = False

        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x + 8    > bullet.x and
                    enemy.x         < bullet.x + 2 and
                    enemy.y + 8    > bullet.y and
                    enemy.y         < bullet.y + 2):
                    #Hit時の処理
                    enemy.hp -= 1
                    enemy.isDamage = True
                    hitparticles.append(
                        HitParticle(bullet.x + 1, bullet.y)
                    )
                    #HitParticle
                    for i in range(2):
                        particles.append(
                            Particle(enemy.x, enemy.y)
                        )
                    #レーザーは貫通する
                    if bullet.type != 2:
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
                        for i in range(10):
                            particles.append(
                                Particle(enemy.x, enemy.y)
                            )
                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生

        #option制御
        for option in options:
            option.x = self.player.x
            option.y = self.player.y

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

        #EnemyBulletとPlayerの当たり判定
        for enemybullet in enemybullets:
            if (self.player.x + 6  > enemybullet.x - 0 and
                self.player.x + 2   < enemybullet.x + 2 and
                self.player.y + 6  > enemybullet.y - 0 and
                self.player.y + 2  < enemybullet.y + 2):
                #Hit時の処理
                self.player.hp -= 1
                enemybullet.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生
                #player残りHP判定
                if self.player.hp <= 0:
                    blasts.append(
                        Blast(enemybullet.x, enemybullet.y)
                    )
                    pyxel.stop()
                    self.scene = SCENE_GAMEOVER

        #EnemyのPlayer狙い処理
        for enemy in enemies:
            #攻撃タイミング
            if enemy.isFire == True:
                #playerのy座標より小さく and 画面中央より上で攻撃
                if enemy.y < self.player.y and enemy.y < WINDOW_H / 2:
                    dx = self.player.x - enemy.x
                    dy = self.player.y - enemy.y
                    enemy.aim = math.atan2(-dy, dx)
    #                print(self.aim)
                    #敵弾生成
                    if enemy.atkType == 2:
                        enemybullets.append(
                            EnemyBullet(enemy.x + 4, enemy.y + 8, ENEMY_BULLET_SPEED, enemy.aim, 1, 1)
                        )
                    else:
                        enemybullets.append(
                            EnemyBullet(enemy.x + 4, enemy.y + 8, ENEMY_BULLET_SPEED, enemy.aim, 1, 1)
                        )
                    enemy.isFire = False
            #移動タイミング
            if enemy.isMoveSeach == False:
                dx = self.player.x - enemy.x
                dy = self.player.y - enemy.y
                enemy.aim2 = math.atan2(-dy, dx)
                enemy.isMoveSeach = True    #Falseだとずーっと追いかけてくる

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
        update_list(enemybullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(items)
        update_list(particles)
        update_list(hitparticles)
        update_list(options)
        update_list(bgs)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemybullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(items)
        cleanup_list(particles)
        cleanup_list(hitparticles)
        cleanup_list(options)
        cleanup_list(bgs)

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
            enemybullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                     #list全要素削除
            blasts.clear()                     #list全要素削除
            items.clear()                     #list全要素削除
            particles.clear()                     #list全要素削除
            hitparticles.clear()                     #list全要素削除
            options.clear()                     #list全要素削除
            bgs.clear()                     #list全要素削除

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
        pyxel.text(48, 28, "________", 7)
        pyxel.text(32, 58, "- PRESS  ENTER -", 7)
        pyxel.text(0, 76, "--------------------------------", 7)
        pyxel.text(40, 82, "HOW TO PLAY", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        draw_list(bgs)
        self.player.draw()
        draw_list(bullets)
        draw_list(enemybullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)
        draw_list(particles)
        draw_list(hitparticles)
        draw_list(options)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()