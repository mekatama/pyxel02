import pyxel
 
class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(120, 160, title="Pysel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        #playerのx座標初期化
        self.x = 0
        #playerの移動方向flag
        self.isRight = True
        #playerの停止flag
        self.isStop = False
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新関数
    def update(self):
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
        pass

	#描画関数
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #editorデータ描画(player)
        pyxel.blt(self.x, 144, 0, 0, 0, 16, 16, 0)
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
        pass
App()