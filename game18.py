#左右移動アクション
import pyxel
import math
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
SCENE_HELP1 = 3     #ヘルプ画面1
SCENE_HELP2 = 4     #ヘルプ画面2
SCENE_HELP3 = 5     #ヘルプ画面3
SCENE_HELP4 = 6     #ヘルプ画面4
#グローバル変数
g_enemy_spawn_num = 0   #enemyの生成数
#定数
WINDOW_H = 128
WINDOW_W = 128
GRAVITY = 0.05
PLAYER_HP = 10
PLAYER_SPEED = 0.5
PLAYER_BULLET_SPEED = 4
ENEMY_BULLET_SPEED = 0.5
STAGE_W = 64 * 3
#STAGE_W = 128 * 2
SAGE_H = 128 * 1
LEFT_LIMIT = 64
RIGHT_LIMIT = WINDOW_W - 64 #調整項目
TILE_SIZE = 8
MAP_WIDTH = 16
MAP_HEIGHT = 16
#list用意
enemybullets = []
bullets = []
hitparticles = []
enemies = []
enemiesUI = []
blasts = []
particles = []
transpoters = []
items = []

#関数(TileMap(0)のタイルを取得)
#指定座標のタイルの種類を取得
def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
 
#関数(足元タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #8は今回のplayerが8×8ドットサイズだから
    #足元の2点だけ判定
def check_collision_yuka(x, y):
    x1 = (x + 1) // 8           #キャラx座標左端のTileMapの座標
    y1 = y // 8                 #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 8 - 1) // 8       #キャラy座標下端のTileMapの座標
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

#関数(足元タイルとのコリジョン判定)
    #//は商を求める(余りは切り捨てる)
    #中型機用
    #足元の2点だけ判定
