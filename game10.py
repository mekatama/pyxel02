#tank01
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
ENEMY_SPEED = 0.3
ENEMY_BLOWSPEED = 2
ENEMY_HITSTOP = 1
ENEMY_COUNT = 0
#list用意
bullets = []
melees = []
enemies = []
enemiesUI = []
blowenemies = []
blasts = []

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
    x2 = (x + 8 - 0) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 0) // 8   #キャラy座標下端のTileMapの座標
    #tileの種類で判定
    #左上判定
    if get_tile(x1,y1) == (0,0):
        isStop = True
        return isStop
    #右上判定
    if get_tile(x2,y1) == (0,0):
        isStop = True
        return isStop
    #左下判定
    if get_tile(x1,y2) == (0,0):
        isStop = True
        return isStop
    #右下判定
    if get_tile(x2,y2) == (0,0):
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
        self.vh = 0 #上下と左右移動の判定用
        self.reversal = 1
        self.direction = 6
        self.count = 0
        self.is_stop = False
        self.is_alive = True
    def update(self):
        #移動入力
        if self.is_stop == False:
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
        #shot攻撃入力
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
        #melee攻撃入力
        if pyxel.btnp(pyxel.KEY_S):
            self.is_stop =True
            if self.reversal == 1:
                if self.vh == 0:    #右向き
                    Melee(self.x + 8, self.y, 6)
                elif self.vh == 1:  #上向き
                    Melee(self.x, self.y - 8, 8)
            elif self.reversal == -1:
                if self.vh == 0:    #左向き
                    Melee(self.x - 8, self.y, 4)
                elif self.vh == 1:  #下向き
                    Melee(self.x, self.y + 8, 2)
        if self.is_stop == True:
            self.count += 1
        
        #Playerの位置を更新
        new_player_x = self.x + self.dx
        new_player_y = self.y + self.dy
        #移動先で当たり判定
        if check_collision(new_player_x, self.y) == False:
            self.x = new_player_x
        if check_collision(self.x, new_player_y) == False:
            self.y = new_player_y
        #移動停止
        self.dx = 0
        self.dy = 0
        #一定時間停止
        if self.count > 30:
            self.is_stop = False
            self.count = 0  #初期化            

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
        #移動先で当たり判定
        if check_bullet_collision(self.x, self.y) == True:
            self.is_alive = False   #タイル接触なら消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

