# DataGent - AI-Powered Data Analysis Assistant

DataGent is an intelligent data analysis application powered by AI models. It provides a user-friendly interface for performing various data analysis tasks on CSV and Excel files, including data cleaning, visualization, querying, filtering, and sentiment analysis.

## Features

- **Data Cleaning**: Identify and handle missing values, duplicates, and inconsistencies
- **Data Visualization**: Create interactive charts and graphs
- **Data Querying**: Ask natural language questions about your data
- **Advanced Querying**: Perform complex data analysis with AI assistance
- **Interactive Filtering**: Filter and explore data interactively
- **Sentiment Analysis**: Analyze text data for sentiment (if applicable)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/datagent.git
   cd datagent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Open `main.py` Add the name of the ai models you want to use (Line 42).
   ```
   if model_choice == "ChatGroq (Cloud)":
    if not os.getenv("GROQ_API_KEY"):
        st.sidebar.error("GROQ_API_KEY not found in .env file")
        model = LocalLLM(api_base="http://localhost:11434/v1", model="qwen2.5-coder")
    else:
        model = ChatGroq(temperature=0, model_name="gemma2-9b-it")
   else:
      model = LocalLLM(api_base="http://localhost:11434/v1", model="qwen2.5-coder")
   ```

6. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage

1. Start the application by running `streamlit run main.py`
2. Upload a CSV file using the sidebar
3. Explore the different tabs for various data analysis features:
   - **Data Cleaning**: Clean and preprocess your data
   - **Data Visualization**: Create visualizations of your data
   - **Data Querying with AI**: Ask natural language questions about your data
   - **Advanced Querying**: Perform complex data analysis
   - **Interactive Data Filtering**: Filter and explore your data
   - **Sentiment Analysis**: Analyze text data for sentiment (if applicable)

4. Use the sidebar to:
   - Choose between Cloud (ChatGroq) or Local AI models
   - End the current session
   - View information about the current AI model

## Configuration

### AI Models
DataGent supports two types of AI models:
1. **ChatGroq (Cloud)**: Requires a GROQ_API_KEY in the .env file
2. **LocalLLM**: Requires a local Ollama server running with the qwen2.5-coder model

To use the local model:
1. Install Ollama: https://ollama.ai/
2. Pull the model:
   ```bash
   ollama pull qwen2.5-coder
   ```
3. Start the Ollama server:
   ```bash
   ollama serve
   ```

## Requirements

- Python 3.10
- Streamlit
- Pandas
- LangChain
- PandasAI
- python-dotenv

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.