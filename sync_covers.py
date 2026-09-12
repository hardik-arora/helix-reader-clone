#!/usr/bin/env python3
"""
sync_covers.py - Helix Reader Clone Cover & Metadata Synchronizer
Appends ?default=false to Open Library cover requests. If Open Library returns a 404
or placeholder, falls back to Google Books direct / API cover URL.
"""

import csv
import os
import sys
import time
import urllib.parse
import urllib.request

SITE_DIR = "/Users/hardikarora/.gemini/antigravity-ide/scratch/helix-reader-clone"
CSV_PATH = os.path.join(SITE_DIR, "digital_library_starter.csv")
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# Specific overrides for known books with missing Open Library covers
OVERRIDE_COVERS = {
    "Beyond Good and Evil": "https://books.google.com/books/content?vid=isbn9780140449233&printsec=frontcover&img=1&zoom=1",
    "The Interpretation of Dreams": "https://books.google.com/books/content?vid=isbn9780141184944&printsec=frontcover&img=1&zoom=1",
    "Gitanjali": "https://books.google.com/books/content?vid=isbn9781420926590&printsec=frontcover&img=1&zoom=1",
    "The Prince and the Pauper": "https://books.google.com/books/content?vid=isbn9780140350173&printsec=frontcover&img=1&zoom=1"
}

def resolve_cover(title, isbn, current_cover):
    if title in OVERRIDE_COVERS:
        return OVERRIDE_COVERS[title]
        
    if current_cover and "8276442-L.jpg" in current_cover:
        return f"https://books.google.com/books/content?vid=isbn{isbn}&printsec=frontcover&img=1&zoom=1"

    if isbn and isbn != "0000000000000":
        ol_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false"
        try:
            req = urllib.request.Request(ol_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = resp.read()
                if len(data) > 1000:
                    return ol_url
        except Exception:
            pass
        return f"https://books.google.com/books/content?vid=isbn{isbn}&printsec=frontcover&img=1&zoom=1"

    return current_cover or ""

def main():
    print(f"📖 Synchronizing covers for: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print(f"❌ File not found: {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated_count = 0
    for idx, row in enumerate(rows, 1):
        title = row.get("title", "").strip()
        isbn = row.get("isbn", "").strip()
        current_cover = row.get("cover_url", "").strip()

        new_cover = resolve_cover(title, isbn, current_cover)
        row["cover_url"] = new_cover
        
        # Ensure RES-PHI-0014 gets Google Books URL
        if row.get("resource_id") == "RES-PHI-0014" or title == "Beyond Good and Evil":
            row["cover_url"] = "https://books.google.com/books/content?vid=isbn9780140449233&printsec=frontcover&img=1&zoom=1"

        updated_count += 1
        print(f"[{idx:02d}/{len(rows)}] {title:<35} | Cover: {row['cover_url']}")

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n🎉 Successfully updated {updated_count}/{len(rows)} books in digital_library_starter.csv!")

if __name__ == "__main__":
    main()
