
try:
    from langchain_community.chat_models import ChatOllama
    print("SUCCESS: langchain_community.chat_models.ChatOllama is importable.")
    model = ChatOllama(model="llama2")
    print("SUCCESS: ChatOllama instantiated.")
except ImportError as e:
    print(f"ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
