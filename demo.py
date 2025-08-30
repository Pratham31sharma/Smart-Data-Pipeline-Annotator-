#!/usr/bin/env python3
"""
Smart Data Pipeline Annotator - Demo Script
Demonstrates the pipeline's capabilities with sample data
"""

import pandas as pd
import os
from pathlib import Path
from pipeline.extract import save_uploaded_csv
from pipeline.transform import enrich_dataframe
from pipeline.load import save_dataframe_to_db, read_table
from pipeline.query import nl_to_sql, run_sql

def create_sample_data():
    """Create sample data for demonstration"""
    sample_data = {
        'review_id': range(1, 21),
        'text': [
            "This product is absolutely amazing! I love everything about it.",
            "Terrible quality, waste of money. Would not recommend.",
            "It's okay, nothing special but gets the job done.",
            "Excellent customer service and fast delivery.",
            "The product broke after just one week of use.",
            "Great value for money, exceeded my expectations.",
            "Average product, could be better for the price.",
            "Outstanding quality and durability.",
            "Poor packaging, item arrived damaged.",
            "Fantastic features and easy to use.",
            "Disappointed with the performance.",
            "Best purchase I've made this year!",
            "Not worth the price, very basic features.",
            "Amazing design and functionality.",
            "Customer support was unhelpful.",
            "High-quality materials and construction.",
            "Falls apart easily, very fragile.",
            "Perfect for my needs, highly recommend.",
            "Overpriced for what you get.",
            "Reliable and efficient product."
        ],
        'rating': [5, 1, 3, 5, 2, 5, 3, 5, 2, 5, 2, 5, 2, 5, 1, 5, 2, 5, 2, 4],
        'category': ['electronics'] * 20
    }
    
    df = pd.DataFrame(sample_data)
    return df

def run_demo():
    """Run the complete pipeline demonstration"""
    print("🚀 Smart Data Pipeline Annotator - Demo Mode")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️  GROQ_API_KEY not found. Please set it to run the full demo.")
        print("   You can still see the pipeline structure without AI enrichment.")
        demo_mode = False
    else:
        print("✅ GROQ_API_KEY found. Running full AI-powered demo.")
        demo_mode = True
    
    # Create sample data
    print("\n📊 Creating sample data...")
    df = create_sample_data()
    print(f"   Created {len(df)} sample reviews")
    
    # Save sample data
    print("\n💾 Saving sample data...")
    sample_path = Path("data/raw/sample_reviews.csv")
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(sample_path, index=False)
    print(f"   Saved to {sample_path}")
    
    # Show sample data
    print("\n📋 Sample Data Preview:")
    print(df.head(3).to_string(index=False))
    
    if demo_mode:
        # Run AI enrichment
        print("\n🤖 Running AI-powered enrichment...")
        try:
            df_enriched = enrich_dataframe(
                df, 
                text_column='text', 
                model='llama3-8b-8192'
            )
            
            # Save enriched data
            enriched_path = Path("data/processed/sample_reviews_enriched.csv")
            enriched_path.parent.mkdir(parents=True, exist_ok=True)
            df_enriched.to_csv(enriched_path, index=False)
            print(f"   Enriched data saved to {enriched_path}")
            
            # Save to database
            save_dataframe_to_db(df_enriched, table_name="sample_reviews")
            print("   Data saved to database")
            
            # Show enrichment results
            print("\n✨ Enrichment Results Preview:")
            print(df_enriched[['text', 'sentiment', 'keywords', 'summary']].head(3).to_string(index=False))
            
            # Demonstrate natural language querying
            print("\n🔍 Natural Language Query Demo:")
            queries = [
                "Show me all positive reviews",
                "What are the most common keywords?",
                "Show reviews with rating 5"
            ]
            
            for query in queries:
                print(f"\n   Query: '{query}'")
                try:
                    sql = nl_to_sql(query)
                    print(f"   SQL: {sql}")
                    result = run_sql(sql)
                    print(f"   Results: {len(result)} rows")
                    if len(result) <= 3:
                        print(f"   {result.to_string(index=False)}")
                except Exception as e:
                    print(f"   Error: {e}")
            
        except Exception as e:
            print(f"   ❌ Enrichment failed: {e}")
            print("   This might be due to API rate limits or configuration issues.")
    
    # Show pipeline structure
    print("\n🏗️  Pipeline Architecture:")
    print("   📁 data/raw/ - Input CSV files")
    print("   📁 data/processed/ - Enriched output files")
    print("   📁 pipeline/ - Core ETL components")
    print("   🐳 Dockerfile - Containerization")
    print("   📋 requirements.txt - Dependencies")
    
    print("\n🎯 Next Steps:")
    print("   1. Run 'streamlit run dashboard.py' for the web interface")
    print("   2. Upload your own CSV files for processing")
    print("   3. Customize the enrichment prompts in pipeline/transform.py")
    print("   4. Deploy with Docker for production use")
    
    print("\n✨ Demo completed! Your Smart Data Pipeline is ready to use.")

if __name__ == "__main__":
    run_demo()
