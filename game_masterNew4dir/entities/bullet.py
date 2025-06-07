import pyxel
#from collision import in_collision, push_back

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
            self.hit_area = (2, 1, 5, 6)  # 当たり判定領域
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
        if self.side == self.SIDE_ENEMY:
            self.x += self.vx
            self.y += self.vy
        elif self.side == self.SIDE_PLAYER_H:
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
        
        #playerの弾はすぐに消す
        if self.side == Bullet.SIDE_PLAYER:
            if self.life_time % 10 == 0:
                self.game.player_bullets.remove(self)

    # 弾を描画する
    def draw(self):
        if self.side == Bullet.SIDE_PLAYER:
            dir = 1 if self.angle == 0 else -1
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * dir, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)
