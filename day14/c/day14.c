#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint8_t get_file_row_count(FILE* fp) {
    uint8_t row_count = 1;

    char c;
    while ((c = fgetc(fp)) != EOF) {
        if (c == '\n')
            row_count++;
    }

    fseek(fp, 0, 0);

    return row_count;
}

uint8_t get_file_col_count(FILE* fp) {
    uint8_t col_count = 0;

    while (fgetc(fp) != '\n') {
        col_count++;
    }
    
    fseek(fp, 0, 0);

    return col_count;
}

char** read_input_grid(FILE* fp, uint8_t row_count, uint8_t col_count) {
    char** grid = malloc(sizeof(char*) * row_count);

    for (int i = 0; i < row_count; i++) {
        grid[i] = malloc((sizeof(char) * col_count));
    }

    char c;
    uint8_t current_row = 0;
    uint8_t current_col = 0;

    while ((c = fgetc(fp)) != EOF) {
        if (c == '\n') {
            current_row++;
            current_col = 0;
        } else {
            grid[current_row][current_col] = c;
            current_col++;
        }
    }

    return grid;
}

void free_grid(char** grid, uint8_t row_count) {
    // free the rows
    for (int i = 0; i < row_count; i++) {
        free(grid[i]);
    }

    // then free the row container
    free(grid);
}

void bubble_sort_upwards(char** grid, uint8_t row_count, uint8_t col_count) {
    for (int current_col = 0; current_col < col_count; current_col++) {
        // keep performing rounds until we do a round where no changes were made
        int made_a_change = 1;
        while (made_a_change != 0) {
            made_a_change = 0;
            // row count -1 otherwise we try to compare off bottom of grid
            for (int current_row = 0; current_row < (row_count - 1);
                 current_row++) {
                if (grid[current_row][current_col] == '.' &&
                    grid[current_row + 1][current_col] == 'O') {
                    char temp = grid[current_row][current_col];
                    grid[current_row][current_col] =
                        grid[current_row + 1][current_col];
                    grid[current_row + 1][current_col] = temp;
                    made_a_change = 1;
                }
            }
        }
    }
}

void print_grid(char** grid, uint8_t row_count, uint8_t col_count) {
    for (int i = 0; i < row_count; i++) {
        printf("%.*s\n", col_count, grid[i]);
    }
}

int main(int argc, char** argv) {
    char* input_file;
    if (argc == 2) {
        input_file = argv[1];
    } else {
        input_file = "../input_short.txt";
    }

    // parse input
    FILE* fp = fopen(input_file, "r");
    uint8_t row_count = get_file_row_count(fp);
    uint8_t col_count = get_file_col_count(fp);

    char** grid = read_input_grid(fp, row_count, col_count);
    fclose(fp);

    // do solution

    bubble_sort_upwards(grid, row_count, col_count);

    int total_load = 0;

    for (int i = 0; i < row_count; i++) {
        int points_per_item_for_this_row = row_count - i;
        for (int j = 0; j < col_count; j++) {
            if (grid[i][j] == 'O') {
                total_load += points_per_item_for_this_row;
            }
        }
    }

    printf("Total Load: %d\n", total_load);

    // tidy up
    free_grid(grid, row_count);
}