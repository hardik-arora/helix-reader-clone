#!/usr/bin/env python3
"""
sync_covers.py - Helix Reader Clone Cover Synchronizer
"""
import csv
import os
import sys

SITE_DIR = "/Users/hardikarora/.gemini/antigravity-ide/scratch/helix-reader-clone"
CSV_PATH = os.path.join(SITE_DIR, "digital_library_starter.csv")

CATALOG = {
  "A Brief History of Time": "https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg?default=false",
  "The Origin of Species": "https://covers.openlibrary.org/b/isbn/9780140432053-L.jpg?default=false",
  "Cosmos": "https://covers.openlibrary.org/b/isbn/9780345331359-L.jpg?default=false",
  "The Selfish Gene": "https://covers.openlibrary.org/b/isbn/9780199291151-L.jpg?default=false",
  "The Double Helix": "https://covers.openlibrary.org/b/isbn/9780743216302-L.jpg?default=false",
  "Silent Spring": "https://covers.openlibrary.org/b/isbn/9780618249060-L.jpg?default=false",
  "Sapiens: A Brief History of Humankind": "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg?default=false",
  "Guns, Germs, and Steel": "https://covers.openlibrary.org/b/isbn/9780393317558-L.jpg?default=false",
  "A People's History of the United States": "https://covers.openlibrary.org/b/isbn/9780060838652-L.jpg?default=false",
  "The Rise and Fall of the Third Reich": "https://covers.openlibrary.org/b/isbn/9781451651683-L.jpg?default=false",
  "The Diary of a Young Girl": "https://covers.openlibrary.org/b/isbn/9780553296983-L.jpg?default=false",
  "The Republic": "https://covers.openlibrary.org/b/isbn/9780140449143-L.jpg?default=false",
  "Meditations": "https://covers.openlibrary.org/b/isbn/9780140449334-L.jpg?default=false",
  "Beyond Good and Evil": "https://books.google.com/books/content?vid=isbn9780140449233&printsec=frontcover&img=1&zoom=1",
  "Critique of Pure Reason": "https://covers.openlibrary.org/b/isbn/9780140447477-L.jpg?default=false",
  "The Prince": "https://covers.openlibrary.org/b/isbn/9780140449150-L.jpg?default=false",
  "1984": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg?default=false",
  "To Kill a Mockingbird": "https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg?default=false",
  "The Great Gatsby": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg?default=false",
  "Pride and Prejudice": "https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg?default=false",
  "Frankenstein": "https://covers.openlibrary.org/b/isbn/9780141439471-L.jpg?default=false",
  "Moby-Dick": "https://covers.openlibrary.org/b/isbn/9780142437247-L.jpg?default=false",
  "The Mythical Man-Month": "https://covers.openlibrary.org/b/isbn/9780201835953-L.jpg?default=false",
  "Clean Code": "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg?default=false",
  "Introduction to Algorithms": "https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg?default=false",
  "Design Patterns": "https://covers.openlibrary.org/b/isbn/9780201633610-L.jpg?default=false",
  "Steve Jobs": "https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg?default=false",
  "Long Walk to Freedom": "https://covers.openlibrary.org/b/isbn/9780316548182-L.jpg?default=false",
  "The Autobiography of Malcolm X": "https://covers.openlibrary.org/b/isbn/9780345350688-L.jpg?default=false",
  "Alexander Hamilton": "https://covers.openlibrary.org/b/isbn/9780143034759-L.jpg?default=false",
  "The Wealth of Nations": "https://covers.openlibrary.org/b/isbn/9780140436075-L.jpg?default=false",
  "Das Kapital": "https://covers.openlibrary.org/b/isbn/9780140445688-L.jpg?default=false",
  "The Interpretation of Dreams": "https://books.google.com/books/content?vid=isbn9780141184944&printsec=frontcover&img=1&zoom=1",
  "Gitanjali": "https://books.google.com/books/content?vid=isbn9781420926590&printsec=frontcover&img=1&zoom=1",
  "The Odyssey": "https://covers.openlibrary.org/b/isbn/9780140268867-L.jpg?default=false",
  "The Prince and the Pauper": "https://books.google.com/books/content?vid=isbn9780140350173&printsec=frontcover&img=1&zoom=1",
  "The Art of War": "https://covers.openlibrary.org/b/isbn/9780140449181-L.jpg?default=false",
  "The Elements": "https://covers.openlibrary.org/b/isbn/9780486600888-L.jpg?default=false",
  "Walden": "https://covers.openlibrary.org/b/isbn/9780140390445-L.jpg?default=false",
  "Understanding Media": "https://covers.openlibrary.org/b/isbn/9780262631594-L.jpg?default=false"
}

def main():
    print(f"📖 Synchronizing covers for: {CSV_PATH}")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    for idx, row in enumerate(rows, 1):
        title = row.get("title", "").strip()
        if title in CATALOG:
            row["cover_url"] = CATALOG[title]
        print(f"[{idx:02d}/{len(rows)}] {title:<35} | Cover: {row['cover_url']}")

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("🎉 Successfully synchronized all covers!")

if __name__ == "__main__":
    main()
