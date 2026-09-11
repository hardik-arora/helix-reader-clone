# 🧬 Helix Reader — Next-Gen Kindle Rebuild

A premium, feature-rich, Kindle-inspired digital library application providing access to **15,000 locally cataloged works** and querying a global index of **158 million digitized books**.

## 🚀 Live & Local Links

- 🌐 **Live Website Link:** **[https://hardik-arora.github.io/helix-reader/](https://hardik-arora.github.io/helix-reader/)**
- 📄 **Presentation PDF Deck:** **[https://hardik-arora.github.io/helix-reader/helix_reader_presentation.pdf](https://hardik-arora.github.io/helix-reader/helix_reader_presentation.pdf)**
- 📊 **Presentation PowerPoint (PPTX):** **[https://hardik-arora.github.io/helix-reader/helix_reader_presentation.pptx](https://hardik-arora.github.io/helix-reader/helix_reader_presentation.pptx)**

---

## 📂 Repository File Directory

This repository contains the complete frontend, database backend, NLP engines, and presentation materials for Helix Reader:

*   **[`index.html`](./index.html)**: The main Kindle-style digital reader web app featuring 28 themes, real-time TTS voice reading with word highlights, floating dictionary, and Firebase sync.
*   **[`helix_reader_presentation.pdf`](./helix_reader_presentation.pdf)**: Official Hackathon presentation slide deck (PDF format).
*   **[`helix_reader_presentation.pptx`](./helix_reader_presentation.pptx)**: Official Hackathon presentation slide deck (editable PowerPoint format).
*   **[`app.py`](./app.py)**: Streamlit-based analytics dashboard and fallback reader interface.
*   **[`search.py`](./search.py)**: Multi-field search engine matching titles, authors, and keywords across catalogs.
*   **[`reading_support.py`](./reading_support.py)**: NLP readability engine for syllable count, reading difficulty scores, and focus advice.
*   **[`ai_tools.py`](./ai_tools.py)**: AI tools helper module for dictionary definitions, AI summaries, and quiz generators.
*   **[`db_setup.py`](./db_setup.py)**: Seeds the local SQLite database (`library.db`) and configures full-text search indexes.
*   **[`generate_data.py`](./generate_data.py)**: Dataset generator building the initial catalog of classic literature and global authors.
*   **[`digital_library_starter.csv`](./digital_library_starter.csv)**: Starter dataset containing 15,000+ cataloged works and metadata.
*   **[`monitor.html`](./monitor.html)**: System health and telemetry monitoring page.
*   **[`verify_flow.py`](./verify_flow.py)**: Automated verification test script for end-to-end user flows.


---

## 🌟 Key Features

1. **🌐 158 Million Book Index & Platform Selector**: Query the global digital library in real-time. Clicking "Read Book" launches a platform redirect modal connecting readers directly to digitized copies on **Project Gutenberg, Open Library, Google Books, and Internet Archive**.
2. **✍️ Global Authors Spotlight**: Features legendary literature spanning all continents, including a dedicated Indian literature registry (Rabindranath Tagore, Kalidasa, Arundhati Roy, R. K. Narayan, Premchand, Wings of Fire, and classical epics).
3. **🎭 Premium Styling & Themes**: Toggle between 28 premium themes (including 8 gorgeous linear gradients) instantly.
4. **🔊 Text-to-Speech (TTS) Voice Engine**: High-fidelity paragraph reading voice synthesis with active highlighting and speed controls.
5. **♿ Reading Focus Modes**: Dyslexic-friendly layouts (dyslexic letter-spacing) and sentence-by-sentence focus view toggles.
6. **📖 Floating Dictionary**: Highlight any word in the reader to view meanings, save vocabulary words, and trigger audio pronunciation.
7. **🧠 Quizzes & Badges**: Interactive multi-choice comprehension checkpoints with XP points and achievements.
8. **📥 Custom Document Importer**: Add personal logs or external articles and read them in the custom layout.
9. **🖊️ Highlighting & Vocabulary Sanctuary**: Store vocabulary logs and colored highlight extracts.
