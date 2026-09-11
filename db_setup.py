#!/usr/bin/env python3
"""
SQLite Database Schema Definition and Seeding Tool.
Defines 'resources' and 'user_actions' tables with optimized indexes,
and seeds data including the new 'dictionary' definitions column.
"""

import csv
import os
import sqlite3

def create_database(db_path):
    """
    Creates the SQLite database and defines the schema with optimization indexes.
    """
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign key constraint support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create resources table
    print("Creating 'resources' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            resource_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            topic TEXT NOT NULL,
            excerpt TEXT,
            reading_level TEXT,
            summary TEXT,
            source_url TEXT,
            keywords TEXT,
            dictionary TEXT
        );
    """)

    # 2. Create user_actions table
    print("Creating 'user_actions' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_actions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id TEXT NOT NULL,
            action_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE
        );
    """)

    # 3. Create Optimization Indexes
    print("Creating optimization indexes on 'title', 'author', and 'topic'...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_resources_title ON resources(title);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_resources_author ON resources(author);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_resources_topic ON resources(topic);")

    conn.commit()
    return conn

def seed_database(conn, csv_path):
    """
    Reads the CSV file and seeds the data into the 'resources' table.
    """
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading data from CSV: {csv_path}")
    cursor = conn.cursor()
    
    records_inserted = 0
    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source_name = row.get("source", "")
            source_url = f"https://en.wikipedia.org/wiki/{source_name.replace(' ', '_')}" if source_name else None

            cursor.execute("""
                INSERT OR REPLACE INTO resources (
                    resource_id, title, author, topic, excerpt, reading_level, summary, source_url, keywords, dictionary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                row.get("resource_id"),
                row.get("title"),
                row.get("author"),
                row.get("topic"),
                row.get("excerpt"),
                row.get("reading_level"),
                row.get("summary"),
                source_url,
                row.get("keywords"),
                row.get("dictionary")
            ))
            records_inserted += 1

    conn.commit()
    print(f"Successfully seeded {records_inserted} records into the 'resources' table.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "library.db")
    csv_path = os.path.join(script_dir, "digital_library_starter.csv")

    # Create database schema
    conn = create_database(db_path)

    # Seed with CSV data
    seed_database(conn, csv_path)

    conn.close()
    print("Database setup and seeding completed successfully!")

if __name__ == "__main__":
    main()
