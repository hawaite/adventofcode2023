#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <math.h>
#include "grid_utils.h"

const int ROW_BUFFER_SIZE = 200;

int main(int argc, char** argv){
    int64_t row = 0;
    int64_t col = 0;
    char* input_file;

    if (argc == 2) {
        input_file = argv[1];
    } else {
        input_file = "../input.txt";
    }

    FILE* fp = fopen(input_file, "r");
    int16_t input_row_count = get_file_row_count(fp);

    char buf[ROW_BUFFER_SIZE];
    int64_t perimeter = 0;

    int64_t x_coords[input_row_count];
    int64_t y_coords[input_row_count];

    // init first coord
    x_coords[0] = col;
    y_coords[0] = row;

    for(int i=0; i < input_row_count; i++){
        fgets(buf, ROW_BUFFER_SIZE, fp);
        int hex_digits_start = 6;

        // if the original size value was two digits, push the start of hex digits out by one
        if(buf[3] != ' ')
            hex_digits_start ++; 

        // build a new string of first 5 hex digits with null terminator which strol will be happy with
        char hex_size_field[6];
        memcpy(hex_size_field, (buf+hex_digits_start), 5);
        hex_size_field[5] = '\0';
        long decimal_size = strtol(hex_size_field, NULL, 16);

        char direction = *(buf+hex_digits_start+5);

        if(direction == '0'){
            // right
            col += decimal_size;
        }
        else if(direction == '1'){
            // down
            row += decimal_size;
        }
        else if(direction == '2'){
            // left
            col -= decimal_size;
        }
        else if(direction == '3'){
            // up
            row -= decimal_size;
        }

        x_coords[i+1] = col;
        y_coords[i+1] = row;

        perimeter += decimal_size;
    }

    // shoelace formula
    int64_t left = 0;
    int64_t right = 0;
    for(int i = 0; i < input_row_count; i++){
        int64_t current_x = x_coords[i];
        int64_t current_y = y_coords[i];
        int64_t next_x = x_coords[i+1];
        int64_t next_y = y_coords[i+1];

        left += (current_x * next_y);
        right += (current_y * next_x);
    }

    // getting away with using an int type when dividing by two as area is always 
    // a whole number when drawing vertical and horizontal lines on a 2d grid
    int64_t area = llabs(left - right) * 0.5;

    // add perimeter in using Pick's theorem
    printf("area (with border) = %"PRId64"\n", (int64_t)(area + (perimeter*0.5) + 1));

    return 0;
}