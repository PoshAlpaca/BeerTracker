// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

void trash(node *crawl);
void count(node *crawl);

int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *crawl = root;

    for (int i = 0, c = word[i], index; c != '\0'; c = word[i])
    {
        // Make character lowercase
        c = tolower(c);

        // Transform character into a number from 0-26
        if (c == '\'')
        {
            index = 26;
        }
        else
        {
            index = c - 'a';
        }


        // If the node at "index" does not exist that means the word does not exist
        if (crawl -> children[index] == NULL)
        {
            return false;
        }

        // If the node exists we go to that node
        else
        {
            crawl = crawl -> children[index];
        }

        i++;
    }

    if (crawl -> is_word == true)
    {
        return true;
    }

    else
    {
        return false;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file for reading
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }

    root = malloc(sizeof(node));
    if (root == NULL)
    {
        printf("Error: Out of memory");
        return 1;
    }

    // Initialize children array to NULL and is_word to false
    for (int i = 0; i < 27; i++)
    {
        root -> children[i] = NULL;
    }
    root -> is_word = false;


    // Set up crawl pointer which will keep track of where we are in our trie
    node *crawl = root;

    for (int c = fgetc(file), index; c != EOF; c = fgetc(file))
    {
        // If c is a line break, set is_word to true, go back to root and start new loop iteration
        if (c == '\n')
        {
            crawl -> is_word = true;
            crawl = root;
            continue;
        }

        // Transform character into a number from 0-26
        else if (c == '\'')
        {
            index = 26;
        }

        else
        {
            index = c - 'a';
        }

        // If the node doesn't exist yet, create it
        if (crawl -> children[index] == NULL)
        {
            node *n = malloc(sizeof(node));
            if (n == NULL)
            {
                printf("Error: Out of memory");
                return 1;
            }

            // Initialize children array to NULL and is_word to false
            for (int i = 0; i < 27; i++)
            {
                n -> children[i] = NULL;
            }
            n -> is_word = false;

            crawl -> children[index] = n;
            crawl = n;
        }
        // The node already exists, so we go to that node
        else
        {
            crawl = crawl -> children[index];
        }
    }

    // Check whether there was an error
    if (ferror(file))
    {
        fclose(file);
        printf("Error reading %s.\n", dictionary);
        return 1;
    }

    // Close text
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (!root)
    {
        return 0;
    }

    node *crawl = root;

    count(crawl);

    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *crawl = root;

    trash(crawl);

    return true;
}

void trash(node *crawl)
{
    for (int i = 0; i < 27; i++)
    {
        if (crawl -> children[i] == NULL)
        {
            continue;
        }

        else
        {
            trash(crawl -> children[i]);
        }
    }

    free(crawl);
}

void count(node *crawl)
{
    if (crawl -> is_word)
    {
        word_count++;
    }

    for (int i = 0; i < 27; i++)
    {
        if (crawl -> children[i] == NULL)
        {
            continue;
        }

        else
        {
            count(crawl -> children[i]);
        }
    }
}