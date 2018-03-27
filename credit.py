from cs50 import get_int


def main():
    while True:
        number = number_copy = get_int("Number: ")
        if number >= 0:
            break

    sum = 0
    while number != 0:                      # Luhn algorithm.
        sum += (number % 10)                # Add right-most digit of number to sum.
        number = int(number / 10)           # Cut right-most digit of number.
        snippet = (number % 10) * 2         # Multiply right-most digit of number by 2 and save result in snippet.

        while snippet != 0:                 # Add each individual digit of snippet to sum
            sum += snippet % 10             # Add right-most digit of snippet to sum.
            snippet = int(snippet / 10)     # Cut right-most digit of snippet.

        number = int(number / 10)           # Cut right-most digit of number.

    if sum % 10 == 0:                       # If the number passes the Luhn-check then check for card-type.
        while True:
            if number_copy == 4:
                print("VISA")
                break
            elif number_copy == 34 or number_copy == 37:
                print("AMEX")
                break
            elif (51 <= number_copy <= 55) or (2221 <= number_copy <= 2720):
                print("MASTERCARD")
                break
            elif number_copy == 0:
                print("INVALID")
                break

            number_copy = int(number_copy / 10)
    else:
        print("INVALID")


if __name__ == "__main__":
    main()