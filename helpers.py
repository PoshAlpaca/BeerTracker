from nltk.tokenize import sent_tokenize


# Tokenize string into substrings of length n
def sub_tokenize(string, n):
    substrings = []

    for i, char in enumerate(string):

        # Prevent substrings towards the end of the string from being shorter than n
        if i + n <= len(string):
            substring = string[i:i + n]
            substrings.append(substring)

    return substrings


def lines(a, b):
    """Return lines in both a and b"""

    matches = []

    lines_a = a.splitlines()
    lines_b = b.splitlines()

    # Iterate through each line of a and each line of b and if there is a match that is not recorded yet, append to list
    for line_a in lines_a:
        for line_b in lines_b:
            if line_a == line_b and line_a not in matches:
                matches.append(line_a)

    return matches


def sentences(a, b):
    """Return sentences in both a and b"""

    matches = []

    sentences_a = sent_tokenize(a)
    sentences_b = sent_tokenize(b)

# Iterate through each sentence of a and each sentence of b and if there is a match that is not recorded yet, append to list
    for sentence_a in sentences_a:
        for sentence_b in sentences_b:
            if sentence_a == sentence_b and sentence_a not in matches:
                matches.append(sentence_a)

    return matches


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    matches = []

    substrings_a = sub_tokenize(a, n)
    substrings_b = sub_tokenize(b, n)

    # Iterate through each substring of a and each substring of b and if there is a match that is not recorded yet, append to list
    for substring_a in substrings_a:
        for substring_b in substrings_b:
            if substring_a == substring_b and substring_a not in matches:
                matches.append(substring_a)

    return matches