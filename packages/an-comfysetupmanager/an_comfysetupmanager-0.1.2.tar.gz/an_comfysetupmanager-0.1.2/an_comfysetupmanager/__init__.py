# __init__.py

# comfysetupmanager.py からクラスや関数をインポート
from .comfysetupmanager import ComfySetupManager  # 相対インポート

# __all__ を使用して公開するクラスや関数を制限
__all__ = ["ComfySetupManager"]
