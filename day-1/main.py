corpus = [
    "I love programming in Python!",
    "Python is a great language for data science.",
    "I enjoy machine learning and natural language processing.",
]

sentence = "I love programming in Python!"


def normalize_doc(doc):
    words = doc.split()
    normalized_words = [word.lower().strip('.,!?:;"()') for word in words]
    return " ".join(normalized_words)


def normalize_corpus(corpus):
    return [normalize_doc(document) for document in corpus]


def build_bag_of_words(corpus, sort=False) -> dict[str, int]:
    bag_of_words = {}

    for document in corpus:
        words = document.split()
        for word in words:
            if word in bag_of_words:
                bag_of_words[word] += 1
            else:
                bag_of_words[word] = 1

    if sort:
        bag_of_words = dict(
            sorted(bag_of_words.items(), key=lambda x: x[1], reverse=True)
        )

    return bag_of_words


def build_vocabulary(corpus):
    vocabulary = set()
    for document in corpus:
        words = document.split()
        vocabulary.update(words)
    return sorted(vocabulary)


def text_to_vector(text, vocabulary):
    vector = [0] * len(vocabulary)
    word_to_index = {word: index for index, word in enumerate(vocabulary)}

    words = text.split()
    for word in words:
        if word in word_to_index:
            index = word_to_index[word]
            vector[index] += 1

    return vector


def main():
    normalized_corpus = normalize_corpus(corpus)
    print(f"Normalized Corpus: {normalized_corpus}")
    print("-----\n")

    vocabulary = build_vocabulary(normalized_corpus)
    print(f"Vocabulary: {vocabulary}")
    print("-----\n")

    bag_of_words = build_bag_of_words(normalized_corpus, sort=True)
    print(f"Bag of Words: {bag_of_words}")
    print("-----\n")

    normalized_sentence = normalize_doc(sentence)
    print(f"Normalized Sentence: '{normalized_sentence}'")
    print("-----\n")

    sentence_vector = text_to_vector(normalized_sentence, bag_of_words)
    print(f"Sentence Vector: {sentence_vector}")
    print("-----\n")


if __name__ == "__main__":
    main()
