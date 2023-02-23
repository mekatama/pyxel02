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
bullets = []
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
        self.isRight = True #playerの方向flag
        self.is_alive = True
    def update(self):
        #key入力(攻撃)
        if pyxel.btnp(pyxel.KEY_D):
            self.isRight = True
            #弾生成
#            Bullet(self.x + 8, self.y - 8)
        if pyxel.btnp(pyxel.KEY_A):
            self.isRight = False
            #弾生成
#            Bullet(self.x + 8, self.y - 8)
    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 2
        self.color = 10 #colorは0～15
        self.is_alive = True
        bullets.append(self)
    def update(self):
        self.y -= BULLET_SPEED      #弾移動
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

class Enemy:
    def __init__(self, x, y, hp, img):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.is_alive = True
        enemies.append(self)
    def update(self):
        self.x += ENEMY_SPEED           #敵移動
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16 * self.img, 0, 16, 16, 0)

#ゲーム管理
class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        self.scene = SCENE_TITLE
        self.score = 0
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


        #Player制御
        self.player.update()
        #list実行
        update_list(bullets)
        update_list(enemies)
        #list更新
        cleanup_list(enemies)
        cleanup_list(bullets)

    #Gameover画面制御
    def update_gameover_scene(self):
        update_list(bullets)
        update_list(enemies)
        cleanup_list(enemies)
        cleanup_list(bullets)
        #ボタン入力で再play
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2     #初期位置
            self.player.y = pyxel.height - 20   #初期位置
            self.player.isRight = True          #flag初期化
            self.player.hp = 3                  #HP初期化
            self.score = 0
            enemies.clear()                     #list全要素削除
            bullets.clear()                     #list全要素削除

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
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        pyxel.text(self.player.x, 134, f"HP:{self.player.hp:1}", 13)

    def draw_gameover_scene(self):
        draw_list(bullets)
        draw_list(enemies)
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

App()