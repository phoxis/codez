#ifndef TEST_UTILS_H
#define TEST_UTILS_H

#include <stdlib.h>
#include <stdio.h>

int *allocate_random_array (int n);
int check_sort_order_up (int *arr, int n);
void input_array (int *arr, int n);
void output_array (int *arr, int n);
 
#endif