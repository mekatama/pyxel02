#ベルトスクロール多重強制スクロール
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 64
WINDOW_W = 128
PLAYER_SPEED = 1
ENEMY_SPEED = 0.5
PLAYER_BULLET_SPEED = 2
#list用意
player = None
playerbullets = []
enemies = []
blasts = []

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
        self.direction = 1  #playerの向き
        self.isAtk = True   #playerの攻撃flag
        self.motion = 0   #playerのmotion(歩行motion制御用)
        self.count = 0      #時間計測用
        self.aniCount = 0   #アニメ用カウント
        self.is_alive = True
    def update(self):
        self.aniCount += 1
        #歩行アニメ切り替え
        if self.aniCount % 4 == 0: #一定時間表示
            if self.motion == 0:
                self.motion = 1
            elif self.motion == 1:
                self.motion = 0
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A):
            #弾生成
            if self.direction == 1:
                PlayerBullet(self.x + 13, self.y, 1)
#                PlayerBullet(self.x + 13, self.y + 13, 1)
            elif self.direction == -1:
                PlayerBullet(self.x - 1,  self.y, -1)
#                PlayerBullet(self.x - 1,  self.y + 13, -1)
        #移動入力
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.x >= 2:
                self.x -= PLAYER_SPEED
                self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.x <= WINDOW_W - 18:
                self.x += PLAYER_SPEED
                self.direction = 1
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.y >= 16:
                self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.y <= WINDOW_H - 20:
                self.y += PLAYER_SPEED
    def draw(self):
        #editorデータ描画(player)
        if self.isAtk == True:
            pyxel.blt(self.x, self.y, 0, 16 * self.motion, 0, 16 * self.direction, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 16, 16 * self.direction, 16, 0)

#■PlayerBullet
class PlayerBullet:
    def __init__(self, x, y, dir):
        self.x = x
#        self.y = y + 13 #描画順のため数値補正
        self.y = y
        self.size = 2
        self.direction = dir    #移動の向き
        self.color = 10         #colorは0～15
        self.count = 0          #時間計測用
        self.is_alive = True
        playerbullets.append(self)
    def update(self):
        self.count += 1
        #移動
        if self.direction == 1:
            self.x += PLAYER_BULLET_SPEED
        if self.direction == -1:
            self.x-= PLAYER_BULLET_SPEED
        #一定時間表示(8がよさそう)
        if self.count > 60:
            self.is_alive = False       #消去
    def draw(self):
        #見た目
        pyxel.rect(self.x, self.y + 6, 4, 3, 10)
        pyxel.rectb(self.x, self.y + 6, 4, 3, 1)
        #collision
        pyxel.rectb(self.x, self.y + 13, 4, 3, 10)

#■Enemy
class Enemy:
    def __init__(self, x, y, hp, img, speed ,dir):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.speed = speed
        self.dir = dir
        self.is_Move = True
        self.hitStopCount = 0
        self.is_alive = True
        enemies.append(self)
    def update(self):
        #移動
        if self.is_Move == True:
            if self.dir == -1:
                self.x += ENEMY_SPEED
            elif self.dir == 1:
                self.x -= ENEMY_SPEED
        #ヒットストップ
        else:
            self.hitStopCount += 1
            if self.hitStopCount >= 20:
                self.is_Move = True
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 16 * self.dir, 16, 0)
        #当たり判定
        pyxel.rectb(self.x + 4, self.y + 13, 8, 3, 5)

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
        pyxel.blt(self.x, self.y, 0, 0, 32 + (16 * self.motion), 16, 16, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base", fps = 60, display_scale = 5)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource09.pyxres")
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
        #一定時間でenemy出現判定
        if pyxel.frame_count % 30 == 0:
            #生成辺(位置)ランダム
            spawn_side = pyxel.rndi(0, 1)
            #生成座標ランダム
            if spawn_side == 0:     #左端
                spawn_x = -32
                spawn_y = pyxel.rndi(24, 70)
                spawn_dir = -1
            elif spawn_side == 1:   #右端
                spawn_x = 160
                spawn_y = pyxel.rndi(24, 70)
                spawn_dir = 1
            #敵生成
            Enemy(spawn_x, spawn_y, 3, 0, 0, spawn_dir)
        #Player制御
        self.player.update()

        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in playerbullets:
                if (enemy.x + 12    > bullet.x and
                    enemy.x + 4     < bullet.x + 4 and
                    enemy.y + 16    > bullet.y + 13 and
                    enemy.y + 13    < bullet.y + 17):
                    #Hit時の処理
                    pyxel.play(1, 1, loop=False)    #SE再生
                    bullet.is_alive = False
                    enemy.is_Move = False
                    enemy.hp -= 1
                    cleanup_list(playerbullets)
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        self.score += 10
                        pyxel.play(1, 0, loop=False)    #SE再生
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )

        #list実行
        update_list(playerbullets)
        update_list(enemies)
        update_list(blasts)
        #list更新
        cleanup_list(playerbullets)
        cleanup_list(enemies)
        cleanup_list(blasts)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        update_list(playerbullets)
        update_list(enemies)
        update_list(blasts)
        #list更新
        cleanup_list(playerbullets)
        cleanup_list(enemies)
        cleanup_list(blasts)
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list更新
            playerbullets.clear()          #list全要素削除
            enemies.clear()                #list全要素削除
            blasts.clear()                 #list全要素削除

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

        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        #BG背後
        offset = (pyxel.frame_count // 4) % 128
#        pyxel.blt(- offset, 8, 0, 0, 104, 128, 16, 0)
#        pyxel.blt(128 - offset, 8, 0, 0, 104, 128, 16, 0)

        #BGアクションAREA
        offset = (pyxel.frame_count // 2) % 128
#        pyxel.blt(- offset, 20, 0, 0, 64, 128, 40, 0)
#        pyxel.blt(128 - offset, 20, 0, 0, 64, 128, 40, 0)

        #score表示(f文字列的な)
        pyxel.text(0, 0, f"isAtk {self.player.isAtk}", 7)
        self.player.draw()
#        draw_list(playerbullets)

        #敵とplayerのリストをY座標でソートする
        #self.playerリストがあったら、リスト合体させてる
        characters = enemies + playerbullets + [self.player] if self.player else []
#        characters = enemies + [self.player] if self.player else []
        #charactersリストの中から、keyのcharacter.yでソートする。
        sorted_characters = sorted(characters, key=lambda character: character.y)
        #ソートされた順番で敵の描画
        for character in sorted_characters:
            character.draw()


        #BG一番手前
        offset = pyxel.frame_count % 128
#        pyxel.blt(-offset, 56, 0, 0, 64, 128, 8, 0)
#        pyxel.blt(128 - offset, 56, 0, 0, 64, 128, 8, 0)
    
        draw_list(blasts)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        draw_list(playerbullets)
        draw_list(enemies)
        draw_list(blasts)
App()