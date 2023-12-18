#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "grid_utils.h"

grid* create_grid(int16_t row_count, int16_t col_count){
    grid* grid = malloc(sizeof(grid));
    grid->row_count = row_count;
    grid->col_count = col_count;
    grid->grid_data = (char*)calloc((row_count * col_count), sizeof(char));
    return grid;
}

void init_grid(grid* grid, char initialize_character){
    memset(grid->grid_data, initialize_character, (grid->row_count * grid->col_count) * (sizeof(char)));
}

void free_grid(grid* grid){
    free(grid->grid_data);
    free(grid);
}

int16_t get_file_row_count(FILE* fp) {
    int16_t row_count = 1;

    char c;
    while ((c = fgetc(fp)) != EOF) {
        if (c == '\n')
            row_count++;
    }

    fseek(fp, 0, 0);

    return row_count;
}

int16_t get_file_col_count(FILE* fp) {
    int16_t col_count = 0;

    while (fgetc(fp) != '\n') {
        col_count++;
    }

    fseek(fp, 0, 0);

    return col_count;
}

grid* read_input_grid(FILE* fp, int16_t row_count, int16_t col_count) {
    grid* grid = create_grid(row_count, col_count);

    char c;
    int16_t ix = 0;

    while ((c = fgetc(fp)) != EOF) {
        if (c != '\n') {
            grid->grid_data[ix] = c;
            ix++;
        }
    }

    return grid;
}

void pretty_print_grid(grid* grid) {
    for (int i = 0; i < grid->row_count; i++) {
        for (int j = 0; j< grid->col_count; j++){
            printf("%c", grid->grid_data[(i * grid->col_count) + j]);
        }
        printf("\n");
    }
}

char get_grid_value(grid* grid, int16_t row, int16_t col){
    return grid->grid_data[row * grid->col_count + col];
}

void set_grid_value(grid* grid, int16_t row, int16_t col, char value){
    grid->grid_data[row * grid->col_count + col] = value;
}