def check_collision_yuka16(x, y):
    x1 = (x + 1) // 8           #キャラx座標左端のTileMapの座標
    y1 = y // 8                 #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1 - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y + 16 - 1) // 8      #キャラy座標下端のTileMapの座標
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
    x1 = x // 8                 #キャラx座標左端のTileMapの座標
    y1 = (y + 1) // 8           #キャラy座標上端のTileMapの座標
    x2 = (x + 8 - 1) // 8       #キャラx座標右端のTileMapの座標
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
        self.atk_type = 0
        self.motion = 0         #描画切り替えよう
        self.count_ani = 0      #ダメージ用count
        self.count_ani2 = 0     #アニメーション再生用count
        self.count_stop = 0     #移動停止時間をカウント
        self.count_shot = 0     #攻撃間隔をカウント
        self.zandan_missile = 10
        self.zandan_laser = 10
        self.isGround = False
        self.isJump = False
        self.isWall = False
        self.isShot = False
        self.isHit = False
        self.isUp = False       #上入力flag
        self.isStepOn = False   #敵踏みつけflag
        self.is_alive = True
    def update(self):
        self.count_ani2 += 1
        #歩行アニメ切り替え
        if self.count_ani2 % 8 == 0: #一定時間表示
            if self.motion == 0:
                self.motion = 1
            elif self.motion == 1:
                self.motion = 0
        #移動入力
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = PLAYER_SPEED
            self.direction = 1      #右向き
            self.isShot = True
            self.isUp = False
        elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -1 * PLAYER_SPEED
            self.direction = -1     #左向き
            self.isShot = True
            self.isUp = False
        #武器チェンジ
        elif (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            self.isShot = False
            self.isUp = False
            #武器チェンジ
            if self.atk_type == 0:
                self.atk_type = 1
            elif self.atk_type == 1:
                self.atk_type = 2
            elif self.atk_type == 2:
                self.atk_type = 0
        else:
            #上攻撃
            if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                self.isUp = True
                self.isShot = True
                self.dx = 0
            #停止
            else:
                self.isUp = False
                self.isShot = False
                self.dx = 0
                self.count_stop += 1
                self.count_shot = 0
        #jump入力(敵踏みつけてもジャンプtest)
        if ((pyxel.btnp(pyxel.KEY_SPACE) and (self.isJump == False) and (self.isGround == True)) or
             self.isStepOn == True):
            self.dy = -1.5
            self.isJump = True
            self.isGround = False
            self.isStepOn = False
            self.count_stop = 0
        #攻撃入力
        #一定時間で自動射撃
        if self.isShot == True:
            self.count_stop = 0
            self.count_shot += 1
            if self.atk_type == 0:
                if self.count_shot % 9 == 0:
                    if self.direction == 1:
                        Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                    elif self.direction == -1:
                        Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                    elif self.isUp == True:
                        Bullet(self.x + 4, self.y + 2, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
            elif self.atk_type == 1:
                if self.zandan_missile > 0:
                    if self.count_shot % 30 == 0:
                        if self.isUp == False:
                            if self.direction == 1:
                                Bullet(self.x + 8, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                            elif self.direction == -1:
                                Bullet(self.x - 8, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                        elif self.isUp == True:
                            Bullet(self.x, self.y - 8, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                        #残弾処理
                        self.zandan_missile -= 1
            elif self.atk_type == 2:
                if self.zandan_laser > 0:
                    if self.count_shot % 30 == 0:
                        if self.isUp == False:
                            if self.direction == 1:
                                Bullet(self.x + 4, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                            elif self.direction == -1:
                                Bullet(self.x - 12, self.y, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                        elif self.isUp == True:
                            Bullet(self.x, self.y - 8, PLAYER_BULLET_SPEED, self.direction, self.atk_type, self.isUp)
                        #残弾処理
                        self.zandan_laser -= 1
        #空中時処理
        if self.isGround == False:
            self.count_stop = 0
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
        if self.isHit == False:
            pyxel.blt(self.x, self.y, 0, 0, 24 + (8 * self.motion), 8 * self.direction, 8, 0)
        else:
            if self.count_ani <= 8: #ダメージモーション再生
                self.count_ani += 1 
            elif self.count_ani > 8:
                self.isHit = False
                self.count_ani = 0  #初期化
            pyxel.blt(self.x, self.y, 0, 8, 24 + (8 * self.motion), 8 * self.direction, 8, 0)
#■Bullet
class Bullet:
    def __init__(self, x, y, speed, dir, type, isUp):
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
        self.type = type #0:通常 1:ミサイル 2:レーザー 3:???
        self.isUp = isUp
        self.is_alive = True
        bullets.append(self)
    def update(self):
        #位置を更新する前に衝突判定
        if self.type == 0:      #通常
            #左右方向
            if self.isUp == False:
                self.new_bullet_x = self.x + self.speed * self.direction
            else:
                self.new_bullet_y = self.y - self.speed
        elif self.type == 1:    #ミサイル
            #左右方向
            if self.isUp == False:
                #初速と加速で更に判定
                self.new_bullet_x = self.x + self.speed * self.direction * 0.1
                self.count_missile += 1
                #missile加速
                if self.count_missile >= 20:
                    self.new_bullet_x = self.x + self.speed * self.direction * 1.2
            else:
                #初速と加速で更に判定
                self.new_bullet_y = self.y - self.speed * 0.1
                self.count_missile += 1
                #missile加速
                if self.count_missile >= 20:
                    self.new_bullet_y = self.y - self.speed * 1.2
        elif self.type == 2:    #レーザー
            #左右方向
            if self.isUp == False:
                self.new_bullet_x = self.x + self.speed * self.direction * 1.2
            else:
                self.new_bullet_y = self.y - self.speed * 1.2
        #移動先でtileと当たり判定
        if self.type == 0:      #通常弾
            #左右方向
            if self.isUp == False:
                if check_bullet_collision(self.new_bullet_x, self.y) == True:
                    self.x = round(self.x / 8) * 8 #丸めて着地
                    #HitParticle
                    hitparticles.append(
                        HitParticle(self.x, self.y)
                    )
                    self.is_alive = False   #タイル接触なら消去
                else:
                    self.x = self.new_bullet_x
            #上方向
            else:
                self.y = self.new_bullet_y
        elif self.type == 1:    #ミサイル
            #左右方向
            if self.isUp == False:
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
            #上方向
            else:
                self.y = self.new_bullet_y
        elif self.type == 2:    #レーザー
            #左右方向
            if self.isUp == False:
                self.x = self.new_bullet_x
            #上方向
            else:
                self.y = self.new_bullet_y
        self.count += 1
        #一定時間で消去
        if self.count > 60:
            self.is_alive = False   #消去
    def draw(self):
        if self.type == 0:
            pyxel.pset(self.x, self.y, self.color)
        elif self.type == 1:
            if self.isUp == False:
                pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.direction, 8, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)
        elif self.type == 2:
            if self.isUp == False:
                pyxel.blt(self.x, self.y, 0, 48, 0, 16 * self.direction, 8, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 56, 8, 8, 16, 0)
#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp, moveType, atkType):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.new_enemy_x = x
        self.new_enemy_y = y
        self.gravity = GRAVITY
        self.hp = hp
        self.direction = dir        #移動方向flag(右:1 左:-1)
        self.moveType = moveType    #0:移動 1:移動と停止 2:停止 3:空中移動 4:画面外から空中停止
        self.atkType = atkType      #0:横通常弾 1:下通常弾 2:エイム通常弾 3:グレネード弾
        self.speed = speed
        self.moveCount = 0
        self.moveCount2 = 0
        self.motion = 0         #描画切り替えよう
        self.count_ani = 0      #ダメージ用count
        self.count_ani2 = 0     #アニメーション再生用count
        self.isGround = False
        self.isJump = False
        self.isWall = False
        self.isShot = True
        self.isFire = False         #aim攻撃判定用
        self.isHit = False
        self.is_alive = True
        enemies.append(self)
    def update(self):
        self.count_ani2 += 1
        #歩行アニメ切り替え
        if self.count_ani2 % 8 == 0: #一定時間表示
            if self.motion == 0:
                self.motion = 1
            elif self.motion == 1:
                self.motion = 0
        #移動
        if self.isGround == True:
            #左右移動
            if self.moveType == 0:
                if self.isHit == False:
                    if self.direction == 1:
                        self.dx = self.speed
                    elif self.direction == -1:
                        self.dx = -1 * self.speed
                else:
                    self.dx = 0
            #移動と停止
            elif self.moveType == 1:
                #移動
                if self.moveCount < 30:
                    self.moveCount += 1
                    if self.isHit == False:
                        if self.direction == 1:
                            self.dx = self.speed
                        elif self.direction == -1:
                            self.dx = -1 * self.speed
                    else:
                        self.dx = 0
                #停止
                elif self.moveCount >= 30 and self.moveCount < 60:
                    self.dx = 0
                    self.moveCount += 1
                #初期化
                elif self.moveCount >= 60:
                    self.moveCount = 0
            #停止
            else:
                pass
        #空中用
        else:
            #左右移動
            if self.moveType == 3:
                if self.isHit == False:
                    if self.direction == 1:
                        self.dx = self.speed
                    elif self.direction == -1:
                        self.dx = -1 * self.speed
                else:
                    self.dx = 0
            #画面外から空中停止
            if self.moveType == 4:
                if self.moveCount2 < 25:
                    self.dy += 0.1
                    self.y += self.dy
                    self.moveCount2 += 1
                elif self.moveCount2 >= 25:
                    self.dy = 0

        #攻撃入力
        #一定時間で自動射撃
        if self.isShot == True:
            if self.atkType == 0:
                if pyxel.frame_count % 180 == 0:
                    if self.direction == 1:
                        EnemyBullet(self.x + 5, self.y + 4, ENEMY_BULLET_SPEED, self.direction, self.atkType, 0)
                    elif self.direction == -1:
                        EnemyBullet(self.x + 2, self.y + 4, ENEMY_BULLET_SPEED, self.direction, self.atkType, 0)
            if self.atkType == 1:
                if pyxel.frame_count % 180 == 0:
                    EnemyBullet(self.x + 4, self.y + 8, ENEMY_BULLET_SPEED, 2, self.atkType, 0)
            if self.atkType == 2:
                if pyxel.frame_count % 180 == 0:
                    self.isFire = True  #エイム攻撃はappで処理
                pass
        #空中時処理
        if self.isGround == False:
            if self.moveType != 3 and self.moveType != 4:
                #加速度更新
                self.dy += self.gravity #重力加速度的な
            else:
                self.dy += 0            #空中敵は落下しない
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
        if self.isHit == False:
            if self.moveType == 0:
                pyxel.blt(self.x, self.y, 0, 16, 24 + (8 * self.motion), 8 * self.direction, 8, 0)
            elif self.moveType == 1:
                pyxel.blt(self.x, self.y, 0, 0, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
            if self.atkType == 1:
                pyxel.blt(self.x, self.y, 0, 16, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
            elif self.atkType == 2:
                pyxel.blt(self.x, self.y, 0, 32, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
        else:
            if self.count_ani <= 8: #ダメージモーション再生
                self.count_ani += 1
            elif self.count_ani > 8:
                self.isHit = False
                self.count_ani = 0  #初期化

            if self.moveType == 0:
                pyxel.blt(self.x, self.y, 0, 24, 24 + (8 * self.motion), 8 * self.direction, 8, 0)
            elif self.moveType == 1:
                pyxel.blt(self.x, self.y, 0, 8, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
            if self.atkType == 1:
                pyxel.blt(self.x, self.y, 0, 24, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
            elif self.atkType == 2:
                pyxel.blt(self.x, self.y, 0, 40, 40 + (8 * self.motion), 8 * self.direction, 8, 0)
#■Enemy_UI
class EnemyUI:
    def __init__(self, x, y, score, type):
        self.x = x
        self.y = y
        self.score = score
        self.type = type    #0:score 1:HP
        self.count = 0
        self.is_alive = True
        enemiesUI.append(self)
    def update(self):
        self.count += 1
        if self.count < 20:
            self.y -= 0.7
        elif self.count >= 20 and self.count < 40:
            pass
        elif self.count >= 40:
            self.is_alive = False
    def draw(self):
        if self.type == 0:
            pyxel.text(self.x, self.y, f"+{self.score:2}", 13)
        elif self.type == 1:
            pyxel.text(self.x, self.y, f"HP+1", 13)
#■EnemyBullet
class EnemyBullet:
    def __init__(self, x, y, speed, dir,type, aim):
        self.x = x
        self.y = y
        self.new_bullet_x = x
        self.new_bullet_y = y
        self.speed = speed
        self.direction = dir    #1:右 -1:左 2:下
        self.size = 1
        self.color = 10         #colorは0～15
        self.count = 0
        self.count_missile = 0
        self.aim = aim          #攻撃角度
        self.type = type        #0:通常(左右) 1:通常(下) 2:エイム 3:グレネード弾 4:???
        self.is_alive = True
        enemybullets.append(self)
    def update(self):
        #位置を更新する前に衝突判定
        if self.type == 0:      #通常弾(左右)
            self.new_bullet_x = self.x + self.speed * self.direction
        elif self.type == 1:    #通常弾(下)
            self.new_bullet_y = self.y + self.speed
        elif self.type == 2:    #エイム
            #弾用座標
            self.new_bullet_x += self.speed * math.cos(self.aim)
            self.new_bullet_y += self.speed * -math.sin(self.aim)
        elif self.type == 3:    #グレネード弾
            pass
        #移動先でtileと当たり判定
        if self.type == 0:      #通常弾(左右)
            if check_bullet_collision(self.new_bullet_x, self.y) == True:
                self.x = round(self.x / 8) * 8 #丸めて着地
                #HitParticle
                hitparticles.append(
                    HitParticle(self.x, self.y)
                )
                self.is_alive = False   #タイル接触なら消去
            else:
                self.x = self.new_bullet_x
        elif self.type == 1:    #通常弾(下)
            if check_bullet_collision(self.x, self.new_bullet_y) == True:
                self.y = round(self.y / 8) * 8 #丸めて着地
                #HitParticle
                hitparticles.append(
                    HitParticle(self.x, self.y)
                )
                self.is_alive = False   #タイル接触なら消去
            else:
                self.y = self.new_bullet_y
        elif self.type == 2:    #エイム
            if check_bullet_collision(self.new_bullet_x, self.new_bullet_y) == True:
                self.x = round(self.x / 8) * 8 #丸めて着地
                self.y = round(self.y / 8) * 8 #丸めて着地
                #HitParticle
                hitparticles.append(
                    HitParticle(self.x, self.y)
                )
                self.is_alive = False   #タイル接触なら消去
            else:
                self.x = self.new_bullet_x
                self.y = self.new_bullet_y
        elif self.type == 3:    #グレネード弾
            pass

        self.count += 1
        #一定時間で消去
        if self.count > 360:
            self.is_alive = False   #消去
    def draw(self):
        if self.type == 0:
            pyxel.circ(self.x, self.y, 1, self.color)
        elif self.type == 1:
            pyxel.circ(self.x, self.y, 1, self.color)
        elif self.type == 2:
            pyxel.circ(self.x, self.y, 1, self.color)
#■Transpoter
class Transpoter:
    def __init__(self, x, y, speed, dir, hp, type, spawnNum):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.new_transpoter_y = y
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.type = type        #0:空中中型機 1:コンテナ
        self.speed = speed
        self.spawnNum = spawnNum#生成数
        self.gravity = GRAVITY
        self.moveCount = 0
        self.isGround = False
        self.is_alive = True
        transpoters.append(self)
    def update(self):
        #移動
        if self.type == 0:
            if self.moveCount < 35:
                self.dy += 0.1
                self.y += self.dy
                self.moveCount += 1
            elif self.moveCount >= 35 and self.moveCount < 1000:
                self.moveCount += 1
#                pass
            elif self.moveCount >= 1000 and self.moveCount < 1100:
                #画面外へ
                self.dy -= 0.2
                self.y += self.dy
                self.moveCount += 1
            elif self.moveCount >= 1100:
                #画面外で消去
                self.is_alive = False

        elif self.type == 1:
            #空中時処理
            if self.isGround == False:
                #加速度更新
                self.dy += self.gravity #重力加速度的な
            else:
                self.dy += 0 #変化なし
            #playerの位置を更新する前に衝突判定
            #y座標のみ空中時に計算
            if self.isGround == False:
                self.new_transpoter_y = self.y + self.dy
            #移動先での当たり判定
            #床判定
            if check_collision_yuka16(self.x, self.new_transpoter_y) == True:
                self.y = round(self.y / 8) * 8 #丸めて着地
                self.isGround = True
            else:
                self.isGround = False
                self.y = self.new_transpoter_y

        #グローバル変数宣言
        global g_enemy_spawn_num
        #生成
        if self.type == 0:
            if pyxel.frame_count % 180 == 0 and self.spawnNum > 0:
                Enemy(self.x + 4, self.y, 0.5, -1, 5, 0, 0)
                self.spawnNum -= 1
                g_enemy_spawn_num += 1
        elif self.type == 1:
            if pyxel.frame_count % 180 == 0 and self.spawnNum > 0 and self.isGround == True:
                Enemy(self.x + 4, self.y, 0.5, -1, 5, 0, 0)
                self.spawnNum -= 1
                g_enemy_spawn_num += 1

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
        pyxel.pset(self.x, self.y, 7)
#■Item
class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.dy = 0
        self.new_item_y = y
        self.gravity = GRAVITY
        self.type = type        #0:missile 1:laser 2:trap 3:hp
        self.getCount = 0       #出現直後に取得できないようにカウント用
        self.isGround = False
        self.is_alive = True
        items.append(self)
    def update(self):
        #空中時処理
        if self.isGround == False:
            #加速度更新
            self.dy += self.gravity #重力加速度的な
        else:
            self.dy += 0            #変化なし
        #位置を更新する前に衝突判定
        #y座標のみ空中時に計算
        if self.isGround == False:
            self.new_item_y = self.y + self.dy
        #移動先での当たり判定
        #床判定
        if check_collision_yuka(self.x, self.new_item_y) == True:
            self.y = round(self.y / 8) * 8 #丸めて着地
            self.isGround = True
        else:
            self.isGround = False
            self.y = self.new_item_y

    def draw(self):
        if self.type == 0:
            pyxel.blt(self.x, self.y, 0, 40, 32, 8, 8, 0)
        elif self.type == 1:
            pyxel.blt(self.x, self.y, 0, 48, 32, 8, 8, 0)
        elif self.type == 2:
            pyxel.blt(self.x, self.y, 0, 32, 32, 8, 8, 0)
        elif self.type == 3:
            pyxel.blt(self.x, self.y, 0, 56, 32, 8, 8, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="2D ACT", fps = 60)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource18.pyxres")
        self.score = 0
        self.highScore = 0
        self.enemyS_dead_num = 0    #普通enemyの破壊数
        self.enemyM_dead_num = 0    #中型機enemyの破壊数
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成(+1は着地座標調整、確定ではない)
        self.player = Player(36, pyxel.height / 2 + 1)

        #BG表示用の座標
        self.scroll_x = 0
        self.scroll_y = 0
        #playerのHP表示用の座標
        self.player_hp_X = 0
        #制御用flag
        self.isOnece1 = True  #中型機生成用
        self.isOnece2 = True  #浮遊enemy真下に攻撃生成用
        #仮配置
#        Enemy(96, pyxel.height / 2, 0.5, -1, 100, 4, 2)
#        Transpoter(64, -32, 2, -1, 20, 0, 5)

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
        elif self.scene == SCENE_HELP1:
            self.update_help1_scene()
        elif self.scene == SCENE_HELP2:
            self.update_help2_scene()
        elif self.scene == SCENE_HELP3:
            self.update_help3_scene()
        elif self.scene == SCENE_HELP4:
            self.update_help4_scene()

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)    #BGM再生
            self.scene = SCENE_PLAY
        #H_keyでヘルプ画面1に遷移
        if pyxel.btnr(pyxel.KEY_H):
#            pyxel.playm(0, loop = True)    #BGM再生
            self.scene = SCENE_HELP1

    #ゲーム画面処理用update
    def update_play_scene(self):
        #グローバル変数宣言
        global g_enemy_spawn_num
        #scoreで生成間隔を制御
        if self.score < 30:
            spawntime = 30
        elif self.score >= 30 and self.score < 70:
            spawntime = 25
        elif self.score >= 70:
            spawntime = 20
        """
        #左右からenemy生成
        if pyxel.frame_count % 120 == 0:
            if pyxel.rndi(0, 1) == 0:
                Enemy(0, 50, 0.5, 1, 3, 1, 0)
                g_enemy_spawn_num += 1
                pass
            else:
                Enemy(184, 50, 0.5, -1, 3, 1, 0)
                g_enemy_spawn_num += 1
                pass
        #生成数で中型機生成
        if g_enemy_spawn_num % 10 == 0:
            if self.isOnece1 == False:
                Transpoter(self.player.x + pyxel.rndi(0, 32), -32, 2, -1, 20, 0, 5)
                self.isOnece1 = True
        elif g_enemy_spawn_num % 10 == 1:
            self.isOnece1 = False
        #撃破数で浮遊enemy真下に攻撃を生成
        if self.enemyS_dead_num % 10 == 0:
            if self.isOnece2 == False:
                Enemy(self.player.x + pyxel.rndi(0, 32), -32, 0, -1, 3, 4, 1)
                self.isOnece2 = True
        elif self.enemyS_dead_num % 10 == 1:
            self.isOnece2 = False
        #停止で浮遊enemy生成
        if self.player.count_stop > 120:
            #位置ランダム
            if pyxel.rndi(0, 1) == 0:
                Enemy(self.player.x + pyxel.rndi(0, 32), -32, 0, -1, 3, 4, 2)
            else:
                Enemy(self.player.x - pyxel.rndi(0, 32), -32, 0, 1, 3, 4, 2)
            self.player.count_stop = 0
        """
        #Player制御
        self.player.update()
        #EnemyBulletとPlayerの当たり判定
        for enemybullet in enemybullets:
            if enemybullet.type == 0:    #通常弾(左右)
                if (self.player.x + 6  > enemybullet.x - 0 and
                    self.player.x + 2   < enemybullet.x + 2 and
                    self.player.y + 6  > enemybullet.y - 0 and
                    self.player.y + 2  < enemybullet.y + 2):
                    #Hit時の処理
                    self.player.hp -= 1
                    self.player.isHit = True
                    hitparticles.append(
                        HitParticle(enemybullet.x, enemybullet.y)
                    )
                    #Particle
                    for i in range(2):
                        particles.append(
                            Particle(enemybullet.x, enemybullet.y)
                        )
                    enemybullet.is_alive = False
    #                pyxel.play(3, 1, loop=False)    #SE再生
                    #player残りHP判定
                    if self.player.hp <= 0:
                        blasts.append(
                            Blast(enemybullet.x, enemybullet.y)
                        )
                        pyxel.stop()
                        self.scene = SCENE_GAMEOVER
            if enemybullet.type == 1:    #通常弾(下)
                if (self.player.x + 8  > enemybullet.x - 0 and
                    self.player.x + 0   < enemybullet.x + 2 and
                    self.player.y + 6  > enemybullet.y - 0 and
                    self.player.y + 2  < enemybullet.y + 2):
                    #Hit時の処理
                    self.player.hp -= 1
                    self.player.isHit = True
                    hitparticles.append(
                        HitParticle(enemybullet.x, enemybullet.y)
                    )
                    #Particle
                    for i in range(2):
                        particles.append(
                            Particle(enemybullet.x, enemybullet.y)
                        )
                    enemybullet.is_alive = False
    #                pyxel.play(3, 1, loop=False)    #SE再生
                    #player残りHP判定
                    if self.player.hp <= 0:
                        blasts.append(
                            Blast(enemybullet.x, enemybullet.y)
                        )
                        pyxel.stop()
                        self.scene = SCENE_GAMEOVER
            if enemybullet.type == 2:    #エイム弾
                if (self.player.x + 8  > enemybullet.x - 0 and
                    self.player.x + 0   < enemybullet.x + 2 and
                    self.player.y + 8  > enemybullet.y - 0 and
                    self.player.y + 0  < enemybullet.y + 2):
                    #Hit時の処理
                    self.player.hp -= 1
                    self.player.isHit = True
                    hitparticles.append(
                        HitParticle(enemybullet.x, enemybullet.y)
                    )
                    #Particle
                    for i in range(2):
                        particles.append(
                            Particle(enemybullet.x, enemybullet.y)
                        )
                    enemybullet.is_alive = False
    #                pyxel.play(3, 1, loop=False)    #SE再生
                    #player残りHP判定
                    if self.player.hp <= 0:
                        blasts.append(
                            Blast(enemybullet.x, enemybullet.y)
                        )
                        pyxel.stop()
                        self.scene = SCENE_GAMEOVER

        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if bullet.type == 0:    #通常弾
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
                                Particle(bullet.x, bullet.y)
                            )
                        bullet.is_alive = False
                        enemy.isHit = True
                        #残りHP判定
                        if enemy.hp <= 0 and enemy.is_alive == True:
                            self.enemyS_dead_num += 1
                            enemy.is_alive = False
                            blasts.append(
                                Blast(enemy.x, enemy.y)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(enemy.x, enemy.y)
                                )
                            #item出現はランダム
                            if pyxel.rndi(0, 3) == 0:
                                items.append(
                                    Item(enemy.x, enemy.y - 4, pyxel.rndi(0, 2))
                                )
                            self.score += 10
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 10, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生
                if bullet.type == 1:    #ミサイル弾
                    if (enemy.x + 8    > bullet.x and
                        enemy.x        < bullet.x + 8 and
                        enemy.y + 8    > bullet.y + 2 and
                        enemy.y        < bullet.y + 6):
                        #Hit時の処理
                        enemy.hp -= 1
                        #HitParticle
                        if bullet.isUp == False:
                            if bullet.direction == 1:
                                hitparticles.append(
                                    HitParticle(bullet.x + 8, bullet.y + 4)
                                )
                            else:
                                hitparticles.append(
                                    HitParticle(bullet.x, bullet.y + 4)
                                )
                        else:
                            hitparticles.append(
                                HitParticle(bullet.x + 4, bullet.y + 4)
                            )
                        #Particle
                        for i in range(2):
                            particles.append(
                                Particle(enemy.x + 4, enemy.y + 4)
                            )
                        bullet.is_alive = False
                        #残りHP判定
                        if enemy.hp <= 0 and enemy.is_alive == True:
                            self.enemyS_dead_num += 1
                            enemy.is_alive = False
                            blasts.append(
                                Blast(enemy.x, enemy.y)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(enemy.x + 4, enemy.y + 4)
                                )
                            #item出現はランダム
                            if pyxel.rndi(0, 3) == 0:
                                items.append(
                                    Item(enemy.x, enemy.y - 4, pyxel.rndi(0, 2))
                                )
                            self.score += 20
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 20, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生
                if bullet.type == 2:    #レーザー
                    if (enemy.x + 8    > bullet.x and
                        enemy.x        < bullet.x + 16 and
                        enemy.y + 8    > bullet.y + 2 and
                        enemy.y        < bullet.y + 6):
                        #Hit時の処理
                        enemy.hp -= 1
                        #HitParticle
                        hitparticles.append(
                            HitParticle(bullet.x + 4, bullet.y + 4)
                        )
                        #Particle
                        for i in range(2):
                            particles.append(
                                Particle(bullet.x + 4, bullet.y + 4)
                            )
                        #残りHP判定
                        if enemy.hp <= 0 and enemy.is_alive == True:
                            self.enemyS_dead_num += 1
                            enemy.is_alive = False
                            blasts.append(
                                Blast(enemy.x, enemy.y)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(enemy.x + 4, enemy.y + 4)
                                )
                            #item出現はランダム
                            if pyxel.rndi(0, 3) == 0:
                                items.append(
                                    Item(enemy.x, enemy.y - 4, pyxel.rndi(0, 2))
                                )
                            self.score += 30
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 30, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生
        #中型機とBulletの当たり判定
        for transpoter in transpoters:
            for bullet in bullets:
                if bullet.type == 0:    #通常弾
                    if (transpoter.x + 16    > bullet.x - 2 and
                        transpoter.x        < bullet.x + 2 and
                        transpoter.y + 16    > bullet.y - 2 and
                        transpoter.y        < bullet.y + 2):
                        #Hit時の処理
                        transpoter.hp -= 1
                        #HitParticle
                        hitparticles.append(
                            HitParticle(bullet.x, bullet.y)
                        )
                        #Particle
                        for i in range(2):
                            particles.append(
                                Particle(bullet.x, bullet.y)
                            )
                        bullet.is_alive = False
                        #残りHP判定
                        if transpoter.hp <= 0 and transpoter.is_alive == True:
                            self.enemyM_dead_num += 1
                            transpoter.is_alive = False
                            blasts.append(
                                Blast(transpoter.x + 4, transpoter.y + 4)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(transpoter.x + 8, transpoter.y + 8)
                                )
                            self.score += 40
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 40, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生
                if bullet.type == 1:    #ミサイル弾
                    if (transpoter.x + 16    > bullet.x and
                        transpoter.x        < bullet.x + 8 and
                        transpoter.y + 16    > bullet.y + 2 and
                        transpoter.y        < bullet.y + 6):
                        #Hit時の処理
                        transpoter.hp -= 1
                        #HitParticle
                        if bullet.isUp == False:
                            if bullet.direction == 1:
                                hitparticles.append(
                                    HitParticle(bullet.x + 8, bullet.y + 4)
                                )
                            else:
                                hitparticles.append(
                                    HitParticle(bullet.x, bullet.y + 4)
                                )
                        else:
                            hitparticles.append(
                                HitParticle(bullet.x + 4, bullet.y + 4)
                            )
                        #Particle
                        for i in range(2):
                            if bullet.isUp == False:
                                if bullet.direction == 1:
                                    particles.append(
                                        Particle(bullet.x + 8, bullet.y + 4)
                                    )
                                else:
                                    hitparticles.append(
                                        Particle(bullet.x, bullet.y + 4)
                                    )
                            else:
                                hitparticles.append(
                                    Particle(bullet.x + 4, bullet.y + 4)
                                )
                        bullet.is_alive = False
                        #残りHP判定
                        if transpoter.hp <= 0 and transpoter.is_alive == True:
                            self.enemyM_dead_num += 1
                            transpoter.is_alive = False
                            blasts.append(
                                Blast(transpoter.x + 4, transpoter.y + 4)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(transpoter.x + 8, transpoter.y + 8)
                                )
                            self.score += 50
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 50, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生
                if bullet.type == 2:    #レーザー
                    if (transpoter.x + 16    > bullet.x and
                        transpoter.x        < bullet.x + 16 and
                        transpoter.y + 16    > bullet.y + 2 and
                        transpoter.y        < bullet.y + 6):
                        #Hit時の処理
                        transpoter.hp -= 1
                        #HitParticle
                        if bullet.isUp == False:
                            hitparticles.append(
                                HitParticle(bullet.x, bullet.y + 4)
                            )
                        else:
                            hitparticles.append(
                                HitParticle(bullet.x + 4, bullet.y + 4)
                            )
                        #Particle
                        for i in range(2):
                            if bullet.isUp == False:
                                if bullet.direction == 1:
                                    particles.append(
                                        Particle(bullet.x + 8, transpoter.y + 8)
                                    )
                                else:
                                    hitparticles.append(
                                        Particle(bullet.x, transpoter.y + 8)
                                    )
                            else:
                                particles.append(
                                    Particle(bullet.x + 4, bullet.y + 4)
                                )
                        #残りHP判定
                        if transpoter.hp <= 0 and transpoter.is_alive == True:
                            self.enemyM_dead_num += 1
                            transpoter.is_alive = False
                            blasts.append(
                                Blast(transpoter.x + 4, transpoter.y + 4)
                            )
                            #Particle
                            for i in range(10):
                                particles.append(
                                    Particle(transpoter.x + 8, transpoter.y + 8)
                                )
                            self.score += 60
                            enemiesUI.append(
                                EnemyUI(enemy.x, enemy.y, 60, 0)
                            )
#                        pyxel.play(1, 0, loop=False)    #SE再生

        #EnemyとPlayer踏みつけ処理(当たり判定は調整必要)
        for enemy in enemies:
            if (self.player.x + 7 > enemy.x + 0 and
                self.player.x + 0 < enemy.x + 7 and
                self.player.y + 8 > enemy.y and
                self.player.y + 7 < enemy.y):
                if enemy.is_alive == True:
                    #Hit時の処理
                    self.player.isStepOn = True
                    #HP回復item出現はランダム
                    if pyxel.rndi(0, 3) == 0:
                        items.append(
                            Item(enemy.x, enemy.y - 4, 3)
                        )
                    self.enemyS_dead_num += 1
                    enemiesUI.append(
                        EnemyUI(enemy.x, enemy.y, 0, 0)
                    )
                    enemy.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

        #ItemとPlayerの処理
        for item in items:
            if (self.player.x + 8  > item.x + 0 and
                self.player.x + 0  < item.x + 8 and
                self.player.y + 8  > item.y + 0 and
                self.player.y + 0  < item.y + 8):
                if item.is_alive == True:
                    item.getCount += 1
                    if item.getCount > 10:   #出現直後は取得不可
                        #Hit時の処理
                        if item.type == 0:
                            self.player.zandan_missile += 1
                        elif item.type == 1:
                            self.player.zandan_laser += 1
                        elif item.type == 2:
                            #コンテナ生成
                            Transpoter(item.x, -32, 2, -1, 20, 1, 3)
                        elif item.type == 3:
                            self.player.hp += 1
                            enemiesUI.append(
                                EnemyUI(item.x, item.y, 0, 1)
#                                EnemyUI(enemy.x, enemy.y, 0, 1)
                            )
                        item.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

        #EnemyのPlayer狙い処理
        for enemy in enemies:
            #攻撃タイミング
            if enemy.isFire == True:
                dx = self.player.x - enemy.x
                dy = self.player.y - enemy.y
                enemy.aim = math.atan2(-dy, dx)
                #敵弾生成
                EnemyBullet(enemy.x + 4, enemy.y + 8, ENEMY_BULLET_SPEED, 2, enemy.atkType, enemy.aim)
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
        update_list(enemybullets)
        update_list(bullets)
        update_list(hitparticles)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(particles)
        update_list(transpoters)
        update_list(items)
        #list更新
        cleanup_list(enemybullets)
        cleanup_list(bullets)
        cleanup_list(hitparticles)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(particles)
        cleanup_list(transpoters)
        cleanup_list(items)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #グローバル変数宣言
        global g_enemy_spawn_num
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.player.hp = 10
            g_enemy_spawn_num = 0       #enemyの生成数
            self.enemyS_dead_num = 0    #普通enemyの破壊数
            self.enemyM_dead_num = 0    #中型機enemyの破壊数
            self.scene = SCENE_TITLE
            #list全要素削除
            enemybullets.clear()    #list全要素削除
            bullets.clear()         #list全要素削除
            hitparticles.clear()    #list全要素削除
            enemies.clear()         #list全要素削除
            enemiesUI.clear()       #list全要素削除
            blasts.clear()          #list全要素削除
            particles.clear()       #list全要素削除
            transpoters.clear()     #list全要素削除
            items.clear()     #list全要素削除

    #ヘルプ画面1処理用update
    def update_help1_scene(self):
        #Hでヘルプ画面2に遷移
        if pyxel.btnr(pyxel.KEY_H):
            self.scene = SCENE_HELP2

    #ヘルプ画面2処理用update
    def update_help2_scene(self):
        #Hでヘルプ画面3に遷移
        if pyxel.btnr(pyxel.KEY_H):
            self.scene = SCENE_HELP3

    #ヘルプ画面3処理用update
    def update_help3_scene(self):
        #Hでヘルプ画面4に遷移
        if pyxel.btnr(pyxel.KEY_H):
            self.scene = SCENE_HELP4

    #ヘルプ画面4処理用update
    def update_help4_scene(self):
        #Hでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_H):
            self.scene = SCENE_TITLE

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
        elif self.scene == SCENE_HELP1:
            self.draw_help1_scene()
        elif self.scene == SCENE_HELP2:
            self.draw_help2_scene()
        elif self.scene == SCENE_HELP3:
            self.draw_help3_scene()
        elif self.scene == SCENE_HELP4:
            self.draw_help4_scene()

        #score表示(f文字列的な)
#        pyxel.text(4, 4, f"SCORE {self.score:5}", 7)
#        pyxel.text(60, 4, f"HIGH SCORE {self.highScore:5}", 6)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.blt(0, 8, 0, 0, 96, 128, 32, 0)
        pyxel.text(0, 52, "--------------------------------", 7)
        pyxel.text(20, 58, "- START PRESS ENTER -", 9)
        pyxel.text(0, 64, "--------------------------------", 7)
        pyxel.text(20, 100, "HOW TO PLAY PRESS H KEY", 7)
        self.player.draw()

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #BG描画
        pyxel.bltm(0, 0, 0, self.scroll_x, self.scroll_y, 128, 128, 0)
        #camera再セット
        pyxel.camera(self.scroll_x, self.scroll_y)

        draw_list(items)
        draw_list(enemiesUI)
        self.player.draw()
        draw_list(enemybullets)
        draw_list(bullets)
        draw_list(enemies)
        draw_list(transpoters)
        draw_list(hitparticles)
        draw_list(blasts)
        draw_list(particles)
        
        pyxel.camera()  #左上隅の座標を(0, 0)にリセット処理,UIの位置固定
        #debug UI
        pyxel.text(0,   0, "isWall:%s" %self.player.isWall, 7)
        pyxel.text(0,   6, "isGround:%s" %self.player.isGround, 7)
        pyxel.text(0,  12, "isJump:%s" %self.player.isJump, 7)
        pyxel.text(0,  18, "ene_S:%i" %self.enemyS_dead_num, 7)
        pyxel.text(0,  24, "ene_M:%i" %self.enemyM_dead_num, 7)
        pyxel.text(0,  30, "spawn:%i" %g_enemy_spawn_num, 7)
#        pyxel.text(0,  24, "    y:%f" %self.player.y, 7)
#        pyxel.text(0,  30, "spawn:%i" %g_enemy_spawn_num, 7)
#        pyxel.text(0,  30, "   dy:%f" %self.player.dy, 7)

        #player HP UI
        if self.player.x < RIGHT_LIMIT:
            self.player_hp_X = self.player.x
        elif self.player.x >= RIGHT_LIMIT and self.player.x <= 128:
            self.player_hp_X = RIGHT_LIMIT
        elif self.player.x > 128:
            self.player_hp_X = self.player.x - RIGHT_LIMIT 
        pyxel.text(self.player_hp_X - 4,  self.player.y - 6, "HP:%i" %self.player.hp, 7)

        #UI
        #残段数
        pyxel.text(60, 114, "%i" %self.player.zandan_missile, 7)
        pyxel.text(70, 114, "%i" %self.player.zandan_laser, 7)
        #武器icon
        if self.player.atk_type == 0:
            pyxel.blt(50, 120, 0, 32, 24, 8, 8, 0)
            pyxel.blt(60, 120, 0, 40, 16, 8, 8, 0)
            pyxel.blt(70, 120, 0, 48, 16, 8, 8, 0)
        elif self.player.atk_type == 1:
            pyxel.blt(50, 120, 0, 32, 16, 8, 8, 0)
            pyxel.blt(60, 120, 0, 40, 24, 8, 8, 0)
            pyxel.blt(70, 120, 0, 48, 16, 8, 8, 0)
        else:
            pyxel.blt(50, 120, 0, 32, 16, 8, 8, 0)
            pyxel.blt(60, 120, 0, 40, 16, 8, 8, 0)
            pyxel.blt(70, 120, 0, 48, 24, 8, 8, 0)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)

    #ヘルプ画面1描画用update
    def draw_help1_scene(self):
#        pyxel.text(0, 0, "01234567890123456789012345678901", 7)
        pyxel.text(44, 3, "NEXT:H KEY", 3)
        pyxel.text(96, 3, "PAGE 1/4", 10)
        pyxel.text(1, 12, "BASIC ACTION:", 9)

        pyxel.text(30, 30, "MOVE & SHOT", 7)
        pyxel.blt(  4, 28, 0, 0, 56, 16, 8, 0)

        pyxel.text(30, 48, "JUMP", 7)
        pyxel.text(2, 48, "SPACE", 6)
        pyxel.blt(  0, 46, 0, 0, 64, 24, 8, 0)

        pyxel.text(30, 66, "WEAPON CHANGE", 7)
        pyxel.blt(  7, 64, 0, 24, 56, 8, 8, 0)

        pyxel.text(1, 84, "STOMP ACTION:", 9)
        pyxel.blt(  1, 93, 0, 8, 72, 32, 32, 0)

#        pyxel.text(32, 112, "- PRESS H -", 7)

    #ヘルプ画面2描画用update
    def draw_help2_scene(self):
        pyxel.text(44, 3, "NEXT:H KEY", 3)
        pyxel.text(96, 3, "PAGE 2/4", 10)

        pyxel.text(18, 12, "NORMAL BULLET", 9)
        pyxel.blt(  4, 10, 0, 48, 8, 8, 8, 0)
        pyxel.text(26, 21, "WEAK", 7)
        pyxel.text(26, 30, "CAN ATTACK INFINITELY", 7)

        pyxel.text(18, 48, "MISSILE", 9)
        pyxel.blt(  4, 46, 0, 0, 8, 8, 8, 0)
        pyxel.text(26, 57, "VERY STRONG", 7)
        pyxel.text(26, 66, "HAS AMMO", 7)

        pyxel.text(18, 84, "LASER", 9)
        pyxel.blt(  0, 82, 0, 48, 0, 16, 8, 0)
        pyxel.text(26, 93, "STRONG. PIERCES", 7)
        pyxel.text(26, 102, "HAS AMMO", 7)

#        pyxel.text(32, 112, "- PRESS H -", 7)

    #ヘルプ画面3描画用update
    def draw_help3_scene(self):
        pyxel.text(44, 3, "NEXT:H KEY", 3)
        pyxel.text(96, 3, "PAGE 3/4", 10)

        pyxel.text(18, 12, "MISSILE ITEM", 9)
        pyxel.blt(  4, 10, 0, 40, 32, 8, 8, 0)
        pyxel.text(26, 21, "ADDS ONE MISSILE AMMO", 7)

        pyxel.text(18, 39, "LASER ITEM", 9)
        pyxel.blt(  4, 37, 0, 48, 32, 8, 8, 0)
        pyxel.text(26, 48, "ADDS ONE LASER AMMO", 7)

        pyxel.text(18, 66, "RECOVERY ITEM", 9)
        pyxel.blt(  4, 64, 0, 56, 32, 8, 8, 0)
        pyxel.text(26, 75, "RECOVERS ONE HP", 7)

        pyxel.text(18, 93, "TRAP ITEM", 9)
        pyxel.blt(  4, 91, 0, 32, 32, 8, 8, 0)
        pyxel.text(26, 102, "A CONTAINER FULL OF", 7)
        pyxel.text(26, 111, "ENEMIES WILL APPEAR", 7)

    #ヘルプ画面4描画用update
    def draw_help4_scene(self):
        pyxel.text(44, 3, "NEXT:H KEY", 3)
        pyxel.text(96, 3, "PAGE 4/4", 10)
        pyxel.text(1, 12, "HINT1:", 9)
        pyxel.text(26, 12, "YOU CAN'T ATTACK LEFT OR", 7)
        pyxel.text(1, 21, "RIGHT IF YOU DON'T MOVE", 7)

        pyxel.text(1, 39, "HINT2:", 9)
        pyxel.text(26, 39, "GAME OVER WHEN HP IS ZERO", 7)

        pyxel.text(1, 57, "HINT3:", 9)
        pyxel.text(26, 57, "WHEN YOU DEFEAT AN ENEMY", 7)
        pyxel.text(1, 66, "WITH AN ATTACK, THEY WILL SOME-", 7)
        pyxel.text(1, 75, "TIMES DROP MISSILE OR LASER", 7)
        pyxel.text(1, 84, "ITEMS", 7)

        pyxel.text(1, 102, "HINT4:", 9)
        pyxel.text(26, 102, "WHEN YOU STOMP ON AN", 7)
        pyxel.text(1, 111, "ENEMY, THEY WILL SOMETIMES DROP", 7)
        pyxel.text(1, 120, "A RECOVERY ITEM", 7)
App()