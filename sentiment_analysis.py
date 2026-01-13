import plotly.express as px
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import streamlit as st
# removed seaborn and matplotlib imports
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
nltk.download('punkt_tab')

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
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Positive Texts", (data['Sentiment_Label'] == 'Positive').sum())
            with c2:
                st.metric("Negative Texts", (data['Sentiment_Label'] == 'Negative').sum())
            with c3:
                st.metric("Neutral Texts", (data['Sentiment_Label'] == 'Neutral').sum())

            # Visualizations
            st.markdown("#### Sentiment Distribution")
            
            c1, c2 = st.columns(2)
            
            with c1:
                # Bar Chart
                st.markdown("**Bar Chart**")
                sentiment_counts = data['Sentiment_Label'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                fig = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment', 
                             title="Sentiment Distribution", color_discrete_map={
                                 'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'
                             })
                st.plotly_chart(fig, width='stretch')
            
            with c2:
                # Pie Chart
                st.markdown("**Pie Chart**")
                # Recalculate to ensure sync/cleanliness
                sentiment_counts_pie = data['Sentiment_Label'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=sentiment_counts_pie.index, 
                    values=sentiment_counts_pie.values,
                    hoverinfo='value+percent',
                    marker=dict(colors=['green' if x=='Positive' else 'red' if x=='Negative' else 'gray' for x in sentiment_counts_pie.index])
                )])
                fig.update_layout(
                    title="Sentiment Distribution",
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig, width='stretch')
            
            # Word Clouds
            st.markdown("#### Word Clouds")
            positive_words = " ".join(data[data['Sentiment_Label'] == 'Positive']['Clean_Text'])
            negative_words = " ".join(data[data['Sentiment_Label'] == 'Negative']['Clean_Text'])
            neutral_words = " ".join(data[data['Sentiment_Label'] == 'Neutral']['Clean_Text'])
            
            t1, t2, t3 = st.tabs(["Positive Words", "Negative Words", "Neutral Words"])
            
            with t1:
                if positive_words.strip():
                    wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(positive_words)
                    st.image(wc.to_array(), caption="Positive Words", use_column_width=True)
                else:
                    st.info("No positive words found.")
            
            with t2:
                if negative_words.strip():
                    wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(negative_words)
                    st.image(wc.to_array(), caption="Negative Words", use_column_width=True)
                else:
                    st.info("No negative words found.")

            with t3:
                if neutral_words.strip():
                    wc = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(neutral_words)
                    st.image(wc.to_array(), caption="Neutral Words", use_column_width=True)
                else:
                    st.info("No neutral words found.")
            
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
                    st.plotly_chart(fig, width='stretch')
            
        else:
            st.warning("Selected column does not contain text data.")
        
    
        # Download sentiment analysis results
        st.markdown("#### Download Results")
        results = data[[text_column, 'Clean_Text', 'Sentiment', 'Sentiment_Label']]
        results.to_csv("sentiment_analysis.csv", index=False)
        
        # Use open/read/close pattern or better, just pass the string if st.download_button supports it, 
        # but to match previous logic, we use BytesIO or simple file read.
        # Actually simplest is to convert to csv string.
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="sentiment_analysis.csv",
            mime="text/csv",
        )