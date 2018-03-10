#include <stdio.h>
#include <stdint.h>

#define BLOCK 512

int main(int argc, char *argv[])
{
    // throw error if wrong number of arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover forensic_image\n");
        return 1;
    }

    FILE *fileptr = fopen(argv[1], "r");

    // throw error if file could not be opened for reading
    if (fileptr == NULL)
    {
        fprintf(stderr, "Image could not be opened for reading.\n");
        return 2;
    }

    int filecounter = 0;

    uint8_t buffer[BLOCK];
    char filename[sizeof("###.jpg")];

    FILE *image = NULL;

    while(fread(buffer, BLOCK, 1, fileptr))
    {
        // look for the beginning of a new file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            // if we already had a JPEG then we close it
            if (image != NULL)
                fclose(image);

            // open new image
            sprintf(filename, "%03d.jpg", filecounter);
            image = fopen(filename, "w");

            filecounter++;
        }

        // if we already have a JPEG then we add to it
        if (image != NULL)
            fwrite(buffer, BLOCK, 1, image);
    }

    fclose(fileptr);
    if (image != NULL)
        fclose(image);
}