# Questions

## What's `stdint.h`?

It's a header file that implements the definiton of integers with specific sizes.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The different integer types take up different amounts of space.
E.g. if you don't need to represent negative numbers you can use an unsigned integer type.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1 byte
DWORD = 4 bytes
LONG = 4 bytes
WORD = 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM

## What's the difference between `bfSize` and `biSize`?

bfSize is the size, in bytes, of the BMP file.
biSize is the size, in bytes, of the BITMAPINFOHEADER structure.

## What does it mean if `biHeight` is negative?

It means that the Bitmap is a top-down DIB and its origin is in the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If there is no file or it is unable to open the file.

## Why is the third argument to `fread` always `1` in our code?

Because we always only want to read the block once.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

It changes the position of your 'cursor' inside the file.

## What is `SEEK_CUR`?

It's an argument that changes the behavior of fseek so that it moves the cursor relative to its current position.
