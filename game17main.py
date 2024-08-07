#左右移動アクション
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
STAGE_W = 128 * 2
SAGE_H = 128 * 1
LEFT_LIMIT = 40
RIGHT_LIMIT = WINDOW_W - 40 #調整項目
TILE_SIZE = 8
MAP_WIDTH = 16
MAP_HEIGHT = 16
#list用意
bullets = []
enemies = []
enemiesUI = []
blasts = []
items = []
particles = []
hitparticles = []

#関数(TileMap(0)のタイルを取得)
#指定座標のタイルの種類を取得
def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
 
#関数(タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #8は今回のplayerが8×8ドットサイズだから
def check_collision(x, y):
    x1 = x // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 1) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (1,0):
        isStop = True
        return isStop
    #右上判定
    if get_tile(x2,y1) == (1,0):
        isStop = True
        return isStop
    #左下判定
    if get_tile(x1,y2) == (1,0):
        isStop = True
        return isStop
    #右下判定
    if get_tile(x2,y2) == (1,0):
        isStop = True
        return isStop
    return False

#関数(タイルとのBulletコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #2は今回のbulletが2×2ドットサイズだから
def check_bullet_collision(x, y):
    x1 = x // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    x2 = (x + 2 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 2 - 1) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (1,0):
        isTileHit = True
        return isTileHit
    #右上判定
    if get_tile(x2,y1) == (1,0):
        isTileHit = True
        return isTileHit
    #左下判定
    if get_tile(x1,y2) == (1,0):
        isTileHit = True
        return isTileHit
    #右下判定
    if get_tile(x2,y2) == (1,0):
        isTileHit = True
        return isTileHit
    return False

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
        self.new_player_x = x
        self.new_player_y = y
        self.old_x = 0
        self.old_y = 0
        self.gravity = GRAVITY
        self.hp = PLAYER_HP
        self.direction = 1
        self.isGround = False
        self.isJump = False
        self.isLRmove = True
        self.is_alive = True
    def update(self):
        #移動入力
        if self.isLRmove == True:
            if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                self.dx = 1
                self.direction = 1  #右向き
            if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dx = -1
                self.direction = -1 #左向き
        """
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A):
            if self.direction == 1:
                Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == -1:
                Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
        """
        #jump入力
        if (pyxel.btnp(pyxel.KEY_SPACE) and (self.isJump == False) and (self.isGround == True)):
            self.dy = -1.5
            self.isJump = True
            self.isGround = False

        #空中時処理
        if self.isGround == False:
            #加速度更新
            self.dy += self.gravity #重力加速度的な
            #速度更新
            self.x += self.dx
            self.y += self.dy
            #直前座標
            self.old_x = self.x
            self.old_y = self.y
            #Playerの位置を更新
            self.new_player_x = self.x + self.dx
            self.new_player_y = self.y + self.dy
        #接地時処理
        else:
            #速度更新
            self.x += self.dx
            #直前座標
            self.old_x = self.x
            #Playerの位置を更新
            self.new_player_x = self.x + self.dx
            self.new_player_y = self.y + self.dy

        #移動先での当たり判定
        #床判定
        if check_collision(self.x, self.new_player_y) == True:
            self.dy = 0
            #座標戻す
#            self.y = self.old_y   #足元に障害物。座標戻す
            self.isGround = True
            self.isJump = False
        else:
            self.y = self.new_player_y
            self.isGround = False

        #左右壁判定
        if check_collision(self.new_player_x, self.y) == False:
            self.x = self.new_player_x   #左右に障害物が無いので座標更新
            print("wall")
#            self.isLRmove = True
        else:
            pass
#            self.isLRmove = False
        """
        #床
        if check_collision(self.x, self.new_player_y) == False:
            #加速度更新
#            self.dy += self.gravity #重力加速度的な
            #速度更新
#            self.y += self.dy
#            self.y = new_player_y   #足元に障害物が無いので座標更新
            #直前座標
#            self.old_y = self.y
            self.isGround = False   #つまり地面にいない状態
            print(self.old_y)
#            print("sky")
        else:   #床的なところに接触
            self.isGround = True
#            self.isJump = False
            #加速度更新
#            self.dy += self.gravity #重力加速度的な
            #座標戻す
            self.y = self.old_y   #足元に障害物。座標戻す
            print(self.y)
            self.dy = 0
            print("ground")
        """
        #移動停止
        self.dx = 0
#        self.dy += self.gravity #重力加速度的な
#        self.dy = 1 #重力加速度的な

    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8 * self.direction, 8, 0)

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
        self.x += self.speed * self.direction        #弾移動
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
        #移動先でtileと当たり判定
        if check_bullet_collision(self.x, self.y) == True:
            #HitParticle
            hitparticles.append(
                HitParticle(self.x, self.y)
            )

            self.is_alive = False   #タイル接触なら消去
    def draw(self):
        pyxel.pset(self.x, self.y, self.color)

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
        items.append(self)
    def update(self):
        self.x = self.x
        self.y = self.y
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 8, 8, 0)

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
        pyxel.circb(self.x, self.y, 2, 7)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="2D ACT", fps = 60)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource17.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成(+1は着地座標調整、確定ではない)
        self.player = Player(pyxel.width / 2, pyxel.height / 2 + 1)

        #仮配置
        Enemy(32, pyxel.height / 2, 0, 0,20)
        Enemy(100, pyxel.height / 2, 0, 0,20)
        #BG表示用の座標
        self.scroll_x = 0
        self.scroll_y = 0

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
                if (enemy.x + 8    > bullet.x - 2 and
                    enemy.x        < bullet.x + 2 and
                    enemy.y + 8    > bullet.y - 2 and
                    enemy.y        < bullet.y + 2):
                    #Hit時の処理
                    enemy.hp -= 1
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
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        items.append(
                            Item(enemy.x, enemy.y)
                        )
                        #Particle
                        for i in range(10):
                            particles.append(
                                Particle(enemy.x, enemy.y)
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
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(items)
        update_list(particles)
        update_list(hitparticles)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(items)
        cleanup_list(particles)
        cleanup_list(hitparticles)

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
            particles.clear()                     #list全要素削除
            hitparticles.clear()                     #list全要素削除

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

        pyxel.text(0,  0, "PC_dx:%f" %self.player.old_x, 7)
        pyxel.text(0, 6, f"SCORE {self.player.dx:5}", 7)

        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)
        draw_list(particles)
        draw_list(hitparticles)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()