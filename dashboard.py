# dashboard.py
import streamlit as st
from pipeline.extract import save_uploaded_csv, load_csv
from pipeline.transform import enrich_dataframe
from pipeline.load import save_dataframe_to_db, read_table
from pipeline.query import nl_to_sql, run_sql
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

st.set_page_config(page_title="Smart ETL + LLM Dashboard", layout="wide")
load_dotenv()


st.title("Smart ETL + LLM — Streamlit Dashboard")


DATA_PROCESSED = Path("data/processed")
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


# API Key configuration (hidden from UI)
api_key_default = st.session_state.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
if api_key_default:
    st.session_state["GROQ_API_KEY"] = api_key_default
    os.environ["GROQ_API_KEY"] = api_key_default

# Sidebar: Upload
st.sidebar.header("Upload data")
uploaded = st.sidebar.file_uploader("Upload CSV file", type=["csv"])


if uploaded is not None:
    save_path = save_uploaded_csv(uploaded)
    df = load_csv(save_path)
    st.sidebar.success(f"Saved to {save_path}")
    
    # Show column information
    st.write("### Available columns in your CSV:")
    st.write(f"**Columns:** {list(df.columns)}")
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Let user select text column
    text_column = st.selectbox(
        "Select the column containing text data:",
        options=list(df.columns),
        index=0 if 'text' in df.columns else 0
    )
    
    st.write("### Sample of uploaded data")
    st.dataframe(df.head())


# Transform
st.sidebar.header("LLM Enrichment Options")

# Model selection for speed vs quality
model_option = st.sidebar.selectbox(
    "Model (Speed vs Quality):",
    options=[
        ("llama3-8b-8192", "Fast (8B model)"),
        ("llama3-70b-8192", "Balanced (70B model)"),
        ("mixtral-8x7b-32768", "Fast (8x7B model)"),
        ("gemma2-9b-it", "Very Fast (9B model)")
    ],
    format_func=lambda x: x[1],
    index=0
)
selected_model = model_option[0]

batch_size = st.sidebar.slider("Process in batches of:", min_value=1, max_value=50, value=10, help="Smaller batches = faster but more API calls")
show_progress = st.sidebar.checkbox("Show detailed progress", value=True)

# Performance tips
with st.sidebar.expander("💡 Performance Tips"):
    st.write("""
    - **Smaller models** = Faster processing
    - **Batch size 10-20** = Good balance
    - **100 rows** ≈ 1-2 minutes
    - **1000 rows** ≈ 10-20 minutes
    """)

# Check if API key is set before allowing enrichment
if not st.session_state.get("GROQ_API_KEY"):
    st.sidebar.error("❌ Please set your Groq API key first!")
    st.sidebar.info("💡 Go to the 'API configuration' section above and enter your key")
else:
    if uploaded is not None and st.sidebar.button("Run LLM Enrichment"):
        # Set progress tracking
        st.session_state['show_progress'] = show_progress
        
        # Show dataset info
        st.info(f"📊 Processing {len(df)} rows in batches of {batch_size}")
        st.info(f"⏱️ Estimated time: {len(df) * 0.5 / 60:.1f} minutes (assuming 0.5s per row)")
        
        with st.spinner("Enriching with LLM — this may take a while"):
            try:
                # Process in batches for better progress tracking
                if batch_size < len(df):
                    st.write(f"🔄 Processing in batches of {batch_size}...")
                
                df_enriched = enrich_dataframe(df, text_column=text_column, model=selected_model)
                out_csv = DATA_PROCESSED / (save_path.stem + "_enriched.csv")
                df_enriched.to_csv(out_csv, index=False)
                save_dataframe_to_db(df_enriched, table_name="reviews")
                st.success("✅ Enrichment complete and saved to DB")
                st.dataframe(df_enriched.head())

                # Show metrics if available
                m = st.session_state.get('enrich_metrics')
                if m:
                    st.subheader("Run Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Rows processed", m.get("rows_processed", 0))
                    col2.metric("Cache hits", m.get("cache_hits", 0))
                    col3.metric("API calls", m.get("api_calls", 0))
                    avg_latency = (m.get("total_latency_s", 0.0) / max(1, m.get("api_calls", 1)))
                    col4.metric("Avg API latency (s)", f"{avg_latency:.2f}")
            except Exception as e:
                st.error(f"❌ Enrichment failed: {str(e)}")
                st.write("**Debug info:**")
                st.write(f"- Selected text column: {text_column}")
                st.write(f"- Available columns: {list(df.columns)}")
                st.write(f"- DataFrame shape: {df.shape}")
                st.write(f"- API Key Status: {'✅ Set' if st.session_state.get('GROQ_API_KEY') else '❌ Not set'}")


