# __init__.py

# kohyasetupmanager.py からクラスや関数をインポート
from .kohyasetupmanager import KohyaSetupManager  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["KohyaSetupManager"]
