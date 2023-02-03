import pyxel
#ランダム使用
from random import randint
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面

class Player:
    def __init__(self):
        #playerのx座標初期化
        self.x = 0
        #playerの移動方向flag
        self.isRight = True
        #playerの停止flag
        self.isStop = False

    def update(self):
        # key入力
		# (画面遷移用の仮入力)
        if pyxel.btnr(pyxel.KEY_RETURN):
            #ENTERでゲームオーバー画面に遷移
            self.scene = SCENE_GAMEOVER
        #key入力(player停止)
        if pyxel.btn(pyxel.KEY_A):
            #押したら
            self.isStop = True
        elif pyxel.btnr(pyxel.KEY_A):
            #離したら
            self.isStop = False

        #playerの移動方向判定
        if self.x <= 0:
            self.isRight = True
        elif self.x >= 104:
            self.isRight = False
	    #playerの往復移動
        if self.isStop == False:
            if self.isRight == True:
                self.x = (self.x + 1)
            elif self.isRight == False:
                self.x = (self.x - 1)
#        if pyxel.frame_count % 16 == 0 and self.isOut == True:
        if pyxel.frame_count % 16 == 0:
            Bullet(self.x, self.y)

    def draw(self):
        pyxel.blt(self.x, 144, 0, 0, 0, 16, 16, 0)

    pass

class Bullet:
    def __init__(self, x, y):
        #(仮)bulletの初期位置
        self.x = x
        self.y = y
        #(仮)bullet用flag
        self.isShot = False
        self.isOut = True

    def update(self):
        #(仮)時間と画面外でisShot = Trueにする
#        if pyxel.frame_count % 16 == 0 and self.isOut == True:
#            self.isShot = True
#            self.isOut = False
#            #発射時のx座標はplayerの座標から
#            self.x = self.player_x
        #bullet発射
#        if self.isShot == True:
            #bulletが上に移動するだけ
        self.y = (self.y - 1) % pyxel.height
        #bullet画面外判定
#        if self.y <= 0:
#            self.isOut = True

    def draw(self):
#       if self.isShot == True:
        pyxel.blt(120, self.y, 0, 32, 0, 16, 16, 0)

        pass

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(120, 160, title="Pysel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")

        #生成(クラス対応)
        self.players = Player()
        self.bullets = Bullet()

        #画面遷移の初期化
        self.scene = SCENE_TITLE
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
            self.scene = SCENE_PLAY

    #ゲーム画面処理用update
    def update_play_scene(self):
		#更新処理(クラス対応)
        self.players.update()
        self.bullets.update()

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_TITLE

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
        pyxel.text(70, 40, "Title", 7)
        pyxel.text(50, 80, "- PRESS ENTER -", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #描画(クラス対応)
        self.players.draw()
        self.bullets.draw()

        #text表示(x座標、y座標、文字列、color)
        pyxel.text(5, 4, "test", 7)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(55, 40, "GAME OVER", 7)
        pyxel.text(50, 80, "- PRESS ENTER -", 7)

        pass
App()