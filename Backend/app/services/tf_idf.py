import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def __basic_tokenisation(text):
    sentences = re.split('[.!?]', text)
    return sentences

def __dynamic_max_df(sentences, base_threshold=0.85, min_threshold=0.5):
    num_sentences = len(sentences)

    if num_sentences <= 5:
        return 1.0  # Ignore common word filtering for very short texts
    elif num_sentences <= 10:
        return max(base_threshold, 0.95)  # Allow frequent words more
    else:
        return max(min_threshold, base_threshold - (num_sentences * 0.01))  # Reduce max_df dynamically

def __remove_redundant_keywords(keywords):
    """
    with TF-IDF and allowing bigrams, we get output like "money account" and "account" in the same result
    so we remove "account" and "money" from keywords
    """
    keywords = sorted(keywords, key=len, reverse=True)  # Sort by length (longest first)
    unique_keywords = []

    for keyword in keywords:
        if not any(keyword in longer_kw for longer_kw in unique_keywords):
            unique_keywords.append(keyword)

    return unique_keywords

def tf_idf_keywords(user_text):
    """
    used to find keywords in user text of the news. will return highlighted keywords.
    """
    # Tokenize into sentences
    sentences = __basic_tokenisation(user_text)  # split into words
    max_df = __dynamic_max_df(sentences)
    # Use TF-IDF to identify important sentences
    vectorizer = TfidfVectorizer(
        stop_words="english",
        token_pattern=r"(?u)\b[A-Za-z]{3,}\b",  # Ignores numbers and short words (<3 letters)
        ngram_range=(1, 2),  # Capture bigrams and trigrams
        max_df=max_df,  # Ignore very common words
        min_df=1,  # ignore words only appearing once
        max_features=50  # only keep top 50 words
    )

    tfidf_matrix = vectorizer.fit_transform(sentences)

    feature_names = vectorizer.get_feature_names_out()

    all_top_words = set()
    for i in range(len(sentences)):
        scores = tfidf_matrix[i].toarray()[0]
        top_indices = np.argsort(scores)[-5:][::-1]  # Get top 5 words
        all_top_words.update(feature_names[j] for j in top_indices)

    return __remove_redundant_keywords(list(all_top_words))
