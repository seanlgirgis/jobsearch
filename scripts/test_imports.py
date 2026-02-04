# scripts/test_imports.py
try:
    from src.loaders.master_profile import MasterProfileLoader
    from src.ai.grok_client import GrokClient
    print("Imports OK")
except ImportError as e:
    print("Import failed:", e)