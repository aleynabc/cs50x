#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    //Prompt user for height between 1 and 8
    do
    {

        height = get_int("Height (1-8) : ");

    }
    while (height <1 || height > 8);

    //Draw double pyramid

    for (int i = 0; i< height;i++)
    {
        // Print Left
        for (int j = 0; j <height - i - 1; j++)
        {
            printf(" ");
        }

        printf(" ");

        for ( int k = 0; k <=i ; k++)
        {
            printf("#");
        }

        printf(" ");

        for (int k=0; k <=i; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}
