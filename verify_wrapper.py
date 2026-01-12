
try:
    from pandasai_langchain.llm import LangChainLLM
    from langchain_community.chat_models import ChatOllama
    
    print("SUCCESS: Dependencies imported.")
    
    ollama_model = ChatOllama(model="llama2")
    wrapped_model = LangChainLLM(ollama_model)
    
    # Just checking type
    print(f"Wrapped model type: {type(wrapped_model)}")
    print("SUCCESS: Model wrapped.")
    
except ImportError as e:
    print(f"ERROR: Import failed - {e}")
except Exception as e:
    print(f"ERROR: {e}")
