#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "grid_utils.h"

const int ROW_BUFFER_SIZE = 200;

void perform_flood_fill(grid* grid, int row, int col){
    if(get_grid_value(grid, row, col) != '#')
        set_grid_value(grid, row, col, '#');

    if(row != 0 && get_grid_value(grid, row-1, col) != '#')
        perform_flood_fill(grid, row-1, col);
    if(row != (grid->row_count - 1) && get_grid_value(grid, row+1, col) != '#') 
        perform_flood_fill(grid, row+1, col);
    if(col != 0 && get_grid_value(grid, row, col-1) != '#')
        perform_flood_fill(grid, row, col-1);
    if(col != (grid->col_count - 1) && get_grid_value(grid, row, col+1) != '#') 
        perform_flood_fill(grid, row, col+1);
    
}

void plot_steps(grid* grid, int* starting_row, int* starting_column, int count, char direction){
    if(direction == 'U'){
        for(int i=0; i<count; i++){
            set_grid_value(grid, (*starting_row) - i, (*starting_column), '#');
        }
        (*starting_row) -= count;
    }
    else if(direction == 'D'){
        for(int i=0; i<count; i++){
            set_grid_value(grid, (*starting_row) + i, (*starting_column), '#');
        }
        (*starting_row) += count;
    }
    else if(direction == 'L'){
        for(int i=0; i<count; i++){
            set_grid_value(grid, (*starting_row), (*starting_column) - i, '#');
        }
        (*starting_column) -= count;
    }
    else if(direction == 'R'){
        for(int i=0; i<count; i++){
            set_grid_value(grid, (*starting_row), (*starting_column) + i, '#');
        }
        (*starting_column) += count;
    }
}

int main(int argc, char** argv){
    int use_large_input = 0;

    int row;
    int col;
    int grid_size;
    int flood_fill_start_row;
    int flood_fill_start_col;
    char* input_file;

    if(use_large_input == 1){
        // values all manually verified
        row = 500;
        col = 500;
        grid_size = 1000;
        flood_fill_start_row = 600;
        flood_fill_start_col = 600;
        input_file = "../input.txt";
    }
    else{
        row = 0;
        col = 0;
        grid_size = 20;
        flood_fill_start_row = 1;
        flood_fill_start_col = 1;
        input_file = "../input_short.txt";
    }

    FILE* fp = fopen(input_file, "r");
    int16_t input_row_count = get_file_row_count(fp);

    grid* plotting_grid = create_grid(grid_size, grid_size);

    // fill grid with something that isnt \0 characters. Only actually important if pretty printing the grid.
    init_grid(plotting_grid, '.'); 


    char buf[ROW_BUFFER_SIZE];
    for(int i=0; i < input_row_count; i++){
        fgets(buf, ROW_BUFFER_SIZE, fp);

        char direction = buf[0];

        // the two bytes from index 2 onwards will either be 2 digits, or a digit and a space
        // atoi is hapy with parsing either of these
        char size_str[3];
        size_str[0] = buf[2];
        size_str[1] = buf[3];
        size_str[2] = '\0';
        int size = atoi(size_str);

        plot_steps(plotting_grid, &row, &col, size, direction);
    }

    perform_flood_fill(plotting_grid, flood_fill_start_row, flood_fill_start_col);

    int count = 0;

    for(int i = 0; i < plotting_grid->row_count; i++){
        for(int j=0; j < plotting_grid->col_count; j++){
            if(get_grid_value(plotting_grid, i,j) == '#')
                count++;
        }
    }

    printf("final count = %d\n", count);

    return 0;
}