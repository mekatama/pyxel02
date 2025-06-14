#ロックオンtest
import pyxel
#グローバル変数
g_enemy_id = 0   #enemyのID

# 背景クラス
class Background:
    # 背景を初期化してゲームに登録する
    def __init__(self, game):
        self.game = game  # ゲームへの参照
        # ゲームに背景を登録する()
        self.game.background = self

    # 背景を更新する
    def update(self):
        pass

    # 背景を描画する
    def draw(self):
        # タイトル画面以外で背景画像を描画する
        if self.game.scene != Game.SCENE_TITLE:
            pyxel.blt(0, 0, 2, 0, 0, 128, 128)

# 自機クラス
class Player:
    #定数
    MOVE_SPEED = 2          # 移動速度
    SHOT_INTERVAL = 10      # 弾の発射間隔
    HP = 3                  # 初期HP

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.enemy_x = 0        # 敵のX座標
        self.enemy_y = 0        # 敵のY座標
        self.enemy_id = 0       # 敵のID
        self.shot_timer = 0     # 弾発射までの残り時間
        self.shot_power = 1     # 弾の威力
        self.shot_energy = 100   # powerup用リソース
        self.hp = Player.HP     # HP
        self.is_lockon = False  # lockon flag
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2) 
        # ゲームに自機を登録する
        self.game.player = self

    # 自機にダメージを与える
    def add_damage(self):
        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)
        # BGMを止めて爆発音を再生する
        pyxel.stop()
        pyxel.play(0, 2)
        # 自機を削除する
        self.game.player = None
        # シーンをゲームオーバー画面に変更する
        self.game.change_scene(self.game.SCENE_GAMEOVER)

    # 狙う敵の方向の角度を計算する
    def calc_enemy_angle(self, enemy_x, enemy_y):
        player = self.game.player   # GAME内のplayerの情報にアクセス
        if player is None:          # 自機が存在しない時
            return 90               # 真下方向90度へ攻撃
        else:                       # 自機が存在する時
            return pyxel.atan2(enemy_y - player.y, enemy_x - player.x)

    # 敵との距離判定
    def lockon_distance(self, x1, y1, id):
        player = self.game.player   # GAME内のplayerの情報にアクセス
        if player.is_lockon == False:
            self.enemy_x = x1
            self.enemy_y = y1
            dx = player.x - x1
            dy = player.y - y1
            distance = pyxel.sqrt(dx * dx + dy * dy)
            if distance < 32:
                self.enemy_id = id
                self.is_lockon = True
#                print(self.enemy_id)

    # 自機を更新する
    def update(self):
        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= Player.MOVE_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += Player.MOVE_SPEED

        # キー入力で攻撃力up
        if self.is_lockon == True:
            if pyxel.btn(pyxel.KEY_A):
                #energyあればpowerup
                if self.shot_energy > 0:
                    self.shot_power = 2
                    self.shot_energy -= 1
    #                print(self.shot_energy)
                else:
                    self.shot_power = 1
            else:
                self.shot_power = 1
        else:
            self.shot_power = 1

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        # lockonしたenemyとの角度
        dir = self.calc_enemy_angle(self.enemy_x, self.enemy_y)

        # 弾を発射する
        if self.is_lockon and self.shot_timer == 0:
            # 自機の弾を生成する(右方向は0度)
            Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y, dir, 5)
            # 弾発射音を再生する
            pyxel.play(3, 0)
            # 次の弾発射までの残り時間を設定する
            self.shot_timer = Player.SHOT_INTERVAL

    # 自機を描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8, 8, 0)
        # HP描画
        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)
        # ホーミング攻撃範囲
        pyxel.circb(self.x + 4, self.y + 4, 24, 10)
        # lockon時にline表示
        if self.is_lockon == True:
            pyxel.line(self.x + 4, self.y + 4, self.enemy_x + 4, self.enemy_y + 4, 7)
        # powerup表示
        if self.shot_power == 2:
            pyxel.text(self.x - 2,  self.y + 8, "pow", 7)
        else:
            pyxel.text(-10, -10, "pow", 7)

