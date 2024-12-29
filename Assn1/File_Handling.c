#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main() {
    FILE *file;
    char filename[100];
    int lineCount = 0, wordCount = 0;
    char buffer[255];

    // Taking user input for the file name
    printf("Enter the name of the file: ");
    scanf("%s", filename);

    // Attempting to open the file in read mode
    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: File '%s' does not exist in the directory!\n", filename);
        return 1;
    }

    // Counting lines and words
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        lineCount++;  // Increment line count for each new line

        // Iterate through the buffer to count words
        int inWord = 0; // Flag to check if we are inside a word
        for (int i = 0; buffer[i] != '\0'; i++) {
            if (isspace(buffer[i])) {
                inWord = 0; // End of a word
            } else if (inWord == 0) {
                inWord = 1; // Beginning of a new word
                wordCount++;
            }
        }
    }

    fclose(file);

    // Printing line and word count
    printf("Line count: %d\n", lineCount);
    printf("Word count: %d\n", wordCount);

    return 0;
}
