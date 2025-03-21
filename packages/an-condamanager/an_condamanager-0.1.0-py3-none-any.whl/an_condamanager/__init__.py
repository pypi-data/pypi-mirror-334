# __init__.py

# condamanager.py からクラスや関数をインポート
from .condamanager import CondaManager  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["CondaManager"]
