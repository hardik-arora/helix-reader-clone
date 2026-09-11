#!/usr/bin/env python3
"""
Digital Library Database Search Engine.
Implements SQL LIKE query matching, custom relevance ranking,
and graceful fallback suggestions.
"""

import os
import sqlite3

def search_library(db_path, query_term):
    """
    Searches the database for resources matching the query_term in title, author, topic, or keywords.
    Ranks the results: Exact title match > Topic match > Keyword overlap.
    Returns a list of ranked dicts, or a fallback suggestion dictionary if no matches are found.
    """
    if not os.path.exists(db_path):
        return {
            "status": "error",
            "message": "Database not found. Please run db_setup.py first."
        }

    query_term_clean = query_term.strip().lower()
    if not query_term_clean:
        return {
            "status": "fallback",
            "message": "Search query is empty. Try a broader topic."
        }

    conn = sqlite3.connect(db_path)
    # Use DictRow-like factory for cleaner dictionary access
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Search pattern for SQL LIKE query
    like_pattern = f"%{query_term_clean}%"

    # Query matching title, author, topic, or keywords
    sql_query = """
        SELECT resource_id, title, author, topic, excerpt, reading_level, summary, source_url, keywords, dictionary
        FROM resources
        WHERE title LIKE ? 
           OR author LIKE ? 
           OR topic LIKE ? 
           OR keywords LIKE ?;
    """

    cursor.execute(sql_query, (like_pattern, like_pattern, like_pattern, like_pattern))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {
            "status": "fallback",
            "message": "No matching resources found. Try a broader topic."
        }

    # Convert sqlite3.Row objects to dictionaries
    results = [dict(row) for row in rows]

    # Ranking helper function
    def calculate_rank(record):
        title = record["title"].strip().lower()
        topic = record["topic"].strip().lower()
        
        # 1. Exact title match (highest weight)
        exact_title_match = 1 if query_term_clean == title else 0
        
        # 2. Topic match (second highest weight)
        topic_match = 1 if query_term_clean == topic else 0
        
        # 3. Keyword overlap (third highest weight)
        # Parse keywords into a list
        keywords_list = [k.strip().lower() for k in record["keywords"].split(",") if k.strip()]
        # Tokenize query term to check overlaps
        query_words = set(query_term_clean.replace(",", " ").split())
        keyword_overlap = len(query_words.intersection(keywords_list))

        # Secondary match rules to ensure sorting robustness
        # e.g., partial title match is better than just a random keyword match
        partial_title_match = 1 if query_term_clean in title else 0
        author_match = 1 if query_term_clean in record["author"].strip().lower() else 0

        # Returns a tuple representing ranking criteria (higher values are better)
        # Python sorts tuples element-by-element
        return (exact_title_match, topic_match, keyword_overlap, partial_title_match, author_match)

    # Sort results using the rank calculation tuple in descending order
    results.sort(key=calculate_rank, reverse=True)

    return {
        "status": "success",
        "results": results
    }

def print_search_results(query, response):
    """
    Utility function to format and print search results cleanly.
    """
    print(f"\n--- Search Query: '{query}' ---")
    if response["status"] == "fallback":
        print(f"Suggestion: {response['message']}")
    elif response["status"] == "error":
        print(f"Error: {response['message']}")
    else:
        results = response["results"]
        print(f"Found {len(results)} matching resources:")
        for idx, item in enumerate(results, start=1):
            print(f"\n{idx}. [{item['topic']}] {item['title']} by {item['author']}")
            print(f"   Reading Level: {item['reading_level']}")
            print(f"   Keywords: {item['keywords']}")
            print(f"   Summary: {item['summary']}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "library.db")

    # Define test queries to show the ranking logic in action
    test_queries = [
        "Cosmos",            # Exact title match (Carl Sagan's Cosmos)
        "Science",           # Topic match (all Science books)
        "evolution",         # Keyword match (should match Dawkins, Darwin, Harari etc.)
        "Stephen Hawking",   # Author match
        "quantum physics",   # Partial keyword/topic overlap
        "Quantum-aliens-xyz" # No match (triggers fallback)
    ]

    for query in test_queries:
        res = search_library(db_path, query)
        print_search_results(query, res)

if __name__ == "__main__":
    main()
