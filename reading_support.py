#!/usr/bin/env python3
"""
AI/ML Reading Support Layer.
Provides:
1. Rule-based NLP for keyword extraction and reading difficulty estimation.
2. AI API function layout (OpenAI style) for text simplification and glossary generation.
3. Actionable recommendation engine.
"""

import re
import os

# ---------------------------------------------------------
# Part 1: Rule-Based NLP Approach (Standard Python)
# ---------------------------------------------------------

# Standard English stop words to filter out for keyword extraction
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'
}

def count_syllables(word):
    """
    Heuristic syllable counter for English words.
    """
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    # Remove silent 'e' at the end
    if word.endswith('e'):
        word = word[:-1]
    
    # Count vowel groups
    vowel_groups = re.findall(r'[aeiouy]+', word)
    count = len(vowel_groups)
    
    # Adjust for common endings/rules
    if word.endswith('es') or word.endswith('ed'):
        count = max(1, count - 1)
    
    return max(1, count)

def extract_keywords(text, top_n=5):
    """
    Extracts top_n keywords from text based on frequency of non-stop words.
    """
    # Clean text: keep only alphanumeric words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter stop words
    filtered_words = [w for w in words if w not in STOP_WORDS]
    
    # Compute frequencies
    freq = {}
    for w in filtered_words:
        freq[w] = freq.get(w, 0) + 1
        
    # Sort by frequency and return top_n
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_keywords[:top_n]]

def estimate_reading_difficulty(text):
    """
    Estimates reading difficulty using a simplified Flesch-Kincaid score.
    Flesch Reading Ease Formula: 
    206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
    """
    # Split text into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    num_sentences = max(1, len(sentences))
    
    # Clean and split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    num_words = max(1, len(words))
    
    # Count syllables
    total_syllables = sum(count_syllables(w) for w in words)
    
    # Calculate components
    asl = num_words / num_sentences  # Average Sentence Length
    asw = total_syllables / num_words  # Average Syllables per Word
    
    # Flesch Reading Ease Score
    fre_score = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    # Map score to Reading Level
    if fre_score >= 90:
        level = "Elementary"
        desc = "Very easy to read. Typical of 5th grade level."
    elif fre_score >= 70:
        level = "Middle School"
        desc = "Easy to read. Standard conversational English."
    elif fre_score >= 50:
        level = "High School"
        desc = "Fairly difficult to read. High school level."
    else:
        level = "Academic"
        desc = "Difficult/Academic reading level. Best suited for university level."
        
    return {
        "level": level,
        "score": round(fre_score, 2),
        "desc": desc,
        "average_sentence_length": round(asl, 2),
        "average_syllables_per_word": round(asw, 2)
    }


# ---------------------------------------------------------
# Part 2: AI API Layout (OpenAI / Anthropic structure)
# ---------------------------------------------------------

def simplify_text_ai(text, target_level="Elementary", api_key=None):
    """
    Simulates / lays out the API call to OpenAI to simplify the text.
    To use: Install 'openai' package and configure your API key.
    """
    # Placeholder layout showing structure
    prompt = (
        f"You are an educational reading assistant. Please rewrite the following excerpt "
        f"so it is suitable for a reader at the '{target_level}' level. "
        f"Keep the core themes intact, but use simpler sentence structures and vocabulary.\n\n"
        f"Original text:\n{text}\n\n"
        f"Simplified text:"
    )
    
    # Layout representation of Client call:
    # 
    # from openai import OpenAI
    # client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful educational reading assistant."},
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.7
    # )
    # return response.choices[0].message.content.strip()
    
    # Return structured simulation representation
    return f"[AI Simplified Version for {target_level} Level (Simulation Prompt Outlined)]"

def generate_glossary_ai(text, api_key=None):
    """
    Simulates / lays out the API call to identify complex terms and define them.
    """
    prompt = (
        "Analyze the following text. Identify up to 5 difficult, academic, or jargon terms. "
        "For each word, provide a simple, context-aware definition. "
        "Format your response as a valid JSON list of dictionaries like:\n"
        '[{"word": "example", "definition": "simple explanation"}]\n\n'
        f"Text to analyze:\n{text}"
    )
    
    # Layout representation of Client call:
    # 
    # from openai import OpenAI
    # client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     response_format={"type": "json_object"},
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ],
    #     temperature=0.3
    # )
    # return json.loads(response.choices[0].message.content)
    
    return [
        {"word": "[Term 1]", "definition": "[AI Glossary Definition Simulation]"}
    ]


# ---------------------------------------------------------
# Part 3: Actionable Recommendation Engine
# ---------------------------------------------------------

def get_reading_recommendation(nlp_analysis, user_reading_level="High School"):
    """
    Evaluates the reading difficulty against the user's reading level 
    and outputs actionable recommendation directives.
    """
    levels = ["Elementary", "Middle School", "High School", "Academic"]
    
    try:
        text_level_idx = levels.index(nlp_analysis["level"])
        user_level_idx = levels.index(user_reading_level)
    except ValueError:
        # Fallback to defaults
        text_level_idx = 2
        user_level_idx = 2

    recommendations = []
    
    # Rule 1: Text is harder than the reader's level
    if text_level_idx > user_level_idx:
        recommendations.append("Read the simplified version first to grasp the core concepts.")
        recommendations.append("Review difficult glossary terms before attempting the full original text.")
    # Rule 2: Text matches reader's level but is generally challenging (High School or Academic)
    elif text_level_idx == user_level_idx and text_level_idx >= 2:
        recommendations.append("Review the glossary list for advanced technical terms.")
        recommendations.append("Take regular pauses; the sentence structures are moderately complex.")
    # Rule 3: Text is easier than reader's level
    else:
        recommendations.append("Directly read the original excerpt; vocabulary is standard for your level.")
        
    return {
        "text_difficulty": nlp_analysis["level"],
        "user_level": user_reading_level,
        "recommendations": recommendations
    }

# ---------------------------------------------------------
# Demonstration Execution
# ---------------------------------------------------------

if __name__ == "__main__":
    test_text = (
        "Quantum entanglement is a strange phenomenon where two particles become deeply connected. "
        "No matter how far apart they are—even across the universe—measuring the state of one "
        "instantly determines the state of the other, defying classical physics."
    )
    
    print("--- 1. NLP Analysis (Rule-Based) ---")
    keywords = extract_keywords(test_text)
    difficulty = estimate_reading_difficulty(test_text)
    print(f"Keywords Extracted: {keywords}")
    print(f"Estimated Difficulty: {difficulty['level']} (Score: {difficulty['score']})")
    print(f"Details: {difficulty['desc']}")
    
    print("\n--- 2. Actionable Recommendations (User Level: Middle School) ---")
    recs = get_reading_recommendation(difficulty, user_reading_level="Middle School")
    for idx, rec in enumerate(recs["recommendations"], 1):
        print(f"[{idx}] {rec}")
