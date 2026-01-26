import random

def get_sentence_by_difficulty(level):
    sentences = {
        "Easy": [
            "Hello world",
            "I love coding",
            "The sun is shining",
            "Have a nice day"
        ],
        "Medium": [
            "The quick brown fox jumps over the lazy dog",
            "She sells seashells by the seashore",
            "Pronunciation is key to good communication",
            "Artificial intelligence is changing the world"
        ],
        "Hard": [
            "Peter Piper picked a peck of pickled peppers",
            "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "The sixth sick sheik's sixth sheep's sick",
            "Colonel and choir are pronounced very differently"
        ]
    }

    return random.choice(sentences[level])
