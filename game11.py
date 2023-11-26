#左右移動skybom
import pyxel
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PLAYER_HP = 1
PLAYER_SPEED = 1
PLAYER_BULLET_SPEED = 4
BONUS_TIME = 50
#list用意
bullets = []
enemies = []
enemiesUI = []
blasts = []
items = []

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
        self.hp = PLAYER_HP
        self.direction = 1
        self.bulletNum = 3      #残弾数
        self.is_alive = True
    def update(self):
        #移動入力
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
            self.dx = 1
            self.direction = 1  #右向き
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
            self.dx = -1
            self.direction = -1 #左向き
        #攻撃入力
        if pyxel.btnp(pyxel.KEY_A) and self.bulletNum != 0:
            self.bulletNum -= 1
            if self.direction == 1:
                Bullet(self.x + 5, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
            elif self.direction == -1:
                Bullet(self.x + 2, self.y + 4, PLAYER_BULLET_SPEED, self.direction)
        #Playerの位置を更新
        self.x = self.x + self.dx
        #移動停止
        self.dx = 0
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
        self.x += self.speed * self.direction * 0.5
        self.y += 1 * (self.count * 0.2)
        self.count += 1
        #一定時間で消去
        if self.count > 30:            
            self.is_alive = False   #消去
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, dir, hp, ver):
        self.x = x
        self.y = y
        self.hp = hp
        self.direction = dir    #移動方向flag(右:1 左:-1)
        self.speed = speed
        self.version = ver
        self.is_alive = True
        self.is_bonus = True
        enemies.append(self)
    def update(self):
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x >= (WINDOW_H - 8):
            self.x = (WINDOW_H - 8)
            self.direction = -1
        #移動
        self.x += self.speed * self.direction
    def draw(self):
        if self.version == 0:
            pyxel.blt(self.x, self.y, 0, 24, 0, 8 * self.direction, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 24, 8, 8 * self.direction, 8, 0)


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
        if self.count < 20:
            self.y -= 1
        elif self.count >= 20:
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
        pyxel.blt(self.x, self.y, 0, 16, 0 + (8 * self.motion), 8, 8, 0)

#■Item
class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.x = self.x
        self.y = self.y
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
    def draw(self):
        if self.type == 1:
            pyxel.blt(self.x, self.y, 0, 32, 0, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 32, 8, 8, 8, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="sky bom", fps = 30)
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        self.count = 0
        self.enemyNum = 0       #enemy破壊数
        self.enemySpeed = 1
        self.bonusTime = BONUS_TIME
        self.bonusCount = 0
        self.isOnce1 = True     #enemyのspeed制御用
        self.is_bonus = True    #敵は１組しか出ないのでとりあえずflagをここで管理
        self.is_spawn = True
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2, pyxel.height / 2)
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
        #bonusTime
        self.bonusCount += 1
        if self.bonusCount % 6 == 0 and self.bonusTime >= 1:
            self.bonusTime -= 1
        #enemy破壊数でenemy速度変化
        if self.enemyNum % 6 == 0 and self.isOnce1 == True:
            self.enemySpeed += 0.1
            if self.enemySpeed > 4: #最大speed設定
                self.enemySpeed = 4
            self.isOnce1 = False
        #self.is_bounsで生成
        if self.is_spawn == True:
            #enemy生成位置
            spawn_pos = pyxel.rndi(8, 100)
            #enemy移動方向
            if spawn_pos % 2 == 0:
                dir = 1
            else:
                dir = -1
            #enemy生成
            Enemy(spawn_pos,      99, self.enemySpeed, dir, 1, 1)
            Enemy(spawn_pos + 8,  99, self.enemySpeed, dir, 1, 0)
            Enemy(spawn_pos + 16, 99, self.enemySpeed, dir, 1, 1)
            self.is_spawn = False
        #Player制御
        self.player.update()
        #EnemyとBulletの当たり判定
        for enemy in enemies:
#            print(enemies[2].speed)
            for bullet in bullets:
                if (enemy.x + 8    > bullet.x and
                    enemy.x         < bullet.x + 1 and
                    enemy.y + 8    > bullet.y and
                    enemy.y         < bullet.y + 1):
                    #Hit時の処理
                    enemy.hp -= 1
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0:
#                        self.enemyNum += 1
                        enemy.is_alive = False
                        self.count = 0
#                        self.isOnce1 = True
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        #中央の敵破壊時は、左右敵も同時破壊
                        if enemy.version == 0:
#                            self.enemyNum += 1
                            if self.is_bonus == True:
                                self.score += 100
                                self.score += self.bonusTime
                                items.append(
                                    Item(enemy.x, enemy.y, 3)
                                )
                            else:
                                self.score += 10
                                items.append(
                                    Item(enemy.x, enemy.y, 1)
                                )
                            #左右の敵強制破壊
                            for enemy in enemies:
#                                self.enemyNum += 1
                                enemy.is_alive = False
                        else:
                            self.is_bonus = False
#                            self.enemyNum += 1
                            self.score += 10
                            items.append(
                                Item(enemy.x, enemy.y, 1)
                            )

#                        pyxel.play(1, 0, loop=False)    #SE再生
        #enemy全て倒したら
        if not enemies:
            self.enemyNum += 3
            #flag初期化
            self.is_spawn = True
            self.is_bonus = True
            self.isOnce1 = True
            self.bonusTime = BONUS_TIME
            self.bonusCount = 0
       
        #残弾ゼロでgameover
        if self.player.bulletNum == 0:
            self.count += 1
            if self.count > 30:
                pyxel.stop()
                self.scene = SCENE_GAMEOVER

        #ItemとPlayerの処理
        for item in items:
            #Itemの動き
            ex = (self.player.x - item.x)
            ey = (self.player.y - item.y)
            Kp = 0.2
            if ex != 0 or ey != 0:
                item.x = item.x + ex * Kp
                item.y = item.y + ey * Kp

            #ItemとPlayerの当たり判定
            if (self.player.x + 12  > item.x + 4 and
                self.player.x + 4   < item.x + 12 and
                self.player.y + 12  > item.y + 4 and
                self.player.y + 4   < item.y + 12):
                #Hit時の処理
                if item.type == 1:
                    self.player.bulletNum += 1
                elif item.type == 3:
                    self.player.bulletNum += 3
                item.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(items)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(items)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        #list更新
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            self.player.bulletNum = 3
            self.count = 0
            self.enemyNum = 0
            #list全要素削除
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                     #list全要素削除
            blasts.clear()                     #list全要素削除
            items.clear()                     #list全要素削除

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
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "TITLE", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        pyxel.text(39, 10, f"BULLET {self.player.bulletNum:4}", 7)
        pyxel.text(39, 16, f"ENEMY {self.enemyNum:4}", 7)
        pyxel.text(39, 22, f"SPEED {self.enemySpeed:4}", 7)
        pyxel.text(39, 28, f"TIME {self.bonusTime:4}", 7)
        self.player.draw()
        #BG描画
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(0, 32, "GAME OVER", 7)
App()