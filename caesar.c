#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error: Wrong number of arguments.\n");
        return 1;
    }

    int key = atoi(argv[1]) % 26;
    string text = get_string("plaintext: ");

    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            text[i] = ((((text[i] - 'A') + key) % 26) + 'A');
        }
        else if (islower(text[i]))
        {
            text[i] = ((((text[i] - 'a') + key) % 26) + 'a');
        }
    }

    printf("ciphertext: %s\n", text);
}