# 敵クラス
class Enemy:
    #定数
    KIND_A = 0  # 敵A()
    KIND_B = 1  # 敵B()
    KIND_C = 2  # 敵C()

    # 敵を初期化してゲームに登録する
    def __init__(self, game, kind, level, x, y, id):
        self.game = game
        self.kind = kind                # 敵の種類
        self.level = level              # 強さ
        self.x = x
        self.y = y
        self.id = id                    # 敵ID
        self.life_time = 0              # 生存時間
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域
        self.armor = self.level - 1     # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        # ゲームの敵リストに登録する
        self.game.enemies.append(self)

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            if self.game.player is not None:
                self.armor -= self.game.player.shot_power
#            self.armor -= 1
            self.is_damaged = True
            # ダメージ音を再生する
            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)
        # アイテムを生成する
        # ■■■■後からランダムにする■■■■
        Item(self.game, self.x, self.y)
        # playerのlockon解除
        if self.id == self.game.player.enemy_id:
            self.game.player.is_lockon = False
        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)
        # スコアを加算する
        self.game.score += self.level * 10

    # 狙う自機の方向の角度を計算する
    def calc_player_angle(self):
        player = self.game.player   # GAME内のplayerの情報にアクセス
        return pyxel.atan2(player.y - self.y, player.x - self.x)
            
    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.life_time += 1

        # 敵A(空中)を更新する
        if self.kind == Enemy.KIND_A:
            pass

        # 敵B(地上停止)を更新する
        elif self.kind == Enemy.KIND_B:
            pass

        # 敵C(地上移動)を更新する
        elif self.kind == Enemy.KIND_C:
            pass

    # 敵を描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 32, 56 + u, 8, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 32, 40 + u, 8, 8, 0)

# 弾クラス
class Bullet:
    #定数
    SIDE_PLAYER = 0     # 自機の弾
    SIDE_ENEMY = 1      # 敵の弾
    SIDE_PLAYER_H = 2   # 自機の反射弾

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        self.game = game
        self.side = side
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.life_time = 0  #生存時間
        self.vx = pyxel.cos(angle) * speed  #X軸方向の速度
        self.vy = pyxel.sin(angle) * speed  #Y軸方向の速度
        #反射弾
        self.x_start = x
        self.y_start = y

        # 弾の種類に応じた初期化とゲームの弾リストへの登録を行う
        if self.side == Bullet.SIDE_PLAYER:
            self.hit_area = (2, 2, 5, 5)  # 当たり判定領域
            game.player_bullets.append(self)
        elif self.side == Bullet.SIDE_ENEMY:
            self.hit_area = (2, 2, 5, 5)  # 当たり判定領域
            game.enemy_bullets.append(self)
        elif self.side == Bullet.SIDE_PLAYER_H:
            self.hit_area = (0, 0, 8, 8)  # 当たり判定領域
            game.player_h_bullets.append(self)

     # 弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self.side == Bullet.SIDE_PLAYER:
            if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
                self.game.player_bullets.remove(self)
        elif self.side == Bullet.SIDE_ENEMY:
            if self in self.game.enemy_bullets:     # 敵の弾リストに登録されている時
                self.game.enemy_bullets.remove(self)
        elif self.side == Bullet.SIDE_PLAYER_H:
            if self in self.game.enemy_bullets:     # 反射弾リストに登録されている時
                self.game.player_h_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する
        self.x += self.vx
        self.y += self.vy

        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            if self.side == Bullet.SIDE_PLAYER:
                self.game.player_bullets.remove(self)
            elif self.side == Bullet.SIDE_ENEMY:
                self.game.enemy_bullets.remove(self)
            elif self.side == Bullet.SIDE_PLAYER_H:
                self.game.player_h_bullets.remove(self)
        
    # 弾を描画する
    def draw(self):
        if self.side == Bullet.SIDE_PLAYER:
            pyxel.blt(self.x, self.y, 0, 16, 8, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)

