import pyxel
from .particle import Particle  # 破壊時particle
from .particle_hit import ParticleHit  # 破壊時particle

# 弾クラス
class PlayerBullet:
    #定数
    SHOT_SPEED_X = 4        # shot speed x
    SHOT_SPEED_Y = 4        # shot speed y
    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dir, type):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
        self.life_time = 0  #生存時間
        self.hit_area = (2, 2, 5, 5)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # パーティクル出す
        for i in range(10):
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4)
            )
        # hitパーティクル出す
        self.game.particleHits.append(
            ParticleHit(self.game, self.x + 4, self.y + 4)
        )
        # 弾をリストから削除する
        if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
            self.game.player_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する(type 0:横 1:上 2:下)
        if self.type == 0:
            self.x += PlayerBullet.SHOT_SPEED_X * self.dir
        elif self.type == 1:
            self.x += PlayerBullet.SHOT_SPEED_X * self.dir
            self.y -= PlayerBullet.SHOT_SPEED_Y
        elif self.type == 2:
            self.x += PlayerBullet.SHOT_SPEED_X * self.dir
            self.y += PlayerBullet.SHOT_SPEED_Y
        """
        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.player_bullets.remove(self)
        """
    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)
