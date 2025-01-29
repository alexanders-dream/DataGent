import plotly.express as px
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources (only needed once)
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def text_preprocessing(text):
    """Preprocess text for sentiment analysis."""
    # Convert text to lowercase
    text = text.lower()
    
    # Remove HTML tags and special characters
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'[' + string.punctuation + ']', '', text)
    
    # Tokenize text
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    # Join tokens back into a string
    return ' '.join(tokens)

def sentiment_analysis_section(data):
    st.markdown("### Sentiment Analysis")
    
    # Select text column for sentiment analysis
    text_column = st.selectbox("Select a text column for sentiment analysis", data.columns)
    
    if st.button("Perform Sentiment Analysis"):
        if data[text_column].dtype == "object":
            
            # Preprocess text data
            data['Clean_Text'] = data[text_column].apply(lambda x: text_preprocessing(str(x)))
            
            # Initialize sentiment analyzer
            sia = SentimentIntensityAnalyzer()
            
            # Perform sentiment analysis
            data['Sentiment'] = data['Clean_Text'].apply(lambda x: sia.polarity_scores(x)['compound'])
            
            # Create sentiment labels with improved thresholds
            data['Sentiment_Label'] = pd.cut(
                data['Sentiment'],
                bins=[-1, -0.1, 0.1, 1],
                labels=['Negative', 'Neutral', 'Positive'],
                include_lowest=True
            )
            
            # Show sentiment analysis results
            st.write(data[[text_column, 'Clean_Text', 'Sentiment', 'Sentiment_Label']].head())
            
            # After analysis
            st.subheader("Analysis Metrics")
            st.metric("Total Texts Analyzed", len(data))
            st.metric("Positive Texts", (data['Sentiment_Label'] == 'Positive').sum())
            st.metric("Negative Texts", (data['Sentiment_Label'] == 'Negative').sum())
            st.metric("Neutral Texts", (data['Sentiment_Label'] == 'Neutral').sum())

            # Visualizations
            st.markdown("#### Sentiment Distribution")
            
            # Bar Chart
            st.markdown("**Bar Chart**")
            sentiment_counts = data['Sentiment_Label'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis", ax=ax)
            ax.set_title("Sentiment Distribution (Bar Chart)")
            ax.set_xlabel("Sentiment")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            
            # Pie Chart
            st.markdown("**Pie Chart**")
            sentiment_counts = data['Sentiment_Label'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index, 
                values=sentiment_counts.values,
                hoverinfo='value+percent'  # Move hoverinfo here
            )])
            fig.update_layout(
                title="Sentiment Distribution (Pie Chart)",
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Word Clouds
            st.markdown("**Word Clouds**")
            positive_words = " ".join(data[data['Sentiment_Label'] == 'Positive']['Clean_Text'])
            negative_words = " ".join(data[data['Sentiment_Label'] == 'Negative']['Clean_Text'])
            neutral_words = " ".join(data[data['Sentiment_Label'] == 'Neutral']['Clean_Text'])
            
            # Create subplots for word clouds
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            # Positive words word cloud
            positive_wordcloud = WordCloud(width=400, height=300, background_color='white', max_words=100).generate(positive_words)
            axes[0].imshow(positive_wordcloud, interpolation='bilinear')
            axes[0].set_title("Positive Words")
            axes[0].axis('off')
            
            # Negative words word cloud
            negative_wordcloud = WordCloud(width=400, height=300, background_color='white', max_words=100).generate(negative_words)
            axes[1].imshow(negative_wordcloud, interpolation='bilinear')
            axes[1].set_title("Negative Words")
            axes[1].axis('off')
            
            # Neutral words word cloud
            neutral_wordcloud = WordCloud(width=400, height=300, background_color='white', max_words=100).generate(neutral_words)
            axes[2].imshow(neutral_wordcloud, interpolation='bilinear')
            axes[2].set_title("Neutral Words")
            axes[2].axis('off')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Sentiment Over Time (if a date column exists)
            st.markdown("#### Sentiment Over Time")
            date_columns = [col for col in data.columns if 'date' in col.lower()]
            if date_columns:
                date_column = st.selectbox("Select a date column for time-based analysis", date_columns)
                
                if date_column in data.columns:
                    
                    # Ensure date is in datetime format
                    data[date_column] = pd.to_datetime(data[date_column])
                    
                    # Group by date and calculate sentiment counts
                    daily_sentiment = data.groupby(pd.Grouper(key=date_column, freq='D'))['Sentiment_Label'].value_counts().unstack().fillna(0)
                    
                    # Create an interactive line chart
                    fig = go.Figure()
                    for label in daily_sentiment.columns:
                        fig.add_trace(go.Scatter(x=daily_sentiment.index, y=daily_sentiment[label],
                                               mode='lines', name=label))
                    
                    fig.update_layout(
                        title="Sentiment Over Time",
                        xaxis_title="Date",
                        yaxis_title="Count",
                        hovermode='x unified',
                        margin=dict(l=10, r=10, t=30, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Selected column does not contain text data.")
        
    
        # Download sentiment analysis results
        st.markdown("#### Download Results")
        results = data[[text_column, 'Clean_Text', 'Sentiment', 'Sentiment_Label']]
        results.to_csv("sentiment_analysis.csv", index=False)

        file = open("sentiment_analysis.csv", "rb")
        st.download_button(
            label="Download CSV",
            data=file,
            file_name="sentiment_analysis.csv",
            mime="text/csv",
        )
        file.close()