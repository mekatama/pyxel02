# 定数モジュール

# プレイヤーがこの座標を超えたらスクロールさせる
SCROLL_BORDER_X_RIGHT = 70      # スクロール境界X座標
SCROLL_BORDER_X_LEFT = 128 - 70 # スクロール境界X座標

# タイル種別
TILE_NONE = 0  # 何もない
TILE_GEM = 1  # 宝石
TILE_EXIT = 2  # 出口
TILE_BOMB = 3  # ボム
TILE_SPIKE = 4  # ダメージ
TILE_WALL = 5  # ダメージ
TILE_ROAD = 6  # ダメージ
TILE_ZAKO1_POINT = 7  # ZAKO1出現位置

# タイル→タイル種別変換テーブル
TILE_TO_TILETYPE = {
    (1, 0): TILE_GEM,
    (2, 0): TILE_EXIT,
    (3, 0): TILE_BOMB,
    (4, 0): TILE_SPIKE,
    (1, 2): TILE_WALL,
    (1, 3): TILE_WALL,
    (1, 4): TILE_WALL,
    (1, 5): TILE_WALL,
    (1, 6): TILE_ROAD,
    (0, 10): TILE_ZAKO1_POINT,
}
# このテーブルにないタイルはTILE_NONEとして判定する
