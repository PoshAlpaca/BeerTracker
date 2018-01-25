#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Prompt user for height between (and including) 0 and 23.
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);


    //Print as many rows as the pyramid is high.
    for (int row = 0; row < height; row++)
    {
        //For example a height of 7 means that on row 3 (index: 2) there should be 4 (7-3) spaces and 3 (2+1) blocks.
        int needed_blocks = row + 1;
        int needed_spaces = height - needed_blocks;

        //Print spaces of first pyramid.
        for (int spaces = 0; spaces < needed_spaces; spaces++)
        {
            printf(" ");
        }

        //Print blocks of first pyramid.
        for (int blocks = 0; blocks < needed_blocks; blocks++)
        {
            printf("#");
        }

        //Print spaces between pyramids.
        printf("  ");

        //Print blocks of second pyramid. No spaces needed.
        for (int blocks = 0; blocks < needed_blocks; blocks++)
        {
            printf("#");
        }

        //Print line-breaks.
        printf("\n");
    }
}