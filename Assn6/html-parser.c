#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TAG_LENGTH 100
#define MAX_ATTR_LENGTH 100


char *trimWhitespace(char *str) {
    char *end;

    
    while (isspace((unsigned char)*str)) str++;

    if (*str == 0)  
        return str;

    
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;

    
    *(end + 1) = 0;

    return str;
}

// Function to parse an HTML tag
void parseTag(char *tag) {
    char tagName[MAX_TAG_LENGTH] = {0};
    char attributeName[MAX_ATTR_LENGTH] = {0};
    char attributeValue[MAX_ATTR_LENGTH] = {0};
    
    int i = 0, j = 0;
    int inTagName = 1, inAttrName = 0, inAttrValue = 0;

    
    while (tag[i] != '\0') {
        if (tag[i] == ' ' && inTagName) {
            tagName[j] = '\0'; 
            inTagName = 0;
            inAttrName = 1;
            printf("Tag: Name: %s\n", trimWhitespace(tagName));
            j = 0;
        } else if (inTagName && tag[i] != ' ' && tag[i] != '/') {
            tagName[j++] = tag[i];
        } else if (inAttrName) {
            if (tag[i] == '=') {
                attributeName[j] = '\0';  
                inAttrName = 0;
                inAttrValue = 1;
                j = 0;
            } else if (tag[i] != ' ') {
                attributeName[j++] = tag[i];
            }
        } else if (inAttrValue) {
            if (tag[i] == '"') {
                if (j != 0) {
                    attributeValue[j] = '\0';  
                    printf("Attribute: %s = %s\n", trimWhitespace(attributeName), trimWhitespace(attributeValue));
                    j = 0;
                    inAttrValue = 0;
                    inAttrName = 1;  
                }
            } else {
                attributeValue[j++] = tag[i];
            }
        }
        i++;
    }

    
    if (inTagName) {
        tagName[j] = '\0';
        printf("Tag: Name: %s\n", trimWhitespace(tagName));
    }
}


void parseHTML(const char *html) {
    int i = 0;
    char tagBuffer[MAX_TAG_LENGTH];
    char textBuffer[MAX_TAG_LENGTH];
    int insideTag = 0;
    int bufferPos = 0;
    int textPos = 0;

    while (html[i] != '\0') {
        if (html[i] == '<') {
            
            if (textPos > 0) {
                textBuffer[textPos] = '\0'; 
                
                if (strlen(trimWhitespace(textBuffer)) > 0) {
                    printf("Text: %s\n", trimWhitespace(textBuffer));
                }
                textPos = 0; 
            }
            insideTag = 1;
            bufferPos = 0;
        } else if (html[i] == '>') {
            insideTag = 0;
            tagBuffer[bufferPos] = '\0';
            parseTag(tagBuffer);
        } else if (insideTag) {
            if (bufferPos < MAX_TAG_LENGTH - 1) {
                tagBuffer[bufferPos++] = html[i];
            }
        } else {
            
            if (textPos < MAX_TAG_LENGTH - 1) {
                textBuffer[textPos++] = html[i];
            }
        }
        i++;
    }

    
    if (textPos > 0) {
        textBuffer[textPos] = '\0'; 
        if (strlen(trimWhitespace(textBuffer)) > 0) {
            printf("\nText: %s", trimWhitespace(textBuffer));
        }
    }
}

int main() {
    char fileName[MAX_TAG_LENGTH];
    FILE *file;

    
    printf("Enter the HTML file name (must end with .html): ");
    fgets(fileName, sizeof(fileName), stdin);

    
    fileName[strcspn(fileName, "\n")] = 0;

    
    if (strlen(fileName) < 5 || strcmp(&fileName[strlen(fileName) - 5], ".html") != 0) {
        printf("Error: The file name must end with .html\n");
        return 1;
    }

    
    file = fopen(fileName, "r");
    if (file == NULL) {
        perror("Error: Unable to open the file");
        return 1;
    }

    
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);

    
    char *fileContent = malloc(fileSize + 1);
    if (fileContent == NULL) {
        perror("Error: Unable to allocate memory");
        fclose(file);
        return 1;
    }

    
    fread(fileContent, sizeof(char), fileSize, file);
    fclose(file);
    fileContent[fileSize] = '\0'; 

    
    parseHTML(fileContent);

    
    free(fileContent);
    return 0;
}
