import nltk

def ensure_nltk_resources():
    """Ensure required NLTK resources are available."""
    resources = [
        'stopwords',
        'punkt',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng'
    ]
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)

ensure_nltk_resources()