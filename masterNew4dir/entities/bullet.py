import pyxel
#from collision import in_collision, push_back

# 弾クラス
class Bullet:
    #定数
    SIDE_PLAYER = 0     # 自機の弾

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        self.game = game
        self.side = side
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.life_time = 0  #生存時間
        self.hit_area = (2, 1, 5, 6)  # 当たり判定領域
#        game.player_bullets.append(self)
    """
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
    """
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
            self.game.player_bullets.remove(self)
        
    # 弾を描画する
    def draw(self):
        dir = 1 if self.angle == 0 else -1
        pyxel.blt(self.x, self.y, 0, 0, 8, 8 * dir, 8, 0)
