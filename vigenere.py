from cs50 import get_string
import sys


def main():
    if len(sys.argv) != 2:
        print("Error: Wrong number of arguments.")
        sys.exit(1)
        return 1

    keyword = sys.argv[1].upper()

    if not keyword.isalpha():
        print("Error: Keyword contains non-alphabetical character.")
        sys.exit(1)
        return 1

    text = get_string("plaintext: ")
    ciphertext = ""
    j = 0

    for char in text:

        k_val = ord(keyword[j]) - ord("A")

        if char.isupper():
            char = (ord(char) - ord("A") + k_val) % 26 + ord("A")
            j += 1
        elif char.islower():
            char = (ord(char) - ord("a") + k_val) % 26 + ord("a")
            j += 1
        else:
            char = ord(char)

        ciphertext += chr(char)
        j %= len(keyword)

    print(u"ciphertext: {}".format(ciphertext))


if __name__ == "__main__":
    main()