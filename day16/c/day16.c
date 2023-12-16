#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "util.h"

enum DIRECTION {
    LEFT = 0x01,
    RIGHT = 0x02,
    UP = 0x04,
    DOWN = 0x08,
    UNKNOWN = 0x80
};

typedef struct beam_def {
    int16_t row;
    int16_t col;
    enum DIRECTION beam_direction;
    int16_t is_set;
} beam_def;

void set_beam_def(beam_def* beam_def, int16_t row, int16_t col, enum DIRECTION beam_direction){
    beam_def->row = row;
    beam_def->col = col;
    beam_def->beam_direction = beam_direction;
    beam_def->is_set = 1;
}

int16_t get_new_row(int16_t row, enum DIRECTION direction){
    int16_t new_row;
    if(direction == LEFT){
        new_row = row;
    }
    else if(direction == RIGHT){
        new_row = row;
    }
    else if(direction == UP){
        new_row = row - 1;
    }
    else if(direction == DOWN){
        new_row = row + 1;
    }

    return new_row;
}

int16_t get_new_col(int16_t col, enum DIRECTION direction){
    int16_t new_col;
    if(direction == LEFT){
        new_col = col - 1;
    }
    else if(direction == RIGHT){
        new_col = col + 1;
    }
    else if(direction == UP){
        new_col = col;
    }
    else if(direction == DOWN){
        new_col = col;
    }

    return new_col;
}

enum DIRECTION get_reflected_direction(char mirror, enum DIRECTION incoming_direction){
    if( mirror == '\\'){
        switch (incoming_direction) {
            case LEFT:
                return UP;
            case RIGHT:
                return DOWN;
            case UP:
                return LEFT;
            case DOWN:
                return RIGHT;
            default:
                return UNKNOWN;
        }
    }
    else if( mirror == '/'){
        switch (incoming_direction) {
            case LEFT:
                return DOWN;
            case RIGHT:
                return UP;
            case UP:
                return RIGHT;
            case DOWN:
                return LEFT;
            default:
                return UNKNOWN;
        }
    }
}

void pretty_print_transition_map(grid* transition_map){
    for(int i = 0; i< transition_map->row_count; i++){
        for(int j = 0; j < transition_map->col_count; j++){
            if(get_grid_value(transition_map, i, j) == 0){
                printf(".");
            }
            else{
                printf("#");
            }
        }
        printf("\n");
    }
}

void solve_rec(
    grid* map_grid, 
    grid* seen_transition_map, 
    int16_t current_row, 
    int16_t current_col, 
    enum DIRECTION beam_direction){
    char transition_values_for_cell = get_grid_value(seen_transition_map, current_row, current_col);
    if ( (transition_values_for_cell & beam_direction) != 0){
        // logical and of these values will be > 0 if that bit is set
        // immediately return
        return;
    }
    // set the correct bit in that cell to indicate we have been through here in this direction
    
    set_grid_value(seen_transition_map, current_row, current_col, (transition_values_for_cell | beam_direction));

    // number of next beams to recursively process can only be 1 or 2.
    // initialize both to "NULL"
    beam_def next_one = { .is_set = 0 };
    beam_def next_two = { .is_set = 0 };

    char current_position_symbol = get_grid_value(map_grid, current_row, current_col);

    if(current_position_symbol == '.'){
        // pass straight through '.' without changing direction
        int16_t new_row = get_new_row(current_row, beam_direction);
        int16_t new_col = get_new_col(current_col, beam_direction);
        set_beam_def(&next_one, new_row, new_col, beam_direction);
    }
    else if(current_position_symbol == '/' || 
            current_position_symbol == '\\'){
        // for mirrors, calculate the new direction, then move 1 in that direction
        enum DIRECTION new_beam_direction = get_reflected_direction(current_position_symbol, beam_direction);
        int16_t new_row = get_new_row(current_row, new_beam_direction);
        int16_t new_col = get_new_col(current_col, new_beam_direction);
        set_beam_def(&next_one, new_row, new_col, new_beam_direction);
    }
    else if(current_position_symbol == '-'){
        if(beam_direction == LEFT || beam_direction == RIGHT){
            // straight through
            int16_t new_row = get_new_row(current_row, beam_direction);
            int16_t new_col = get_new_col(current_col, beam_direction);
            set_beam_def(&next_one, new_row, new_col, beam_direction);
        }
        else{
            //split. send one left and send one right
            int16_t new_row_l = get_new_row(current_row, LEFT);
            int16_t new_col_l = get_new_col(current_col, LEFT);
            set_beam_def(&next_one, new_row_l, new_col_l, LEFT);

            int16_t new_row_r = get_new_row(current_row, RIGHT);
            int16_t new_col_r = get_new_col(current_col, RIGHT);
            set_beam_def(&next_two, new_row_r, new_col_r, RIGHT);
        }
    }
    else if(current_position_symbol == '|'){
        if(beam_direction == UP || beam_direction == DOWN){
            // straight through
            int16_t new_row = get_new_row(current_row, beam_direction);
            int16_t new_col = get_new_col(current_col, beam_direction);
            set_beam_def(&next_one, new_row, new_col, beam_direction);
        }
        else{
            //split. send one up and send one down
            int16_t new_row_u = get_new_row(current_row, UP);
            int16_t new_col_u = get_new_col(current_col, UP);
            set_beam_def(&next_one, new_row_u, new_col_u, UP);

            int16_t new_row_d = get_new_row(current_row, DOWN);
            int16_t new_col_d = get_new_col(current_col, DOWN);
            set_beam_def(&next_two, new_row_d, new_col_d, DOWN);
        }
    }

    // for each beam that is set
    // check it is in bounds
    // if it is, call this func again with the new values
    if(next_one.is_set == 1){
        if(
            next_one.row >= 0 && 
            next_one.row < map_grid->row_count && 
            next_one.col >= 0 && 
            next_one.col < map_grid->col_count){
            // is in-bounds.
            solve_rec(map_grid, seen_transition_map, next_one.row, next_one.col, next_one.beam_direction);
        }
    }

    if(next_two.is_set == 1){
        if(
            next_two.row >= 0 && 
            next_two.row < map_grid->row_count && 
            next_two.col >= 0 && 
            next_two.col < map_grid->col_count){
            // is in-bounds
            solve_rec(map_grid, seen_transition_map, next_two.row, next_two.col, next_two.beam_direction);
        }
    }
}

int main(int argc, char** argv){
    char* input_file;
    if (argc == 2) {
        input_file = argv[1];
    } else {
        input_file = "../input_short.txt";
    }

    FILE* fp = fopen(input_file, "r");
    int16_t row_count = get_file_row_count(fp);
    int16_t col_count = get_file_col_count(fp);
    grid* map_grid = read_input_grid(fp, row_count, col_count);
    fclose(fp);

    printf("grid rows -> %d\n", map_grid->row_count);
    printf("grid cols -> %d\n", map_grid->col_count);
    pretty_print_grid(map_grid);
    printf("=============== START =================\n");

    grid* seen_transition_map = create_grid(row_count, col_count);

    solve_rec(map_grid, seen_transition_map, 0, 0, RIGHT);

    int count = 0;
    for(int i = 0; i < (row_count * col_count); i++){
        if(seen_transition_map->grid_data[i] != 0){
            count++;
        }
    }

    printf("Count: %d\n", count);
    return 0;
}