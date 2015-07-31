#ifndef SEARCH_ROUTINES_H
#define SEARCH_ROUTINES_H

#include <stdlib.h>

void *binary_search (const void *key, const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));

#endif

