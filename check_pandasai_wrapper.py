
try:
    from pandasai.llm import LangChainLLM
    print("SUCCESS: pandasai.llm.LangChainLLM is importable.")
except ImportError:
    try:
        from pandasai_langchain import LangChainLLM
        print("SUCCESS: pandasai_langchain.LangChainLLM is importable.")
    except ImportError as e:
        print(f"ERROR: Could not import LangChainLLM. {e}")
except Exception as e:
    print(f"ERROR: {e}")