# 爆発エフェクトクラス
class Blast:
    #定数
    START_RADIUS = 1    # 開始時の半径
    END_RADIUS = 8      # 終了時の半径

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = Blast.START_RADIUS  # 爆発の半径
        # ゲームの爆発エフェクトリストに登録する
        game.blasts.append(self)

    # 爆発エフェクトを更新する
    def update(self):
        # 半径を大きくする
        self.radius += 1
        # 半径が最大になったら爆発エフェクトリストから登録を削除する
        if self.radius > Blast.END_RADIUS:
            self.game.blasts.remove(self)

    # 爆発エフェクトを描画する
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)

# 敵予兆クラス
class Sign:
    #定数
    START_RADIUS = 1    # 開始時の半径
    END_RADIUS = 4      # 終了時の半径

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = Sign.START_RADIUS  # 爆発の半径
        self.is_go = False  #敵生成flag
        # ゲームの爆発エフェクトリストに登録する
        game.signs.append(self)

     # 予兆後に敵を生成
    def spawn_enemy(self):
        #グローバル変数宣言
        global g_enemy_id
        g_enemy_id += 1
        Enemy(self.game, 0, 10, self.x, self.y, g_enemy_id)

    # 敵予兆を更新する
    def update(self):
        # 半径を大きくする
        self.radius += 0.1
        # 半径が最大になったら敵予兆リストから登録を削除する
        if self.radius > Sign.END_RADIUS:
            self.is_go = True
            self.game.signs.remove(self)

    # 敵予兆を描画する
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)

# アイテムクラス
class Item:
    #定数

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hit_area = (0, 0, 8, 8)    # 当たり判定の領域
        # アイテムリストに登録する
        game.items.append(self)

     # アイテムにダメージを与える
    def add_damage(self):
        player = self.game.player   # GAME内のplayerの情報にアクセス
        player.shot_energy += 10     # energy回復
        # アイテムをリストから削除する
        if self in self.game.items:    # アイテムリストに登録されている時
            self.game.items.remove(self)

    # アイテムを更新する
    def update(self):
        #空中に生成されたらy=100まで移動して停止
        if self.y < 100:
            self.y += 1

    # アイテムを描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 56, 32, 8, 8, 0)

# 当たり判定用の関数
#   タプルで設定した当たり判定領域を使用して判定
def check_collision(entity1, entity2):
    #キャラクター1の当たり判定座標を設定
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]

    #キャラクター2の当たり判定座標を設定
    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]

    # キャラクター1の左端がキャラクター2の右端より右にある
    if entity1_x1 > entity2_x2: #成立すれば衝突していない
        return False
    # キャラクター1の右端がキャラクター2の左端より左にある
    if entity1_x2 < entity2_x1: #成立すれば衝突していない
        return False
    # キャラクター1の上端がキャラクター2の下端より下にある
    if entity1_y1 > entity2_y2: #成立すれば衝突していない
        return False
    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_y2 < entity2_y1: #成立すれば衝突していない
        return False
    # 上記のどれでもなければ重なっている
    return True #衝突している

# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    #定数
    SCENE_TITLE = 0     # タイトル画面
    SCENE_PLAY = 1      # プレイ画面
    SCENE_GAMEOVER = 2  # ゲームオーバー画面

    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(128, 128, title="game20")
        # リソースファイルを読み込む
        pyxel.load("my_resource20.pyxres")
        # ゲームの状態を初期化する
        self.score = 0          # スコア
        self.scene = None       # 現在のシーン
        self.background = None  # 背景
        self.player = None      # 自機
        self.enemies = []       # 敵のリスト
        self.player_bullets = []# 自機の弾のリスト
        self.enemy_bullets = [] # 敵の弾のリスト
        self.player_h_bullets = []  # 反射弾のリスト
        self.blasts = []        # 爆発エフェクトのリスト
        self.items = []         # アイテムのリスト
        self.signs = []         # 敵予兆のリスト

        # 背景を生成する(背景はシーンによらず常に存在する)
        Background(self)
        # シーンをタイトル画面に変更する
        self.change_scene(Game.SCENE_TITLE)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する関数
    def change_scene(self, scene):
        self.scene = scene
        # タイトル画面
        if self.scene == Game.SCENE_TITLE:
            # 自機を削除する
            self.player = None  # プレイヤーを削除
            # 全ての弾と敵とアイテムを削除する
            self.enemies.clear()
            self.player_bullets.clear()     # 自機の弾を削除する処理を追加
            self.enemy_bullets.clear()      # 敵の弾を削除する処理を追加
            self.player_h_bullets.clear()   # 反射弾を削除する処理を追加
            self.items.clear()              # アイテムを削除する処理を追加
            self.signs.clear()              # 敵予兆を削除する処理を追加
            #グローバル変数宣言
            global g_enemy_id
            g_enemy_id = 0                  #敵ID初期化

        # プレイ画面
        elif self.scene == Game.SCENE_PLAY:
            # プレイ状態を初期化する
            self.score = 0      # スコアを0に戻す
            # 自機を生成する
            Player(self, 56, 100)
            #仮の敵を生成する
#            kind = pyxel.rndi(Enemy.KIND_A, Enemy.KIND_C)
#            Enemy(self, 1, 1, pyxel.rndi(0, 112), 100)
            #[test敵A]
#            Enemy(self, 0, 10, 64, 32)
#            Enemy(self, 0, 10, 100, 32)
            #[test敵B]
#            Enemy(self, 1, 1, -10, 100, 1)
#            Enemy(self, 1, 1, 138, 100, -1)
            #[test敵C]
#            Enemy(self, 2, 1, -10, 100, 1)
#            Enemy(self, 2, 1, 138, 100, -1)

        # ゲームオーバー画面
        elif self.scene == Game.SCENE_GAMEOVER:
            # 画面表示時間を設定する
            self.display_timer = 60
            # 自機を削除する
            self.player = None  # プレイヤーを削除

    # ゲーム全体を更新する
    def update(self):
        # 背景を更新する
        self.background.update()

        # 自機を更新する
        if self.player is not None: #NONE使用時は判定方法が特殊
            self.player.update()
#            def calc_enemy_angle(self, enemy_x, enemy_y):

        # 敵を更新する
        # ループ中に要素の追加・削除が行われても問題ないようにコピーしたリストを使用する
        for enemy in self.enemies.copy():
            enemy.update()
            # 自機と敵の当たり判定を行う
            if self.player is not None and check_collision(self.player, enemy):
                self.player.add_damage()  # 自機にダメージを与える
            # 自機と敵の距離判定を行う
            if self.player is not None:
                #敵IDも確認
                self.player.lockon_distance(enemy.x, enemy.y, enemy.id)  # 距離測定

        # 自機の弾を更新する
        for bullet in self.player_bullets.copy():   # 自機の弾を更新する処理を追加
            bullet.update()
            # 自機の弾と敵の当たり判定を行う
            for enemy in self.enemies.copy():
                if check_collision(enemy, bullet):
                    bullet.add_damage() # 自機の弾にダメージを与える
                    enemy.add_damage()  # 敵にダメージを与える
                    #弾の発射音制御?
                    if self.player is not None:  # 自機が存在する時
                        self.player.sound_timer = 5  # 弾発射音を止める時間を設定する

        # 敵の弾を更新する
        for bullet in self.enemy_bullets.copy():    # 敵の弾を更新する処理を追加
            bullet.update()
            # プレイヤーと敵の弾の当たり判定を行う
            if self.player is not None and check_collision(self.player, bullet):
                bullet.add_damage()         # 敵の弾にダメージを与える
                self.player.add_damage()    # 自機にダメージを与える

        # 爆発エフェクトを更新する
        for blast in self.blasts.copy():  # 爆発エフェクトを更新する処理を追加
            blast.update()

        # 敵予兆を更新する
        for sign in self.signs.copy():  # 敵予兆を更新する処理を追加
            sign.update()
            #敵を生成
            if sign.is_go == True:
                sign.spawn_enemy()

        # アイテムを更新する
        for item in self.items.copy():  # アイテムを更新する処理を追加
            item.update()
            # 自機とアイテムの当たり判定を行う
            if self.player is not None and check_collision(self.player, item):
                item.add_damage()  # アイテムにダメージを与える

        # シーンを更新する
        if self.scene == Game.SCENE_TITLE:  # タイトル画面
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.change_scene(Game.SCENE_PLAY)
        elif self.scene == Game.SCENE_PLAY:  # プレイ画面
            #enemy生成
            if pyxel.frame_count % 120 == 0:
