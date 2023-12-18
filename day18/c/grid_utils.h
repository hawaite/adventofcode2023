#include <stdint.h>
#include <stdio.h>

typedef struct grid{
    char* grid_data;
    int16_t row_count;
    int16_t col_count;
} grid;

void free_grid(grid* grid);
grid* create_grid(int16_t row_count, int16_t col_count);
void init_grid(grid* grid, char initialize_character);
int16_t get_file_row_count(FILE* fp);
int16_t get_file_col_count(FILE* fp);
grid* read_input_grid(FILE* fp, int16_t row_count, int16_t col_count);
void pretty_print_grid(grid* grid);
char get_grid_value(grid* grid, int16_t row, int16_t col);
void set_grid_value(grid* grid, int16_t row, int16_t col, char value);