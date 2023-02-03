import pyxel
WINDOW_H = 120
WINDOW_W = 160

#xy座標用
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Player用
class player:
    def __init__(self):
        #Vec2クラス内でself.x=0 self.y=0と処理されてるっぽい
        self.pos = Vec2(0, 0)
        self.vec = 0    #向き(ベクトル)

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

#ゲーム管理
class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        #Playerインスタンス生成
        self.mPlayer = player()
        #マウスカーソル表示
        pyxel.mouse(False)
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        #Playerクラス更新
        dx = pyxel.mouse_x - self.mPlayer.pos.x #x軸方向の移動量
        dy = pyxel.mouse_y - self.mPlayer.pos.y #y軸方向の移動量
        #移動量判定
        if dx != 0:
            self.mPlayer.update(pyxel.mouse_x, pyxel.mouse_y, dx)   #移動と向き変更
        elif dy != 0:   #真上or真下に移動
            self.mPlayer.update(pyxel.mouse_x, pyxel.mouse_y, 0)   #移動のみ変更

	#描画
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #テキスト表示(colorが周期的に変わる)
        pyxel.text(55, 40, "Are you Kururu?", pyxel.frame_count % 16)
        #player向き判定
        if self.mPlayer.vec > 0:    #右向き
            #editorデータ描画(player)
            pyxel.blt(self.mPlayer.pos.x, self.mPlayer.pos.y, 0, 0, 0, 16, 16, 0)
        else:                       #左向き
            pyxel.blt(self.mPlayer.pos.x, self.mPlayer.pos.y, 0, 0, 0, -16, 16, 0)

            #描画座標(左上のX座標) #描画座標(左上のY座標)
            #画像番号
            #切り出しの左上のX座標 #切り出しの左上のY座標
            #切り出す幅           #切り出す高さ
            #抜き色(パレット番号)

App()