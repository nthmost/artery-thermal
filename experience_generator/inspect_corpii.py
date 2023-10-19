def corpus_insights(corpus):
    # Tokenize using spaces
    tokens = corpus.split()
    unique_tokens = set(tokens)
    
    # Count sentences
    sentence_count = corpus.count('.') + corpus.count('!') + corpus.count('?')
    
    print(f"Total tokens: {len(tokens)}")
    print(f"Unique tokens: {len(unique_tokens)}")
    print(f"Total sentences: {sentence_count}")
    print(f"Average tokens per sentence: {len(tokens) / sentence_count if sentence_count else 0}")
    print(f"Sample tokens: {list(unique_tokens)[:50]}")  # Print 50 sample unique tokens

print("Party DB Insights:")
corpus_insights(party_db)

print("\nTESCREAL DB Insights:")
corpus_insights(tescreal_db)

