import pyxel
from entities import Player, Zako1

from collision import get_tile_type
from constants import (
    SCROLL_BORDER_X_RIGHT,
    SCROLL_BORDER_X_LEFT,
    TILE_ZAKO1_POINT,
    TILE_ZAKO2_POINT
)

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

# プレイ画面クラス
class PlayScene:
    # プレイ画面を初期化する
    def __init__(self, game):
        self.game = game
    # プレイ画面を開始する
    def start(self):
        # 変更前のマップに戻す
        pyxel.tilemaps[0].blt(0, 0, 2, 0, 0, 256, 16)
        # プレイ画面の状態を初期化する
        game = self.game        # ゲームクラス
        game.score = 0          # スコア
        game.player = Player(game, 64, 16)  # プレイヤー
        #仮の敵を生成する
#        self.spawn_enemy(64, 64)
        # 敵を出現させる
        self.spawn_enemy(0, 127)    #画面x座標0～127が表示されたら

    # 敵を出現させる
    def spawn_enemy(self, left_x, right_x):
        game = self.game
        enemies = game.enemies
        # 判定範囲のタイルを計算する
        left_x = pyxel.ceil(left_x / 8)     # x 以上の最小の整数を返す
        right_x = pyxel.floor(right_x / 8)  # x 以下の最大の整数を返す

        # 判定範囲のタイルに応じて敵を出現させる
        for tx in range(left_x, right_x + 1):
            for ty in range(16):
                x = tx * 8
                y = ty * 8
                tile_type = get_tile_type(x, y)

                if tile_type == TILE_ZAKO1_POINT:  # 出現位置の時
                    enemies.append(Zako1(game, x, y))
#                elif tile_type == TILE_ZAKO2_POINT:  # 出現位置の時
#                    enemies.append(Zako2(game, x, y, True))
                else:
                    continue

                # 出現位置タイルを消す
                pyxel.tilemaps[0].pset(tx, ty, (0, 0))

    # プレイ画面を更新する
    def update(self):
        game = self.game
        player = game.player
        player_bullets = game.player_bullets
        player_bombs = game.player_bombs
        enemies = game.enemies
        enemy_blasts = game.enemy_blasts
        enemy_bullets = game.enemy_bullets
        particles = game.particles
        particleHits = game.particleHits
        count = 0

        # プレイヤーを更新する
        if player is not None: #NONE使用時は判定方法が特殊
            player.update()

        # プレイヤーの移動範囲を制限する
        player.x = min(max(player.x, game.screen_x), 248)
        player.x = max(max(player.x, game.screen_x), 0)
        player.y = max(player.y, 0)

        # プレイヤーが右移動スクロール境界を越えたら画面をスクロールする
        if player.x > game.screen_x + SCROLL_BORDER_X_RIGHT:
            last_screen_x = game.screen_x
            game.screen_x = min(player.x - SCROLL_BORDER_X_RIGHT, 32 * 8)
            # 32タイル分以上は右にスクロールさせない

            # スクロールした幅に応じて敵を出現させる
            self.spawn_enemy(last_screen_x + 128, game.screen_x + 127)


        # プレイヤーが左移動スクロール境界を越えたら画面をスクロールする
        if player.x < game.screen_x + SCROLL_BORDER_X_LEFT:
            last_screen_x = game.screen_x
            game.screen_x = min(player.x - SCROLL_BORDER_X_LEFT, 32 * 8)
            # 32タイル分以上は右にスクロールさせない

            # スクロールした幅に応じて敵を出現させる
            self.spawn_enemy(last_screen_x + 128, game.screen_x + 127)

        # 弾(プレイヤー)を更新する
        for player_bullet in player_bullets.copy():
            player_bullet.update()
            # 弾(プレイヤー)と敵が接触したら消去
            for enemy in enemies.copy():
                if check_collision(enemy, player_bullet):
                    player_bullet.add_damage()  # 自機の弾にダメージを与える
                    enemy.add_damage()          # 敵にダメージを与える

        # 爆弾を更新する
        for player_bomb in player_bombs.copy():
            player_bomb.update()
            # 爆弾とplayerが接触したら消去
#            if player is not None and check_collision(player, bomb):
#                bomb.bomb_get()

        # 敵を更新する
        for enemy in enemies.copy():
            enemy.update()
            # プレイヤーと敵が接触したらゲームオーバーにする
            if abs(player.x - enemy.x) < 6 and abs(player.y - enemy.y) < 6:
                game.change_scene("gameover")
                return

        # 敵の爆発を更新する
        for enemy_blast in enemy_blasts.copy():
            enemy_blast.update()

        # 敵の弾を更新する
        for enemy_bullet in enemy_bullets.copy():
            enemy_bullet.update()
            # 弾(enemy)とplayerが接触したら消去
            if player is not None and check_collision(player, enemy_bullet):
                enemy_bullet.add_damage()         # 敵の弾にダメージを与える
                game.change_scene("gameover")
                return

        # 破壊時particlesを更新する
        for particle in particles.copy():
            particle.update()
            # flag onで消す処理入れたい
            if particle.is_alive == False:
                if particle in particles:  # リストに登録されている時
                    particles.remove(particle)

        # Hit時particlesを更新する
        for particleHit in particleHits.copy():
            particleHit.update()
            # flag onで消す処理入れたい
            if particleHit.is_alive == False:
                if particleHit in particleHits:  # リストに登録されている時
                    particleHits.remove(particleHit)

        # [debug]キー入力をチェックする
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            # プレイ画面に切り替える
            self.game.change_scene("gameover")

    # プレイ画面を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # フィールドを描画する
        self.game.draw_field()
        # プレイヤーを描画する
        self.game.draw_player()
        # 弾(プレイヤー)を描画する
        self.game.draw_player_bullets()
        # 爆弾を描画する
        self.game.draw_player_bombs()
        # 敵を描画する
        self.game.draw_enemies()
        # 敵の爆発を描画する
        self.game.draw_enemy_blasts()
        # 敵の弾を描画する
        self.game.draw_enemy_bullets()
        # 破壊時particleを描画する
        self.game.draw_particles()
        # Hit時particleを描画する
        self.game.draw_particleHits()

        # スコアを描画する
#        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        # テキストを描画する
        pyxel.text(31, 108, "- PRESS ENTER -", 6)
