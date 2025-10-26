#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "utils.h"

#define GRID_ROWS      4
#define GRID_COLS      4
#define GRID_SYMBOL   'a'

#define TARGET_ROW     2
#define TARGET_COL     2
#define TARGET_SYMBOL 'X'

void create_map(char *map, int num_rows, int num_cols, char init_value);

void print_map(char *map, int num_rows, int num_cols);

int main() {
	printf("--- Grid Navigation ---\n");
	
	// Vars
	char maze_grid[GRID_ROWS][GRID_COLS];
		
	// Create map
	create_map(&maze_grid[0][0], GRID_ROWS, GRID_COLS, GRID_SYMBOL);
	
	printf("Size of maze_grid rows: %lu\n", sizeof(maze_grid)    / sizeof(maze_grid[0])   );
	printf("Size of maze_grid cols: %lu\n", sizeof(maze_grid[0]) / sizeof(maze_grid[0][0]));
	
	// Place target
	maze_grid[TARGET_ROW][TARGET_COL] = TARGET_SYMBOL;

	// Episode loop
	int num_cycles 	    = 10;
	int current_pos[2]  = {TARGET_ROW, TARGET_COL};
	while (num_cycles > 0) {
		// New position
		int temp_pos[2] = {
			rand_range(0, GRID_ROWS-1),
			rand_range(0, GRID_COLS-1)
		};

		// Place new target
		maze_grid[current_pos[0]][current_pos[1]] = GRID_SYMBOL;
		maze_grid[temp_pos[0]][temp_pos[1]]		  = TARGET_SYMBOL;

		current_pos[0]  = temp_pos[0];
		current_pos[1]  = temp_pos[1];

		// Print map
		print_map(&maze_grid[0][0], GRID_ROWS, GRID_COLS);

		// Delay for debug purposes
		delay(1000);

		// Decrement
		num_cycles--;
	}
	
	return 0;
}

void create_map(char *map, int num_rows, int num_cols, char init_value) {
	// Get total elements
	int num_elems = num_rows * num_cols;
	
	// Create loop
	for (int i=0; i<num_elems; i++) {
		*(map+i) = init_value;
	}
}

void print_map(char *map, int num_rows, int num_cols) {
	// Get total elements
	int num_elems = num_rows * num_cols;
	
	// Print loop
	for (int i=0; i<num_elems; i++) {
		if (i%num_cols == 0 && i!=0) {
			printf("\n");
		}
		
		printf("%c ", *(map+i));
	}
	
	//
	printf("\n\n");
	
}