## Demo

You can demo the app here: [DataGent Demo](https://datagent.streamlit.app)

# DataGent - AI-Powered Data Analysis Assistant

DataGent is an intelligent data analysis application powered by AI models. It provides a user-friendly interface for performing various data analysis tasks on CSV and Excel files, including data cleaning, visualization, querying, filtering, and sentiment analysis.

## Features

- **Data Cleaning**: Identify and handle missing values, duplicates, and inconsistencies
- **Data Visualization**: Create interactive charts and graphs
- **Data Querying**: Ask natural language questions about your data
- **Advanced Querying**: Perform complex data analysis with AI assistance
- **Interactive Filtering**: Filter and explore data interactively
- **Sentiment Analysis**: Analyze text data for sentiment (if applicable)


## Configuration

### AI Models
DataGent supports two types of AI models:
1. **Groq (Cloud)**: Requires a GROQ_API_KEY in the .env file
2. **LocalLLM**: Requires a local Ollama server running with the qwen2.5-coder model or any other open-source model of your choice

To use open-source models from Groq:
1. Visit https://console.groq.com/keys and generate an API key
2. Copy the generated API key. (You'll need it later)

To use the local model:
1. Install Ollama: https://ollama.com/
2. Pull the model:
   ```bash
   ollama pull qwen2.5-coder
   ```
3. Start the Ollama server:
   ```bash
   ollama serve
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alexanders-dream/DataGent.git
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
   
4. Run the application:
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

