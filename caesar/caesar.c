#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);

int main(int argc, string argv[])
{
    // 1. Argüman kontrolü
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // 2. Anahtarı sayıya çevir
    int key = atoi(argv[1]) % 26;

    // 3. Kullanıcıdan metni al
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    // 4. Şifreleme
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            printf("%c", (c - 'A' + key) % 26 + 'A');
        }
        else if (islower(c))
        {
            printf("%c", (c - 'a' + key) % 26 + 'a');
        }
        else
        {
            printf("%c", c);
        }
    }

    printf("\n");
    return 0;
}

// Argümanın tamamen sayı olup olmadığını kontrol eden fonksiyon
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}
