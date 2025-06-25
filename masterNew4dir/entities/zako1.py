import pyxel
#from collision import in_collision, push_back

# 敵クラス
class Zako1:
    #定数
    KIND_A = 0  # 敵A(空中)
    KIND_B = 1  # 敵B(地上停止)
    KIND_C = 2  # 敵C(地上移動)
    enemy_blasts = []        # 爆発エフェクトのリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.life_time = 0              # 生存時間
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域
        self.armor = 2                   # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
#        # ゲームの敵リストに登録する
#        self.game.enemies.append(self)
    # 敵にダメージを与える
    def add_damage(self):
#        if self in self.game.enemies:  # 敵リストに登録されている時
#            self.game.enemies.remove(self)
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
        # 爆発エフェクトを生成する
        Enemy_Blast(self.game, self.x + 4, self.y + 4)
        """
        # アイテムを生成する
        # ■■■■後からランダムにする■■■■
        Item(self.game, self.x, self.y)
        """
        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)
        # スコアを加算する
#        self.game.score += self.level * 10
    """
    # 狙う自機の方向の角度を計算する
    def calc_player_angle(self):Zako1Zako1
        player = self.game.player   # GAME内のplayerの情報にアクセス
        if player is None:          # 自機が存在しない時
            return 90               # 真下方向90度へ攻撃
        else:                       # 自機が存在する時
            return pyxel.atan2(player.y - self.y, player.x - self.x)
    """
            
    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.life_time += 1
        """
        # 敵A(空中)を更新する
        if self.kind == Zako1.KIND_A:
            pass

        # 敵B(地上停止)を更新する
        elif self.kind == Zako1.KIND_B:
            pass

        # 敵C(地上移動)を更新する
        elif self.kind == Zako1.KIND_C:
            pass
        """
    # 敵を描画する
    def draw(self):
#        pyxel.blt(self.x, self.y, 0, 32, 40, 8, 8, 0)
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 0, 8 + 32, 56 + u, 8, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 0, 32, 40 + u, 8, 8, 0)
#            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 32, 40 + u, 8 * self.dir, 8, 0)

# 爆発エフェクトクラス
class Enemy_Blast:
    #定数
    START_RADIUS = 1    # 開始時の半径
    END_RADIUS = 8      # 終了時の半径

    # 初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.radius = Enemy_Blast.START_RADIUS  # 爆発の半径
        # ゲームの爆発エフェクトリストに登録する
        game.enemy_blasts.append(self)

    # 爆発エフェクトを更新する
    def update(self):
        # 半径を大きくする
        self.radius += 1
        # 半径が最大になったら爆発エフェクトリストから登録を削除する
        if self.radius > Enemy_Blast.END_RADIUS:
            self.game.enemy_blasts.remove(self)

    # 爆発エフェクトを描画する
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)
        pyxel.circb(self.x, self.y, self.radius, 10)
