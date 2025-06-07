# 衝突処理モジュール
import pyxel
"""
from constants import TILE_NONE, TILE_TO_TILETYPE, TILE_WALL
"""

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

"""
# 指定した座標のタイル種別を取得する
def get_tile_type(x, y):
    tile = pyxel.tilemaps[0].pget(x // 8, y // 8)
    return TILE_TO_TILETYPE.get(tile, TILE_NONE)


# 指定した座標が壁と重なっているか判定する
def in_collision(x, y):
    return get_tile_type(x, y) == TILE_WALL


# キャラクターが壁と重なっているか判定する
def is_character_colliding(x, y):
    # キャラクターと重なっているタイル座標の領域を計算する
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 7) // 8
    y2 = (pyxel.ceil(y) + 7) // 8

    # タイル座標の領域が壁と重なっているかどうかを判定する
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if in_collision(xi * 8, yi * 8):
                return True  # 壁と衝突している

    return False  # 壁と衝突していない


# 押し戻した座標を返す
def push_back(x, y, dx, dy):
    # 壁と衝突するまで垂直方向に移動する
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_character_colliding(x, y + step):
            break
        y += step
        dy -= step

    # 壁と衝突するまで水平方向に移動する
    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_character_colliding(x + step, y):
            break
        x += step
        dx -= step

    return x, y
"""