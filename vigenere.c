#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    //Check if correct number of arguments.
    if (argc != 2)
    {
        printf("Error: Wrong number of arguments.\n");
        return 1;
    }

    string keyword = argv[1];

    //Check if argument contains non-alphabetical character.
    for (int i = 0; i < strlen(keyword); i++)
    {
        keyword[i] = toupper(keyword[i]);
        if (keyword[i] < 'A' || keyword[i] > 'Z')
        {
            printf("Error: Keyword contains non-alphabetical character.\n");
            return 1;
        }
    }

    string text = get_string("plaintext: ");
    int j = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] = (keyword[j] - 'A' + text[i] - 'A') % 26 + 'A';
            j++;
        }

        else if (text[i] >= 'a' && text[i] <= 'z')
        {
            text[i] = (keyword[j] - 'A' + text[i] - 'a') % 26 + 'a';
            j++;
        }
        j %= strlen(keyword);
    }
    printf("ciphertext: %s\n", text);
}