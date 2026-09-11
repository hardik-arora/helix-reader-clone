#!/usr/bin/env python3
"""
sync_covers.py - Helix Reader Clone Cover & Metadata Synchronizer
Populates isbn, olid, and cover_url columns in digital_library_starter.csv
by querying the Open Library Search API.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

SITE_DIR = "/Users/hardikarora/.gemini/antigravity-ide/scratch/helix-reader-clone"
CSV_PATH = os.path.join(SITE_DIR, "digital_library_starter.csv")

HEADERS = {
    "User-Agent": "HelixReader-CoverSync/1.0 (contact@helixreader.org)"
}

def fetch_open_library_metadata(title, author):
    """Queries Open Library Search API for title and author and extracts isbn, olid, cover_url."""
    query_str = f"{title} {author}".strip()
    encoded_q = urllib.parse.quote(query_str)
    url = f"https://openlibrary.org/search.json?q={encoded_q}&limit=1"
    
    req = urllib.request.Request(url, headers=HEADERS)
    isbn = ""
    olid = ""
    cover_url = ""
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            docs = data.get("docs", [])
            if docs:
                doc = docs[0]
                isbns = doc.get("isbn", [])
                if isbns:
                    isbn = str(isbns[0])
                
                olid = doc.get("cover_edition_key") or (doc.get("edition_key", [""])[0] if doc.get("edition_key") else "")
                cover_i = doc.get("cover_i")
                
                if cover_i:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"
                elif isbn:
                    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                elif olid:
                    cover_url = f"https://covers.openlibrary.org/b/olid/{olid}-L.jpg"
    except Exception as e:
        print(f"⚠️ Error querying Open Library for '{title}': {e}")
        
    return isbn, olid, cover_url

def main():
    print(f"📖 Starting cover metadata sync for: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print(f"❌ File not found: {CSV_PATH}")
        sys.exit(1)

    # Read existing CSV rows
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Found {len(rows)} books in starter catalog. Fetching metadata from Open Library...\n")

    updated_count = 0
    for idx, row in enumerate(rows, 1):
        title = row.get("title", "").strip()
        author = row.get("author", "").strip()
        
        isbn, olid, cover_url = fetch_open_library_metadata(title, author)
        
        # Populate fields
        row["isbn"] = isbn
        row["olid"] = olid
        row["cover_url"] = cover_url
        
        if cover_url:
            updated_count += 1
            
        print(f"[{idx:02d}/{len(rows)}] {title:<32} | ISBN: {isbn:<14} | OLID: {olid:<12} | Cover: {cover_url}")
        time.sleep(0.15) # Polite API rate limiting

    # Write updated rows back to CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n🎉 Successfully updated {updated_count}/{len(rows)} books in digital_library_starter.csv with real cover metadata!")

if __name__ == "__main__":
    main()
