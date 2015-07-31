#ifndef SORT_ROUTINES_H
#define SORT_ROUTINES_H

#include <stdlib.h>

void bubble_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
void selection_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
void insertion_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
void merge_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
void quick_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
void heap_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));

#endif