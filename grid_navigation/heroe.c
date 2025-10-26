#include <stdio.h>

#define POS_X 0
#define POS_Y 1

struct heroe {
    int curr_pos[2];
    
};

enum {
    UP,
    DOWN,
    RIGHT,
    LEFT
};

void heroe_reset(struct heroe *heroe, int pos_x, int pos_y) {
    // Reset pos
    heroe->curr_pos[POS_X] = pos_x;     // "->" already dereferences the pointer
    heroe->curr_pos[POS_Y] = pos_y;
}

void heroe_move(struct heroe *heroe, int direction) {
    // Get current position
    int pos_x = heroe->curr_pos[POS_X];
    int pos_y = heroe->curr_pos[POS_Y];

    // New position
    switch (direction)
    {
        case UP:
            pos_y--;
            break;
            
        case DOWN:
            pos_y++;
            break;

        case RIGHT:
            pos_x++;
            break;

        case LEFT:
            pos_x--;
            break;
    }

    // Reset position
    heroe_reset(&heroe, pos_x, pos_y);
}
