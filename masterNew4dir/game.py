import pyxel
from scenes import GameOverScene, PlayScene, TitleScene

# ゲームクラス
class Game:
    # ゲームを初期化する
    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(128, 128, title="master")
        # リソースファイルを読み込む
        pyxel.load("assets/my_resource20.pyxres")
        pyxel.tilemaps[2].blt(0, 0, 0, 0, 0, 256, 16)  # 変更前のマップをコピーする
        # ゲームの状態を初期化する
        self.player = None          # プレイヤー
        self.player_bullets = []    # 自機の弾のリスト
        self.bombs = []             # 爆弾のリスト
        self.enemies = []           # 敵のリスト
        self.enemy_blasts = []      # 爆発エフェクトのリスト
        self.enemy_bullets = []     # 敵の弾のリスト
        self.scenes = {                     # シーンの辞書
            "title": TitleScene(self),
            "play": PlayScene(self),
            "gameover": GameOverScene(self),
        }
        self.scene_name = None  # 現在のシーン名
        self.screen_x = 0  # フィールド表示範囲の左端のX座標
        self.score = 0  # 得点

        # シーンをタイトル画面に変更する
        self.change_scene("title")

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene_name):
        self.scene_name = scene_name
        self.scenes[self.scene_name].start()

    # フィールドを描画する
    def draw_field(self):
        pyxel.bltm(0, 0, 0, self.screen_x, 0, 128, 128)

    # プレイヤーを描画する
    def draw_player(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        if self.player is not None:  # プレイヤーが存在する時
            self.player.draw()
        # カメラ位置を戻す
        pyxel.camera()

    # 弾(プレイヤー)を描画する
    def draw_player_bullets(self):
        for player_bullet in self.player_bullets:
            player_bullet.draw()
    # 敵を描画する
    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()
    # 敵の爆発を描画する
    def draw_enemy_blasts(self):
        for enemy_blast in self.enemy_blasts:
            enemy_blast.draw()
    # 敵の弾を描画する
    def draw_enemy_bullets(self):
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()
    # 爆弾を描画する
    def draw_bombs(self):
        for bomb in self.bombs:
            bomb.draw()

    # ゲームを更新する
    def update(self):
        # 現在のシーンを更新する
        self.scenes[self.scene_name].update()

    # ゲームを描画する
    def draw(self):
        # 現在のシーンを描画する
        self.scenes[self.scene_name].draw()
