#ifndef SORT_UTILS_T
#define SORT_UTILS_T

#include <stdlib.h>
#include <string.h>

#define MAX_WIDTH 1024

void block_swap (void *a, void *b, size_t width);
void copy_array (void *src, void *dest, size_t nel, size_t width);
void fy_shuffle (void *base, size_t nel, size_t width);

#endif
