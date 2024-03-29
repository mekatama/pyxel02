#ジャンプアクション01
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
STAGE_W = 128 * 2
SAGE_H = 128 * 1
LEFT_LIMIT = 40
RIGHT_LIMIT = WINDOW_W - 40 #調整項目
TILE_SIZE = 8
MAP_WIDTH = 16
MAP_HEIGHT = 16
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
scroll_y = 0    #画面スクロール制御
#list用意
bullets = []
enemies = []
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
            if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                self.dx = 1
                self.direction = 1  #右向き
            if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dx = -1
                self.direction = -1 #左向き
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
            if self.direction == 1:
                Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == -1:
                Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
        #Playerの位置を更新
        new_player_x = self.x + self.dx
        new_player_y = self.y + self.dy
        #移動先で当たり判定
        #左右
        if check_collision(new_player_x, self.y) == False:
            self.x = new_player_x   #左右に障害物が無いので座標更新
        #床
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
        self.count += 0
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
        #移動先で当たり判定
        if check_bullet_collision(self.x, self.y) == True:
            self.is_alive = False   #タイル接触なら消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

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
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource06.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 -8, pyxel.height / 2 -8)

        #仮
        Enemy(64, 112, 0, 0,3)

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
                    bullet.is_alive = False
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
        update_list(blasts)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
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
            #list全要素削除
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            blasts.clear()                     #list全要素削除

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

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #BG描画
        pyxel.bltm(0, 0, 0, self.scroll_x, self.scroll_y, 128, 128, 0)
        #camera再セット
        pyxel.camera(self.scroll_x, self.scroll_y)

        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(blasts)
        #debug表示(f文字列的な)
        pyxel.text(0, 0, f"isJump {self.player.isJump}", 7)
        pyxel.text(0, 8, f"isGround {self.player.isGround}", 7)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
App()