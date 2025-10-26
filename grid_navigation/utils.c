#include <stdio.h>
#include <time.h>

int rand_range(int min_value, int max_value) {
    return rand() % (max_value - min_value + 1) + min_value;
}

void delay(int number_of_seconds)
{
	// Converting time into milli_seconds
	int milli_seconds = 1000 * number_of_seconds;

	// Storing start time
	clock_t start_time = clock();

	// looping till required time is not achieved
	while (clock() < start_time + milli_seconds)
		;
}