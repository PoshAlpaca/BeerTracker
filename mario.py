from cs50 import get_int


def main():
    while True:
        height = get_int("Height: ")
        if height in range(0, 24):
            break

    for index in range(height):
        blocks = index + 1
        spaces = height - blocks
        print(" " * spaces, "#" * blocks, "  ", "#" * blocks, sep="")


if __name__ == "__main__":
    main()