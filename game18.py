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
hitparticles = []
enemies = []
blasts = []
particles = []
transpoters = []

#関数(TileMap(0)のタイルを取得)
#指定座標のタイルの種類を取得
def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
 
#関数(足元タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #8は今回のplayerが8×8ドットサイズだから
    #足元の2点だけ判定
def check_collision_yuka(x, y):
    x1 = (x + 1) // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 1) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左下判定
    if get_tile(x1,y2) == (1,0):
        isStop = True
#        print("左下")
        return isStop
    #右下判定
    if get_tile(x2,y2) == (1,0):
        isStop = True
#        print("右下")
        return isStop
    return False

#関数(頭上タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #8は今回のplayerが8×8ドットサイズだから
    #頭上の2点だけ判定
def check_collision_head(x, y):
    x1 = x // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 1) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (1,0):
        isStop = True
#        print("左上")
        return isStop
    #右上判定
    if get_tile(x2,y1) == (1,0):
        isStop = True
#        print("右上")
        return isStop
    return False

#関数(左右タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #8は今回のplayerが8×8ドットサイズだから
def check_collision_wall(x, y):
    x1 = x // 8            #キャラx座標左端のTileMapの座標
    y1 = (y + 1) // 8            #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 1 - 1) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (1,0):
        isStop = True
#        print("wall左上")
        return isStop
    #右上判定
    if get_tile(x2,y1) == (1,0):
        isStop = True
#        print("wall右上")
        return isStop
    #左下判定
    if get_tile(x1,y2) == (1,0):
        isStop = True
#        print("wall左下")
        return isStop
    #右下判定
    if get_tile(x2,y2) == (1,0):
        isStop = True
#        print("wall右下")
        return isStop
    return False

#関数(タイルとのBullet(dot)コリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #//bulletはdotなので、一点だけで判定で良さそう
def check_bullet_collision(x, y):
    x1 = x // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (1,0):
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
        self.gravity = GRAVITY
        self.hp = PLAYER_HP
        self.direction = 1
        self.atk_type = 1
        self.isGround = False
        self.isJump = False
        self.isWall = False
        self.isShot = False
        self.is_alive = True
    def update(self):
        #移動入力
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = PLAYER_SPEED
            self.direction = 1  #右向き
            self.isShot = True
        elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -1 * PLAYER_SPEED
            self.direction = -1 #左向き
            self.isShot = True
        elif (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            self.isShot = False
            #武器チェンジ
            if self.atk_type == 0:
                self.atk_type = 1
            elif self.atk_type == 1:
                self.atk_type = 0
        else:
            self.isShot = True
            self.dx = 0
        #jump入力
        if (pyxel.btnp(pyxel.KEY_SPACE) and (self.isJump == False) and (self.isGround == True)):
            self.dy = -1.5
            self.isJump = True
            self.isGround = False
        #攻撃入力
        #一定時間で自動射撃
        if self.isShot == True:
            if self.atk_type == 0:
                if pyxel.frame_count % 12 == 0:
                    if self.direction == 1:
                        Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction, self.atk_type)
                    elif self.direction == -1:
                        Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction, self.atk_type)
            elif self.atk_type == 1:
                if pyxel.frame_count % 30 == 0:
                    if self.direction == 1:
                        Bullet(self.x + 5, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type)
                    elif self.direction == -1:
                        Bullet(self.x + 2, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type)

        #空中時処理
        if self.isGround == False:
            #加速度更新
            self.dy += self.gravity #重力加速度的な
        else:
            self.dy += 0 #変化なし
        #playerの位置を更新する前に衝突判定
        self.new_player_x = self.x + self.dx
        #y座標のみ空中時に計算
        if self.isGround == False:
            self.new_player_y = self.y + self.dy

        #移動先での当たり判定
        #wall判定
        if check_collision_wall(self.new_player_x, self.y) == True:
            self.isWall = True
        else:
            self.isWall = False
            self.x = self.new_player_x

        #頭上判定
        if check_collision_head(self.x, self.new_player_y) == True:
            self.dy = 1 #下方向に加速させる

        #床判定
        if check_collision_yuka(self.x, self.new_player_y) == True:
            self.y = round(self.y / 8) * 8 #丸めて着地
            self.isGround = True
            self.isJump = False
        else:
            self.isGround = False
            self.y = self.new_player_y

    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8 * self.direction, 8, 0)

