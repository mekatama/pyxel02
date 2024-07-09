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

#関数(タイルとのBulletコリジョン判定)
    #//は商を求める(余りは切り捨てる)
def check_bullet_collision(x, y):
    x1 = x // 8             #キャラx座標左端のTileMapの座標
    y1 = y // 8             #キャラy座標上端のTileMapの座標
    x2 = (x - 1) // 8   #キャラx座標右端のTileMapの座標
    y2 = (y - 1) // 8   #キャラy座標下端のTileMapの座標
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
        self.gravity = GRAVITY
        self.hp = PLAYER_HP
        self.direction = 1
        self.isGround = False
        self.isJump = False
        self.isWall = False
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
        #jump入力
        if (pyxel.btnp(pyxel.KEY_SPACE) and (self.isJump == False) and (self.isGround == True)):
            self.dy = -1.5
            self.isJump = True
            self.isGround = False
        #攻撃入力
        #一定時間で自動射撃
        if pyxel.frame_count % 12 == 0:
            if self.direction == 1:
                Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == -1:
                Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction)

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
    def __init__(self, x, y, speed, dir):
        self.x = x
        self.y = y
        self.new_bullet_x = x
        self.new_bullet_y = y
        self.speed = speed
        self.direction = dir
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.is_alive = True
        bullets.append(self)
    def update(self):
        #位置を更新する前に衝突判定
        self.new_bullet_x = self.x + self.speed * self.direction
        #移動先でtileと当たり判定
        if check_bullet_collision(self.new_bullet_x, self.y) == True:
            #HitParticle
            hitparticles.append(
                HitParticle(self.x, self.y)
            )
            self.is_alive = False   #タイル接触なら消去
        else:
            self.x = self.new_bullet_x

#        self.x += self.speed * self.direction        #弾移動
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        pyxel.pset(self.x, self.y, self.color)

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
        self.player = Player(36, pyxel.height / 2 + 1)

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
        #list更新
        cleanup_list(bullets)
        cleanup_list(hitparticles)

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
        draw_list(hitparticles)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()