#                kind = pyxel.rndi(Enemy.KIND_A, Enemy.KIND_C)
                kind = Enemy.KIND_A
                if kind == Enemy.KIND_A:
#                    Enemy(self, 0, 10, pyxel.rndi(0, 112), pyxel.rndi(0, 112))
                    Sign(self, pyxel.rndi(0, 112), pyxel.rndi(0, 112))
                elif kind == Enemy.KIND_B:
                    if pyxel.rndi(0, 1) == 0:
                        Enemy(self, 1, 1, -10, 100, 1)
                    else:
                        Enemy(self, 1, 1, 138, 100, -1)
                elif kind == Enemy.KIND_C:
                    if pyxel.rndi(0, 1) == 0:
                        Enemy(self, 2, 1, -10, 100, 1)
                    else:
                        Enemy(self, 2, 1, 138, 100, -1)
        elif self.scene == Game.SCENE_GAMEOVER:  # ゲームオーバー画面
            if self.display_timer > 0:  # 画面表示時間が残っている時
                self.display_timer -= 1
            else:                       # 画面表示時間が0になった時
                self.change_scene(Game.SCENE_TITLE)

    # ゲーム全体を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)

        # 背景を描画する
        self.background.draw()

        # 自機を描画する
        if self.player is not None:
            self.player.draw()

        # 敵を描画する
        for enemy in self.enemies:
            enemy.draw()

        # 自機の弾を描画する
        for bullet in self.player_bullets:  # 自機の弾を更新する処理を追加
            bullet.draw()

        # 敵の弾を描画する
        for bullet in self.enemy_bullets:   # 敵の弾を更新する処理を追加
            bullet.draw()

        # 反射弾を描画する
        for bullet in self.player_h_bullets:  # 反射弾を更新する処理を追加
            bullet.draw()

        # 爆発エフェクトを描画する
        for blast in self.blasts:  # 爆発エフェクトを更新する処理を追加
            blast.draw()

        # 敵予兆を描画する
        for sign in self.signs:  # 敵予兆を更新する処理を追加
            sign.draw()

        # アイテムを描画する
        for item in self.items:  # アイテムを更新する処理を追加
            item.draw()

        # スコアを描画する
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)
        # energyを描画する
        if self.player is not None:
            pyxel.text(35, 11, f"ENERGY {self.player.shot_energy:5}", 7)

        # シーンを描画する
        if self.scene == Game.SCENE_TITLE:      # タイトル画面
            pyxel.blt(0, 18, 0, 0, 96, 128, 32, 15)
            pyxel.text(31, 148, "- PRESS ENTER -", 6)
        elif self.scene == Game.SCENE_GAMEOVER: # ゲームオーバー画面
            pyxel.text(43, 78, "GAME OVER", 8)

# ゲームを生成して開始する
Game()