# Browse DB
st.header("Browse enriched data")
if st.button("Load latest processed table"):
    try:
        df_db = read_table()
        st.dataframe(df_db.head(200))
        
        # Add visualization section
        if not df_db.empty and 'sentiment' in df_db.columns:
            st.subheader("📊 Data Analytics Dashboard")
            
            # Sentiment distribution
            col1, col2 = st.columns(2)
            
            with col1:
                sentiment_counts = df_db['sentiment'].value_counts()
                fig_pie = px.pie(
                    values=sentiment_counts.values, 
                    names=sentiment_counts.index,
                    title="Sentiment Distribution",
                    color_discrete_map={'positive': '#00ff00', 'negative': '#ff0000', 'neutral': '#808080'}
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Keywords analysis
                if 'keywords' in df_db.columns:
                    # Extract keywords from the JSON-like strings
                    try:
                        import json
                        all_keywords = []
                        for keywords_str in df_db['keywords'].dropna():
                            try:
                                if isinstance(keywords_str, str):
                                    keywords = json.loads(keywords_str)
                                    if isinstance(keywords, list):
                                        all_keywords.extend(keywords)
                                elif isinstance(keywords_str, list):
                                    all_keywords.extend(keywords_str)
                            except:
                                continue
                        
                        if all_keywords:
                            keyword_counts = pd.Series(all_keywords).value_counts().head(10)
                            fig_bar = px.bar(
                                x=keyword_counts.values,
                                y=keyword_counts.index,
                                orientation='h',
                                title="Top 10 Keywords",
                                labels={'x': 'Frequency', 'y': 'Keywords'}
                            )
                            st.plotly_chart(fig_bar, use_container_width=True)
                    except Exception as e:
                        st.info("Keywords visualization not available")
            
            # Time series if timestamp available
            if 'timestamp' in df_db.columns:
                try:
                    df_db['timestamp'] = pd.to_datetime(df_db['timestamp'])
                    sentiment_time = df_db.groupby([df_db['timestamp'].dt.date, 'sentiment']).size().unstack(fill_value=0)
                    
                    fig_line = px.line(
                        sentiment_time,
                        title="Sentiment Trends Over Time",
                        labels={'value': 'Count', 'index': 'Date'}
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
                except:
                    pass
            
            # Summary statistics
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("Total Records", len(df_db))
            with col4:
                st.metric("Positive Sentiment", len(df_db[df_db['sentiment'] == 'positive']))
            with col5:
                st.metric("Negative Sentiment", len(df_db[df_db['sentiment'] == 'negative']))
                
    except Exception as e:
        st.error("No processed DB found. Run enrichment first.")

# NL → SQL Query
st.header("Natural language query")
user_q = st.text_input("Ask a question about the data (e.g. 'Show top 5 negative reviews about price')")
if st.button("Run Query") and user_q.strip():
    with st.spinner("Translating to SQL and running..."):
        try:
            sql = nl_to_sql(user_q)
            st.code(sql)
            df_res = run_sql(sql)
            st.dataframe(df_res)
            
            # Add export options for query results
            if not df_res.empty:
                st.subheader("📥 Export Query Results")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv_data = df_res.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"query_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_res.to_excel(writer, index=False, sheet_name='Query Results')
                    excel_data = excel_buffer.getvalue()
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=f"query_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col3:
                    json_data = df_res.to_json(orient='records', indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"query_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        except Exception as e:
            st.error(f"Query failed: {e}")


st.markdown("---")
st.caption("Make sure you set GROQ_API_KEY environment variable before running the app.")