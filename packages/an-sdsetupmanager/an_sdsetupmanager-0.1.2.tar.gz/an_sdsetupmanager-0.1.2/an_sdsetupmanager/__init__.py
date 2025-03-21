# __init__.py

# sdsetupmanager.py からクラスや関数をインポート
from .sdsetupmanager import SDSetupManager  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["SDSetupManager"]
