#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Ask for a name, says hello and writes the name on the screen
    string name = get_string("What is your name? : ");
    printf("hello, %s\n", name);
}