class Melee:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.direction = dir
        self.color = 9 #colorは0～15
        self.count = 0
        self.is_atk = True  #１回だけ当たり判定処理したいの
        self.is_alive = True
        melees.append(self)
    def update(self):
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        if self.direction == 6:     #右向き
            pyxel.rect(self.x, self.y, 8, 8, self.color)
        elif self.direction == 4:   #左向き
            pyxel.rect(self.x, self.y, 8, 8, self.color)
        elif self.direction == 8:   #上向き
            pyxel.rect(self.x, self.y, 8, 8, self.color)
        elif self.direction == 2:   #下向き
            pyxel.rect(self.x, self.y, 8, 8, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.enemyscore = 10
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.count_hitstop = 0
        self.melee_hit_dir = 0
        self.is_meleeHit = False
        self.is_stop = False
        self.is_alive = True
        enemies.append(self)
    def update(self):
        global ENEMY_COUNT  #グローバル変数使えるようにする
        #移動
        if self.is_stop == False and self.is_meleeHit == False:
            if self.direction == 6:
                self.x += self.speed
            elif self.direction == 4:
                self.x -= self.speed
            elif self.direction == 8:
                self.y -= self.speed
            elif self.direction == 2:
                self.y += self.speed
            pass
        #HitStop処理
        else:
            self.count_hitstop += 1
            if self.count_hitstop > 30:
                self.is_stop = False
                self.count_hitstop = 0 #初期化
        if self.is_alive == False:
            ENEMY_COUNT += 1
            print(ENEMY_COUNT)
        '''
        #meleeHit時ふっとび移動
        if self.is_meleeHit == True:
            if self.melee_hit_dir == 8:
                self.x += 0
                self.y -= ENEMY_BLOWSPEED
            elif self.melee_hit_dir == 2:
                self.x += 0
                self.y += ENEMY_BLOWSPEED
            elif self.melee_hit_dir == 6:
                self.x += ENEMY_BLOWSPEED
                self.y += 0
            elif self.melee_hit_dir == 4:
                self.x -= ENEMY_BLOWSPEED
                self.y += 0
        #ふっとび中のタイルとの当たり判定
        if self.is_meleeHit == True:
            if check_collision(self.x, self.y) == True:
                self.is_alive = False   #タイル接触なら消去
                blasts.append(
                    Blast(self.x, self.y)
                )
        '''            
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
        if self.count < 30:
            self.y -= 0.2
        else:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", 13)

#■BlowEnemy
class BlowEnemy:
    def __init__(self, x, y, speed, dir, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.count = 0
        self.count_hitstop = 0
        self.melee_hit_dir = dir
        self.is_meleeHit = False
        self.is_stop = False
        self.is_alive = True
        blowenemies.append(self)
    def update(self):
        global ENEMY_COUNT  #グローバル変数使えるようにする
        #meleeHit時ふっとび移動
        if self.melee_hit_dir == 8:
            self.x += 0
            self.y -= ENEMY_BLOWSPEED
        elif self.melee_hit_dir == 2:
            self.x += 0
            self.y += ENEMY_BLOWSPEED
        elif self.melee_hit_dir == 6:
            self.x += ENEMY_BLOWSPEED
            self.y += 0
        elif self.melee_hit_dir == 4:
            self.x -= ENEMY_BLOWSPEED
            self.y += 0
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
        #ふっとび敵死亡時にENEMY_COUNTリセット
        if self.is_alive == False:
            ENEMY_COUNT = 0

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 8, 8, 0)

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

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Tank", fps = 60, display_scale = 3)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        self.count = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 -8, pyxel.height / 2 -8)
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
        #最終的にscoreで生成間隔を制御
        spawntime = 20
        #一定時間でenemy出現判定
        if pyxel.frame_count % spawntime == 0:
            #生成辺(位置)ランダム
            spawn_side = pyxel.rndi(0, 3)
            #生成座標ランダム
            if spawn_side == 0:
                spawn_x = pyxel.rndi(0, 120)
                spawn_y = -12
                spawn_dir = 2
            elif spawn_side == 1:
                spawn_x = pyxel.rndi(0, 120)
                spawn_y = 140
                spawn_dir = 8
            elif spawn_side == 2:
                spawn_x = -12
                spawn_y = pyxel.rndi(0, 120)
                spawn_dir = 6
            elif spawn_side == 3:
                spawn_x = 140
                spawn_y = pyxel.rndi(0, 120)
                spawn_dir = 4
            pass                
            #enemy生成(最終的にscoreで分岐)
            Enemy(spawn_x, spawn_y, ENEMY_SPEED, spawn_dir,3)

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
                    enemy.is_stop = True
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
        #EnemyとBlowEnemyの当たり判定
        #初期化
        self.count = 0
        for enemy in enemies:
            #ここで敵の数をカウントできる?
            for blowenemy in blowenemies:
                if (enemy.x + 8    > blowenemy.x and
                    enemy.x         < blowenemy.x + 8 and
                    enemy.y + 8    > blowenemy.y and
                    enemy.y         < blowenemy.y + 8):
                    #score計算

                    #Hit時の処理
                    enemy.is_alive = False
                    self.count += 1
                    blasts.append(
                        Blast(enemy.x, enemy.y)
                    )
#                    self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生
                    enemiesUI.append(
                        EnemyUI(enemy.x, enemy.y, 10)
                    )
            #EnemyとMeleeの当たり判定
        for enemy in enemies:
            for melee in melees:
                if melee.is_atk ==  True:
                    if (enemy.x + 8    > melee.x and
                        enemy.x         < melee.x + 8 and
                        enemy.y + 8    > melee.y and
                        enemy.y         < melee.y + 8):
                        #Hit時の処理
                        enemy.is_alive = False
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        blowenemies.append(
                            BlowEnemy(enemy.x, enemy.y, ENEMY_BLOWSPEED, self.player.direction,1)
                        )
                       #残りHP判定
                        if enemy.hp <= 0:
                            enemy.is_alive = False
                            blasts.append(
                                Blast(enemy.x, enemy.y)
                            )
    #                        self.score += 10
    #                        pyxel.play(1, 0, loop=False)    #SE再生
    #                        enemiesUI.append(
    #                            EnemyUI(enemy.x, enemy.y, 10)
    #                        )
                        #１回だけ処理
                        melee.is_atk = False

        #list実行
        update_list(bullets)
        update_list(melees)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blowenemies)
        update_list(blasts)
        #list更新
        cleanup_list(bullets)
        cleanup_list(melees)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blowenemies)
        cleanup_list(blasts)

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
        draw_list(bullets)
        draw_list(melees)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blowenemies)
        draw_list(blasts)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
App()