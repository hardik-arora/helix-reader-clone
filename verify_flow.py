#!/usr/bin/env python3
"""
Integration Flow Verification Script.
Programmatically validates the complete data flow:
1. SQLite search connection and retrieval.
2. AI/NLP reading difficulty and recommendation logic.
3. Easy mode text segmentation/accessibility formatting.
4. AI simplification & glossary layout checks.
"""

import os
import sqlite3
import re
from search import search_library
from ai_tools import (
    estimate_reading_difficulty,
    extract_keywords,
    get_reading_recommendation,
    simplify_text_ai,
    generate_glossary_ai
)

def run_integration_verification():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "library.db")

    print("==================================================")
    # Verification Heading
    print("🚦 INTEGRATION FLOW VERIFICATION SUITE")
    print("==================================================")

    # 1. Database Connectivity and Query Test
    print("\nSTEP 1: Testing SQLite Connectivity and search_library...")
    query = "evolution"
    search_res = search_library(db_path, query)
    
    if search_res["status"] != "success":
        print(f"❌ FAIL: Database search returned status '{search_res['status']}'")
        return False
    
    results = search_res["results"]
    print(f"✅ PASS: Successfully queried DB. Found {len(results)} matches for '{query}'.")
    
    # Select the first matching resource (Origin of Species)
    target_book = results[0]
    print(f"👉 Target Book selected: '{target_book['title']}' by {target_book['author']}")

    # 2. NLP Analysis Test
    print("\nSTEP 2: Validating rule-based NLP Analysis...")
    excerpt = target_book["excerpt"]
    
    # Estimate Difficulty
    difficulty = estimate_reading_difficulty(excerpt)
    # Extract Keywords
    keywords = extract_keywords(excerpt)
    
    if not difficulty or not keywords:
        print("❌ FAIL: NLP extraction returned empty results.")
        return False
        
    print(f"✅ PASS: Extracted keywords: {keywords}")
    print(f"✅ PASS: Calculated Readability Score: {difficulty['score']} ({difficulty['level']})")

    # 3. Reading Recommendations (Next Steps) Engine Test
    print("\nSTEP 3: Testing actionable support recommendation logic (User Level: Middle School)...")
    recs = get_reading_recommendation(difficulty, user_reading_level="Middle School")
    
    if not recs["recommendations"]:
        print("❌ FAIL: Support recommendation list is empty.")
        return False
        
    for idx, rec in enumerate(recs["recommendations"], 1):
        print(f"   [Rec {idx}] {rec}")
    print("✅ PASS: Actionable support recommendations successfully calculated.")

    # 4. Accessibility Easy Mode Formatting Test
    print("\nSTEP 4: Simulating 'Easy Mode' paragraph-by-paragraph text segmentation...")
    text_segments = [s.strip() for s in re.split(r'(?<=[.!?])\s+', excerpt) if s.strip()]
    
    if len(text_segments) < 1:
        print("❌ FAIL: Text segment splitting failed.")
        return False
        
    print(f"✅ PASS: Successfully parsed text into {len(text_segments)} readable segments.")
    for idx, segment in enumerate(text_segments, start=1):
        print(f"   [Segment {idx}] \"{segment}\"")

    # 5. AI tools functions check
    print("\nSTEP 5: Verifying AI layout simulation modules...")
    simplified_text = simplify_text_ai(excerpt, target_level="Middle School")
    glossary = generate_glossary_ai(excerpt)
    
    if not simplified_text or not glossary:
        print("❌ FAIL: AI simulation layout functions returned null.")
        return False
        
    print(f"✅ PASS: AI Text Simplification layout returned: \"{simplified_text}\"")
    print(f"✅ PASS: AI Glossary Generation layout returned: {len(glossary)} definition(s).")

    print("\n==================================================")
    print("🎉 ALL INTEGRATION FLOWS VERIFIED SUCCESSFULLY!")
    print("==================================================")
    return True

if __name__ == "__main__":
    run_integration_verification()
