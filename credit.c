#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Prompt for input.
    long long number, number_copy;
    do
    {
        number = number_copy = get_long_long("Number: ");
    }
    while (number < 0);

    int sum = 0;
    while (number != 0)                     //Luhn algorithm.
    {
        sum += number % 10;                 //Add right-most digit of number to sum.
        number /= 10;                       //Cut right-most digit of number.
        int snippet = (number % 10) * 2;    //Multiply right-most digit of number by 2 and save result in snippet.

        while (snippet != 0)                //Add each individual digit of snippet to sum.
        {
            sum += snippet % 10;            //Add right-most digit of snippet to sum.
            snippet /= 10;                  //Cut right-most digit of snippet.
        }
        number /= 10;                       //Cut right-most digit of number.
    }

    if (sum % 10 == 0)                      //If the number passes the Luhn-check then check for card-type.
    {
        while (true)
        {
            //Check for VISA prefix.
            if (number_copy == 4)
            {
                printf("VISA\n");
                break;
            }

            //Check for AMEX prefix.
            else if (number_copy == 34 || number_copy == 37)
            {
                printf("AMEX\n");
                break;
            }

            //Check for MASTERCARD prefix.
            else if ((number_copy >= 51 && number_copy <= 55) || (number_copy >= 2221 && number_copy <= 2720))
            {
                printf("MASTERCARD\n");
                break;
            }

            //If after n iterations none of the prefixes matched, break.
            else if (number_copy == 0)
            {
                printf("INVALID\n");
                break;
            }

            //Cut right-most digit and then loop around.
            number_copy /= 10;
        }
    }

    else
    {
        printf("INVALID\n");
    }
}