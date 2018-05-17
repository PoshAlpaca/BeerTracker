# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

A lung disease caused by inhaling very fine ash and sand dust.

## According to its man page, what does `getrusage` do?

It returns the resource usage statistics.
In our case for the calling process, which means the sum of resources used by all threads in the process.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because it's faster and more memory efficient

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

Using fgetc(), the for-loop iterates character by character through the file.
If the current character is alphabetical or an apostrophe (that occurs somewhere in the word, not at the beginning), it gets appended to the `word` string.
If the current character is instead a digit, the word gets quickly iterated over, in order to skip it.
If the current character passes neither of the two above conditions, it must be the end of the word, so the character `\0` gets appended and the word gets spellchecked.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Using `fgetc` makes sure that no matter the form of the input file, it will always be interpreted correctly.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So that it is not possible for me to modify the strings in my program.
