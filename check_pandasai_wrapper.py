
try:
    from pandasai_langchain import LangchainLLM
    print("SUCCESS: pandasai_langchain.LangchainLLM is importable.")
except ImportError as e:
    print(f"ERROR: Could not import LangchainLLM. {e}")
except Exception as e:
    print(f"ERROR: {e}")
