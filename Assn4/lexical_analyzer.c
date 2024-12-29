//It identifies keywords,identifiers,numbers,operators and punctuations

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define MAX_TOKEN_LENGTH 100

typedef enum {
    TOKEN_KEYWORD,
    TOKEN_IDENTIFIER,
    TOKEN_NUMBER,
    TOKEN_OPERATOR,
    TOKEN_PUNCTUATION,
    TOKEN_UNKNOWN
} TokenType;

typedef struct {
    TokenType type;
    char value[MAX_TOKEN_LENGTH];
} Token;

// List of keywords
const char *keywords[] = {
    "int", "float", "if", "else", "return"
};
const int num_keywords = sizeof(keywords) / sizeof(keywords[0]);

// Function prototypes
int is_keyword(const char *word);
Token get_next_token(FILE *file);
void print_token(Token token);

int main() {
    FILE *file = fopen("input.c", "r");
    if (!file) {
        perror("Failed to open file");
        return EXIT_FAILURE;
    }

    Token token;
    while ((token = get_next_token(file)).type != TOKEN_UNKNOWN) {
        print_token(token);
    }

    fclose(file);
    return 0;
}

// Check if the word is a keyword
int is_keyword(const char *word) {
    for (int i = 0; i < num_keywords; i++) {
        if (strcmp(word, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

// Get the next token from the input file
Token get_next_token(FILE *file) {
    Token token;
    token.type = TOKEN_UNKNOWN;
    token.value[0] = '\0';

    int c;
    while ((c = fgetc(file)) != EOF) {
        // Skip whitespace
        if (isspace(c)) {
            continue;
        }

        // Identifier or Keyword
        if (isalpha(c) || c == '_') {
            int index = 0;
            do {
                token.value[index++] = c;
                c = fgetc(file);
            } while (isalnum(c) || c == '_');
            token.value[index] = '\0';
            ungetc(c, file); // Push back the last character
            token.type = is_keyword(token.value) ? TOKEN_KEYWORD : TOKEN_IDENTIFIER;
            return token;
        }

        // Number
        if (isdigit(c)) {
            int index = 0;
            do {
                token.value[index++] = c;
                c = fgetc(file);
            } while (isdigit(c) || c == '.');
            token.value[index] = '\0';
            ungetc(c, file); // Push back the last character
            token.type = TOKEN_NUMBER;
            return token;
        }

        // Operator
        if (strchr("+-*/=<>", c)) {
            token.value[0] = c;
            token.value[1] = '\0';
            token.type = TOKEN_OPERATOR;
            return token;
        }

        // Punctuation
        if (strchr(";(),{}", c)) {
            token.value[0] = c;
            token.value[1] = '\0';
            token.type = TOKEN_PUNCTUATION;
            return token;
        }

        // Error for unknown characters
        token.value[0] = c;
        token.value[1] = '\0';
        token.type = TOKEN_UNKNOWN;
        return token;
    }

    token.type = TOKEN_UNKNOWN; // End of file
    return token;
}

// Print the token
void print_token(Token token) {
    const char *type_names[] = {
        "Keyword", "Identifier", "Number", "Operator", "Punctuation", "Unknown"
    };
    printf("Token Type: %s, Value: %s\n", type_names[token.type], token.value);
}
