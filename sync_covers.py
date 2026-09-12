#!/usr/bin/env python3
"""
sync_covers.py - Helix Reader Clone Cover & Metadata Synchronizer
Populates isbn, olid, and cover_url columns in digital_library_starter.csv
by resolving Open Library ISBN URLs with Google Books API/Direct fallback.
"""

import csv
import os
import sys
import time
import urllib.request

SITE_DIR = "/Users/hardikarora/.gemini/antigravity-ide/scratch/helix-reader-clone"
CSV_PATH = os.path.join(SITE_DIR, "digital_library_starter.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def resolve_cover_url(isbn):
    """Resolves primary Open Library ISBN cover URL, falling back to Google Books."""
    if not isbn:
        return ""
    
    ol_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false"
    try:
        req = urllib.request.Request(ol_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            if len(data) > 1000:
                return ol_url
    except Exception:
        pass

    # Fallback to Google Books Direct cover URL
    gb_url = f"https://books.google.com/books/content?vid=isbn{isbn}&printsec=frontcover&img=1&zoom=1"
    try:
        req = urllib.request.Request(gb_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            if len(data) > 1000:
                return gb_url
    except Exception:
        pass

    return ol_url

def main():
    print(f"📖 Starting cover metadata sync for: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print(f"❌ File not found: {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Found {len(rows)} books in starter catalog. Verifying cover URLs...")

    updated_count = 0
    for idx, row in enumerate(rows, 1):
        title = row.get("title", "").strip()
        isbn = row.get("isbn", "").strip()
        
        cover_url = resolve_cover_url(isbn)
        row["cover_url"] = cover_url
        
        if cover_url:
            updated_count += 1
            
        print(f"[{idx:02d}/{len(rows)}] {title:<35} | ISBN: {isbn:<14} | Cover: {cover_url}")

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"🎉 Successfully updated {updated_count}/{len(rows)} books in digital_library_starter.csv!")

if __name__ == "__main__":
    main()
