
try:
    from langchain_core.prompts import ChatPromptTemplate
    print("SUCCESS: langchain_core.prompts.ChatPromptTemplate is importable.")
except ImportError as e:
    print(f"ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")

try:
    import langchain_groq
    print("SUCCESS: langchain_groq is importable.")
except ImportError as e:
    print(f"ERROR: {e}")
