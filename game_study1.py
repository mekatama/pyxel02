import pyxel
WINDOW_H = 120
WINDOW_W = 160

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        #マウスカーソル表示
        pyxel.mouse(False)
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新関数
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

	#描画関数
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #テキスト表示(colorが周期的に変わる)
        pyxel.text(55, 40, "Are you Kururu?", pyxel.frame_count % 16)
            #描画座標(左上のX座標) #描画座標(左上のY座標)
            #画像番号
            #切り出しの左上のX座標 #切り出しの左上のY座標
            #切り出す幅           #切り出す高さ
            #抜き色(パレット番号)
        #cat関数呼び出し
        self.cat()
    
    #cat関数
    def cat(self):
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        #mouse左クリックで反転表示
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
           #editorデータ描画(player)
            pyxel.blt(x, y, 0, 0, 0, -16, 16, 0)
        else:
            pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)



App()