class Bullet:
    def __init__(self, x, y, speed, dir,type):
        self.x = x
        self.y = y
        self.new_bullet_x = x
        self.new_bullet_y = y
        self.speed = speed
        self.direction = dir
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.count_missile = 0
        self.type = type #0:通常 1:ミサイル 2:レーザー
        self.is_alive = True
        bullets.append(self)
    def update(self):
        #位置を更新する前に衝突判定
        if self.type == 0:
            self.new_bullet_x = self.x + self.speed * self.direction
        elif self.type == 1:
            #初速と加速で更に判定
            self.new_bullet_x = self.x + self.speed * self.direction * 0.1
            self.count_missile += 1
            #missile加速
            if self.count_missile >= 20:
                self.new_bullet_x = self.x + self.speed * self.direction * 1.2
            pass
        #移動先でtileと当たり判定
        #通常弾
        if self.type == 0:
            if check_bullet_collision(self.new_bullet_x, self.y) == True:
                self.x = round(self.x / 8) * 8 #丸めて着地
                #HitParticle
                hitparticles.append(
                    HitParticle(self.x, self.y)
                )
                self.is_alive = False   #タイル接触なら消去
            else:
                self.x = self.new_bullet_x
        else:
            if check_collision_wall(self.new_bullet_x, self.y) == True:
                self.x = round(self.x / 8) * 8 #丸めて着地
                #HitParticle
                if self.direction == 1:
                    hitparticles.append(
                        HitParticle(self.x + 8, self.y + 4)
                    )
                else:
                    hitparticles.append(
                        HitParticle(self.x, self.y + 4)
                    )
                self.is_alive = False   #タイル接触なら消去
            else:
                self.x = self.new_bullet_x

#        self.x += self.speed * self.direction        #弾移動
        self.count += 1
        #一定時間で消去
        if self.count > 60:
            self.is_alive = False   #消去
    def draw(self):
        if self.type == 0:
            pyxel.pset(self.x, self.y, self.color)
        elif self.type == 1:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.direction, 8, 0)
#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.new_enemy_x = x
        self.new_enemy_y = y
        self.gravity = GRAVITY
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.speed = speed
        self.isGround = False
        self.isJump = False
        self.isWall = False
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #移動
        if self.isGround == True:
            if self.direction == 1:
                self.dx = self.speed
            elif self.direction == -1:
                self.dx = -1 * self.speed
        #空中時処理
        if self.isGround == False:
            #加速度更新
            self.dy += self.gravity #重力加速度的な
        else:
            self.dy += 0 #変化なし
        #playerの位置を更新する前に衝突判定
        self.new_enemy_x = self.x + self.dx
        #y座標のみ空中時に計算
        if self.isGround == False:
            self.new_enemy_y = self.y + self.dy

        #移動先での当たり判定
        #wall判定
        if check_collision_wall(self.new_enemy_x, self.y) == True:
            self.isWall = True
            #壁接触で移動方向反転
            if self.direction == -1:
                self.direction = 1
            elif self.direction == 1:
                self.direction = -1
            
        else:
            self.isWall = False
            self.x = self.new_enemy_x

        #頭上判定
        if check_collision_head(self.x, self.new_enemy_y) == True:
            self.dy = 1 #下方向に加速させる

        #床判定
        if check_collision_yuka(self.x, self.new_enemy_y) == True:
            self.y = round(self.y / 8) * 8 #丸めて着地
            self.isGround = True
            self.isJump = False
        else:
            self.isGround = False
            self.y = self.new_enemy_y

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 8 * self.direction, 8, 0)

#■Transpoter
class Transpoter:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.speed = speed
        self.is_alive = True
        transpoters.append(self)
    def update(self):
        #移動
        pass
#        self.new_enemy_x = self.x + self.dx
#        self.new_enemy_y = self.y + self.dy
        #生成
        if pyxel.frame_count % 120 == 0:
            Enemy(self.x + 4, self.y, 0.5, -1, 20)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 16 * self.direction, 16, 0)

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
        pyxel.load("my_resource18.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成(+1は着地座標調整、確定ではない)
        self.player = Player(36, pyxel.height / 2 + 1)

        #BG表示用の座標
        self.scroll_x = 0
        self.scroll_y = 0
        #仮配置
        Enemy(32, pyxel.height / 2, 0.5, -1, 20)
#        Transpoter(64, pyxel.height / 2, 0, -1, 20)

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
        update_list(hitparticles)
        update_list(enemies)
        update_list(blasts)
        update_list(particles)
        update_list(transpoters)
        #list更新
        cleanup_list(bullets)
        cleanup_list(hitparticles)
        cleanup_list(enemies)
        cleanup_list(blasts)
        cleanup_list(particles)
        cleanup_list(transpoters)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list全要素削除
            bullets.clear()         #list全要素削除
            hitparticles.clear()    #list全要素削除
            enemies.clear()         #list全要素削除
            blasts.clear()          #list全要素削除
            particles.clear()       #list全要素削除
            transpoters.clear()     #list全要素削除
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

        pyxel.text(0,   0, "isWall:%s" %self.player.isWall, 7)
        pyxel.text(0,   6, "isGround:%s" %self.player.isGround, 7)
        pyxel.text(0,  12, "isJump:%s" %self.player.isJump, 7)
        pyxel.text(0,  18, "new_y:%f" %self.player.new_player_y, 7)
        pyxel.text(0,  24, "    y:%f" %self.player.y, 7)
        pyxel.text(0,  30, "   dy:%f" %self.player.dy, 7)

        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(hitparticles)
        draw_list(blasts)
        draw_list(particles)
        draw_list(transpoters)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()