#!/usr/bin/env python3
"""
Simple MeshOS Data Pipeline Demo for OLake DevRel Assignment
This script demonstrates the complete data pipeline using your real meshOS data
"""

import pandas as pd
import sqlite3
import json
from datetime import datetime
import os

def create_demo_pipeline():
    """Create a simple but complete data pipeline demo"""
    
    print("🚀 Starting MeshOS Data Pipeline Demo")
    print("=" * 50)
    
    # Step 1: Read CSV data (simulating extraction from PostgreSQL)
    print("📊 Step 1: Reading CSV data...")
    
    try:
        habits_df = pd.read_csv('Habits.csv')
        checkmarks_df = pd.read_csv('Checkmarks.csv') 
        scores_df = pd.read_csv('Scores.csv')
        
        print(f"✅ Loaded {len(habits_df)} habits")
        print(f"✅ Loaded {len(checkmarks_df)} daily tracking records")
        print(f"✅ Loaded {len(scores_df)} score records")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure your CSV files are in the current directory")
        return
    
    # Step 2: Transform data (simulating OLake transformation)
    print("\n🔄 Step 2: Transforming data...")
    
    # Transform habits data
    habits_clean = habits_df.copy()
    habits_clean['id'] = range(1, len(habits_clean) + 1)
    habits_clean['user_id'] = 1
    habits_clean['created_at'] = datetime.now().isoformat()
    
    # Transform checkmarks from wide to long format
    checkmarks_long = checkmarks_df.melt(
        id_vars=['Date'],
        var_name='habit_name', 
        value_name='value'
    )
    checkmarks_long['date'] = pd.to_datetime(checkmarks_long['Date']).dt.date
    checkmarks_long['user_id'] = 1
    
    # Map habit names to IDs
    habit_mapping = {
        'Vaping': 1, 'Quit Valorant': 2, 'Walk': 3, 'Wake Up Early': 4,
        'No Pot': 5, 'No Energy Drink': 6, 'Coding': 7, 'Shower': 8,
        'University': 9, 'Gym': 10
    }
    checkmarks_long['habit_id'] = checkmarks_long['habit_name'].map(habit_mapping)
    checkmarks_clean = checkmarks_long.dropna()
    
    # Transform scores similarly
    scores_long = scores_df.melt(
        id_vars=['Date'],
        var_name='habit_name',
        value_name='score'
    )
    scores_long['date'] = pd.to_datetime(scores_long['Date']).dt.date
    scores_long['user_id'] = 1
    scores_long['habit_id'] = scores_long['habit_name'].map(habit_mapping)
    scores_clean = scores_long.dropna()
    
    print(f"✅ Transformed {len(checkmarks_clean)} checkmark entries")
    print(f"✅ Transformed {len(scores_clean)} score entries")
    
    # Step 3: Load into database (simulating Iceberg storage)
    print("\n💾 Step 3: Loading into database...")
    
    # Create SQLite database (simulating Iceberg tables)
    conn = sqlite3.connect('meshos_warehouse.db')
    
    # Create tables
    habits_clean.to_sql('habits', conn, if_exists='replace', index=False)
    checkmarks_clean.to_sql('habit_checkmarks', conn, if_exists='replace', index=False)
    scores_clean.to_sql('habit_scores', conn, if_exists='replace', index=False)
    
    print("✅ Created habits table")
    print("✅ Created habit_checkmarks table") 
    print("✅ Created habit_scores table")
    
    # Step 4: Analytics queries (simulating Spark SQL)
    print("\n📈 Step 4: Running analytics queries...")
    
    # Query 1: Habit performance overview
    query1 = """
    SELECT 
        h.Name,
        h.Color,
        AVG(hs.score) as avg_score,
        COUNT(hc.value) as total_entries
    FROM habits h
    LEFT JOIN habit_scores hs ON h.id = hs.habit_id
    LEFT JOIN habit_checkmarks hc ON h.id = hc.habit_id
    GROUP BY h.id, h.Name, h.Color
    ORDER BY avg_score DESC
    """
    
    results1 = pd.read_sql_query(query1, conn)
    print("\n🏆 Habit Performance Overview:")
    print(results1.to_string(index=False))
    
    # Query 2: Recent trends
    query2 = """
    SELECT 
        date,
        AVG(CASE WHEN habit_name NOT IN ('Vaping') THEN score ELSE NULL END) as positive_habits_avg,
        AVG(CASE WHEN habit_name = 'Vaping' THEN score ELSE NULL END) as vaping_score
    FROM habit_scores
    WHERE date >= date('now', '-7 days')
    GROUP BY date
    ORDER BY date DESC
    """
    
    results2 = pd.read_sql_query(query2, conn)
    print("\n📅 Recent 7-Day Trend:")
    print(results2.to_string(index=False))
    
    # Query 3: Correlation analysis
    query3 = """
    SELECT 
        AVG(CASE WHEN habit_name = 'Coding' THEN score END) as avg_coding,
        AVG(CASE WHEN habit_name = 'Gym' THEN score END) as avg_gym,
        AVG(CASE WHEN habit_name = 'Walk' THEN score END) as avg_walk
    FROM habit_scores
    """
    
    results3 = pd.read_sql_query(query3, conn)
    print("\n🔗 Habit Correlation Data:")
    print(results3.to_string(index=False))
    
    # Generate summary report
    summary = {
        "pipeline_execution_time": datetime.now().isoformat(),
        "data_sources": {
            "habits": len(habits_clean),
            "checkmarks": len(checkmarks_clean), 
            "scores": len(scores_clean)
        },
        "key_insights": {
            "top_performing_habit": results1.iloc[0]['Name'],
            "top_habit_score": float(results1.iloc[0]['avg_score']),
            "total_tracking_days": len(checkmarks_df),
            "habits_tracked": len(habits_clean)
        }
    }
    
    # Save summary
    with open('pipeline_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    conn.close()
    
    print("\n🎉 Pipeline Complete!")
    print("=" * 50)
    print(f"✅ Database created: meshos_warehouse.db")
    print(f"✅ Summary saved: pipeline_summary.json")
    print(f"✅ Top performing habit: {summary['key_insights']['top_performing_habit']}")
    print(f"✅ Total tracking days: {summary['key_insights']['total_tracking_days']}")
    
    return summary

if __name__ == "__main__":
    summary = create_demo_pipeline()
    
    print("\n📊 For your assignment video, you can show:")
    print("1. This script running the complete pipeline")
    print("2. The SQLite database with real data")
    print("3. The analytics queries and insights")
    print("4. How this demonstrates OLake-style ETL concepts")
    print("\n🚀 This shows the SAME data engineering concepts as OLake + Iceberg!")