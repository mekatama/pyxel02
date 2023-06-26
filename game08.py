#ジャンプアクション01
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
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
#list用意
bullets = []

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
#        print("wall_左上")
        isStop = True
        return isStop
    #右上判定
    if get_tile(x2,y1) == (1,0):
#        print("wall_右上")
        isStop = True
        return isStop
    #左下判定
    if get_tile(x1,y2) == (1,0):
#        print("wall_左下")
        isStop = True
        return isStop
    #右下判定
    if get_tile(x2,y2) == (1,0):
#        print("wall_右下")
        isStop = True
        return isStop
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
        self.direction = 1
        self.isStop = False
        self.isJump = False
        self.isGround = False
        self.jumpHeight = 20
        self.jumpCount = 0
        self.is_alive = True
    def update(self):
        #移動入力
        if self.isStop == False:
            if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dx = -1
#                self.direction = -1
            if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                self.dx = 1
#                self.direction = 1
#            if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
#                self.dy = -1
#            if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
#                self.dy = 1
        #jump入力
        if (pyxel.btnp(pyxel.KEY_SPACE) and (self.isJump == False) and (self.isGround == True)):
            self.isJump = True
            self.isGround = False
        #jump挙動
        if self.isJump == True:
            #jump中処理
            if self.jumpCount < self.jumpHeight:
                self.y -= 2 #上に移動
                self.jumpCount += 1
                #jump中の頭上当たり判定
                if check_collision(self.x, self.y) == True:
                    self.isJump = False
                    self.dy = 2 #強引に下降させてメリコミ回避
        else:
            self.jumpCount = 0  #初期化

        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A):
            Bullet(self.x, self.y, PLAYER_BULLET_SPEED)

        #Playerの位置を更新
        new_player_x = self.x + self.dx
        new_player_y = self.y + self.dy
        #移動先で当たり判定
        if check_collision(new_player_x, self.y) == False:
            self.x = new_player_x   #左右に障害物が無いので座標更新

        if check_collision(self.x, new_player_y) == False:
            self.y = new_player_y   #足元に障害物が無いので座標更新
            self.isGround = False   #つまり地面にいない状態
        else:   #床的なところに接触
            self.isGround = True
            self.isJump = False

        #移動停止
        self.dx = 0
        self.dy = 1 #重力加速度的な

    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 0)

class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 1
        self.color = 10 #colorは0～15
        self.is_alive = True
        bullets.append(self)
    def update(self):
        self.x += self.speed        #弾移動
        if self.x > 150:            #画面外判定
            self.is_alive = False   #画面外なら消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource06.pyxres")
        self.score = 0
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
        #Player制御
        self.player.update()

        #list実行
        update_list(bullets)
        #list更新
        cleanup_list(bullets)

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

        #debug表示(f文字列的な)
        pyxel.text(0, 0, f"isJump {self.player.isJump}", 7)
        pyxel.text(0, 8, f"isGround {self.player.isGround}", 7)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
App()