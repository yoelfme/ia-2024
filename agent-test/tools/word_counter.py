from langchain.agents import tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    print('Using the word counter tool.')
    return len(word)
