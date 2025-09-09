# エンティティ(キャラクター)モジュール

# entitiesフォルダのクラスを__init__.pyでインポートすることで
#   from entities.player import Player
# のようにクラスを個別にインポートする代わりに
#   from entities import Player, Enemy1, Enemy2, Enemy3
# のようにまとめてインポートできるようにする

from .player import Player          # プレイヤークラス
from .zako1 import Zako1            # 敵クラス

"""
from .enemy import Enemy            # 敵クラス
from .blast import Blast            # 爆破クラス
from .item import Item              # アイテムクラス
from .background import Background  # 背景クラス

from .flower import Flower  # フラワークラス
from .mummy import Mummy  # マミークラス
from .pollen import Pollen  # 花粉クラス
from .slime import Slime  # スライムクラス
"""