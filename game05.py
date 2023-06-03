#画面中央からSTG
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PLAYER_HP = 1
BULLET_SPEED = 2
ENEMY_SPEED = 1.5
#list用意
enemies = []
enemiesUI = []
bullets = []
blasts = []
boms = []
bomseffects = []

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
        self.hp = PLAYER_HP
        self.is_alive = True
    def update(self):
        #pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        # スペースキーが押されたら新しい弾を発射する
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            Bullet(WINDOW_W // 2, WINDOW_H // 2, BULLET_SPEED)
    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        #当たり判定
#        pyxel.rectb(self.x + 4, self.y + 4, 8, 8, 10)

#■Bullet
class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = [0, 0]
        self.is_alive = True
        self.count = 0
        # マウスの位置を取得
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        # 弾の移動方向を計算
        dx = self.mouse_x - self.x
        dy = self.mouse_y - self.y
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            self.direction[0] = dx / length
            self.direction[1] = dy / length
        bullets.append(self)
    def update(self):
        self.count += 1
        # 弾を移動させる
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        if self.count >= 50: #一定時間表示
            self.is_alive = False       #消去
    def draw(self):
        pyxel.circ(self.x, self.y, 2, 8)

#■Enemy
class Enemy:
    def __init__(self, x, y, hp, img, speed):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img          #表示画像指定
        self.addSpeed = speed   #追加speed
        self.direction = [0, 0]
        self.is_alive = True
        # 敵の移動方向を計算
        dx = WINDOW_W / 2 - self.x -4
        dy = WINDOW_H / 2 - self.y
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            self.direction[0] = dx / length
            self.direction[1] = dy / length
        enemies.append(self)
    def update(self):
        #移動
        self.x += self.direction[0] * self.addSpeed
        self.y += self.direction[1] * self.addSpeed
    def draw(self):
        if self.hp == 1:
            pyxel.blt(self.x, self.y, 0, 16 * self.img, 0, 16, 16, 0)
        elif self.hp == 2:
            pyxel.blt(self.x, self.y, 0, 16 * self.img, 16, 16, 16, 0)
        #当たり判定
#        pyxel.rectb(self.x + 4, self.y + 4, 8, 8, 10)

#■Enemy_UI
class EnemyUI:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.count = 0
        self.is_alive = True
        enemiesUI.append(self)
    def update(self):
        self.count += 1
        if self.count < 10:
            self.y -= 1
        elif self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", 13)

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

#■Cursor
class Cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
    def draw(self):
        #editorデータ描画
        pyxel.blt(self.x - 8, self.y - 8, 0, 16, 32, 16, 16, 0)

#■Bom
class Bom:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.is_alive = True
        boms.append(self)
    def update(self):
        #何も動かない
        pass
    def draw(self):
        if self.hp == 3:
            pyxel.blt(self.x, self.y, 0, 64, 32, 16, 16, 0)
        elif self.hp == 2: 
            pyxel.blt(self.x, self.y, 0, 64, 16, 16, 16, 0)
        elif self.hp == 1: 
            pyxel.blt(self.x, self.y, 0, 64,  0, 16, 16, 0)

#■BomEffect
class BomEffect:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.is_alive = True
        bomseffects.append(self)
    def update(self):
        self.r += 9    #円の半径大きくする用
        if self.r >= 200:
            self.is_alive = False
    def draw(self):
        pyxel.circb(self.x, self.y, self.r, 7)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource05.pyxres")
        self.score = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        # マウスカーソル表示
        pyxel.mouse(False)
        #Cursor生成
        self.cursor = Cursor(pyxel.mouse_x, pyxel.mouse_y)
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
        pass

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
            pyxel.playm(0, loop = True)    #BGM再生
            self.scene = SCENE_PLAY
        #Cursor制御
        self.cursor.update()

    #ゲーム画面処理用update
    def update_play_scene(self):
        #scoreで生成間隔を制御
        if self.score < 30:
            spawntime = 30
        elif self.score >= 30 and self.score < 70:
            spawntime = 25
        elif self.score >= 70:
            spawntime = 20
        
        #一定時間でenemy出現判定
        if pyxel.frame_count % spawntime == 0:
            #生成辺(位置)ランダム
            spawn_side = pyxel.rndi(0, 3)
            #生成座標ランダム
            if spawn_side == 0:
                spawn_x = pyxel.rndi(-32, 160)
                spawn_y = -32
            elif spawn_side == 1:
                spawn_x = pyxel.rndi(-32, 160)
                spawn_y = 160
            elif spawn_side == 2:
                spawn_x = -32
                spawn_y = pyxel.rndi(-32, 160)
            elif spawn_side == 3:
                spawn_x = 160
                spawn_y = pyxel.rndi(-32, 160)
            pass                
            #enemy生成(scoreで分岐)
            if self.score < 30:
                speed = 0.5
                Enemy(spawn_x, spawn_y, 1, 1, speed)
            elif self.score >= 30 and self.score < 70:
                speed = pyxel.rndf(0.5, 1.0)
                img = pyxel.rndi(1, 2)
                Enemy(spawn_x, spawn_y, 1, img, speed)
            elif self.score >= 70:
                speed = pyxel.rndf(1.0, 1.5)
                img = pyxel.rndi(1, 3)
                if img == 3:
                    Enemy(spawn_x, spawn_y, 2, img, speed)
                else:
                    Enemy(spawn_x, spawn_y, 1, img, speed)
                
        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if (enemy.x + 12    > bullet.x and
                    enemy.x + 4     < bullet.x + 2 and
                    enemy.y + 12    > bullet.y and
                    enemy.y + 4     < bullet.y + 2):
                    #Hit時の処理
                    bullet.is_alive = False
                    enemy.hp -= 1
                    cleanup_list(bullets)
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        self.score += 10
                        pyxel.play(1, 0, loop=False)    #SE再生
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        #Bom生成判定
                        if pyxel.rndi(1, 10) == 10:
                            Bom(enemy.x, enemy.y, 3)
                        
        #EnemyとPlayerの当たり判定
        for enemy in enemies:
            if (self.player.x + 12  > enemy.x + 4 and
                self.player.x + 4   < enemy.x + 12 and
                self.player.y + 12  > enemy.y + 4 and
                self.player.y + 4   < enemy.y + 12):
                #Hit時の処理
                self.player.hp -= 1
                enemy.is_alive = False
                pyxel.play(1, 1, loop=False)    #SE再生
                #player残りHP判定
                if self.player.hp <= 0:
                    blasts.append(
                        Blast(enemy.x, enemy.y)
                    )
                    pyxel.stop(0)
                    self.scene = SCENE_GAMEOVER
        #BomとBulletの当たり判定
        for bom in boms:
            for bullet in bullets:
                if (bom.x + 16    > bullet.x and
                    bom.x         < bullet.x + 2 and
                    bom.y + 16    > bullet.y and
                    bom.y         < bullet.y + 2):
                    #Hit時の処理
                    bom.hp -= 1
                    bullet.is_alive = False
                    #Bom残りHP判定
                    if bom.hp <= 0:
                        bom.is_alive = False
                        pyxel.play(1, 0, loop=False)    #SE再生
                        blasts.append(
                            Blast(bom.x, bom.y)
                        )
                        bomseffects.append(
                            BomEffect(bom.x, bom.y, 0)
                        )
                        #BomでEnemy全部にダメージ発生
                        for enemy in enemies:
                            print("bom!")
                            enemy.hp -= 2
                            #enemy残りHP判定
                            if enemy.hp <= 0:
                                enemy.is_alive = False
                                self.score += 10
                                pyxel.play(1, 0, loop=False)    #SE再生
                                enemiesUI.append(
                                    EnemyUI(enemy.x, enemy.y, 10)
                                )
                                blasts.append(
                                    Blast(enemy.x, enemy.y)
                                )

        #Player制御
        self.player.update()
        #Cursor制御
        self.cursor.update()

        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(boms)
        update_list(bomseffects)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(boms)
        cleanup_list(bomseffects)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #Cursor制御
        self.cursor.update()
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(boms)
        update_list(bomseffects)
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(boms)
        cleanup_list(bomseffects)
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.player.hp = PLAYER_HP          #HP初期化
            self.score = 0
            self.scene = SCENE_TITLE
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                   #list全要素削除
            blasts.clear()                      #list全要素削除
            boms.clear()                        #list全要素削除
            bomseffects.clear()                 #list全要素削除

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

        #score表示(f文字列的な)
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    #タイトル画面描画用update
    def draw_title_scene(self):
        self.cursor.draw()
#        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(48, 28, "SPACE360", 7)
        pyxel.text(32, 58, "- PRESS  ENTER -", 7)
        pyxel.text(0, 76, "--------------------------------", 7)
        pyxel.text(40, 82, "HOW TO PLAY", 7)
        pyxel.text(24, 94, "THE TARGET IS MOVED", 7)
        pyxel.text(36, 100, "WITH THE MOUSE", 7)
        pyxel.text(24, 112, "SPACE KEY TO ATTACK", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        self.player.draw()
        self.cursor.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(boms)
        draw_list(bomseffects)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        self.cursor.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(boms)
        draw_list(bomseffects)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()