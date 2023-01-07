import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(120, 160, title="Pysel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
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
        pass

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    #ゲーム画面処理用update
    def update_play_scene(self):
		#playerの更新処理
        self.update_player()

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_TITLE

	#player処理
    def update_player(self):
        # key入力
		# (画面遷移用の仮入力)
        if pyxel.btnr(pyxel.KEY_RETURN):
            #ENTERでゲームオーバー画面に遷移
            self.scene = SCENE_GAMEOVER

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
        #editorデータ描画(player)
        pyxel.blt(0, 144, 0, 0, 0, 16, 16, 0)
            #描画座標(左上のX座標)
            #描画座標(左上のY座標)
            #画像番号
            #切り出しの左上のX座標
            #切り出しの左上のY座標
            #切り出す幅
            #切り出す高さ
            #抜き色(パレット番号)

        #text表示(x座標、y座標、文字列、color)
        pyxel.text(5, 4, "test", 7)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(55, 40, "GAME OVER", 7)
        pyxel.text(50, 80, "- PRESS ENTER -", 7)

        pass
App()