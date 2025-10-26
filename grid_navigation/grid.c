#include <stdlib.h>
#include <stdio.h>

#define GRID_ROWS 4
#define GRID_COLS 4

void create_map(char *map, int num_rows, int num_cols, char init_value);

void print_map(char *map, int num_rows, int num_cols);

int main() {
	printf("--- Grid Navigation ---\n");
	
	// Vars
	char maze_grid[GRID_ROWS][GRID_COLS];
	char initial_val = 'a';
		
	// Create and print map
	create_map(&maze_grid[0][0], GRID_ROWS, GRID_COLS, initial_val);
	
	printf("Size of maze_grid rows: %lu\n", sizeof(maze_grid)    / sizeof(maze_grid[0])   );
	printf("Size of maze_grid cols: %lu\n", sizeof(maze_grid[0]) / sizeof(maze_grid[0][0]));
	
	print_map(&maze_grid[0][0], GRID_ROWS, GRID_COLS);
	
	
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
	printf("\n");
	
}