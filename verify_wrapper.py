
try:
    from pandasai_langchain import LangchainLLM
    from langchain_community.chat_models import ChatOllama
    
    print("SUCCESS: Dependencies imported.")
    
    ollama_model = ChatOllama(model="llama2")
    wrapped_model = LangchainLLM(ollama_model)
    
    # Just checking type
    print(f"Wrapped model type: {type(wrapped_model)}")
    print("SUCCESS: Model wrapped.")
    
except ImportError as e:
    print(f"ERROR: Import failed - {e}")
except Exception as e:
    print(f"ERROR: {e}")
