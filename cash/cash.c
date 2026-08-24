#include <cs50.h>
#include <stdio.h>

// Calculate number of coins of a given denomination
int calculate_coins(int cents, int coin_value);

int main(void)
{
    int cents;
    //Prompt user until a non-negative value is provided
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents<0);

    int total_coins = 0;

    // Calculate quarters
    int quarters =calculate_coins(cents,25);
    cents -= quarters * 25;
    total_coins += quarters;

    // Calculate dimes
    int dimes = calculate_coins(cents, 10);
    cents -= dimes * 10;
    total_coins += dimes;

    // Calculate nickels
    int nickels = calculate_coins(cents,5);
    cents -=nickels *5;
    total_coins += nickels;

    // Calculate pennies
    int pennies = calculate_coins (cents, 1);
    cents -= pennies;
    total_coins += pennies;

    // Print total number of coins
    printf("%d\n",total_coins);

}
int calculate_coins(int cents, int coin_value)
{
    return cents / coin_value;
}
