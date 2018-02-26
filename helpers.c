// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    string fraction_upper = strtok(fraction, "/");
    string fraction_lower = strtok(NULL, "/");

    int numerator = atoi(fraction_upper);
    int denominator = atoi(fraction_lower);

    while (denominator < 8)
    {
        numerator *= 2;
        denominator *= 2;
    }

    while (denominator > 8)
    {
        numerator /= 2;
        denominator /= 2;
    }

    return numerator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    double halftones = 0;
    int octave;

    switch (note[1])
    {
        case '#':
            halftones++;
            octave = note[2] - '0';
            break;

        case 'b':
            halftones--;
            octave = note[2] - '0';
            break;

        default:
            octave = note[1] - '0';
            break;
    }

    octave -= 4;
    halftones += octave * 12;

    switch (note[0])
    {
        case 'B':
            halftones += 2;
            break;

        case 'C':
            halftones -= 9;
            break;

        case 'D':
            halftones -= 7;
            break;

        case 'E':
            halftones -= 5;
            break;

        case 'F':
            halftones -= 4;
            break;

        case 'G':
            halftones -= 2;
            break;
    }

    return round(440 * pow(2, halftones / 12));
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strcmp(s, "") == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
