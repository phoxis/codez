#include "sort_routines.h"
#include "sort_utils.h"

void bubble_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  int i, j;

  for (i=0; i < (int) nmemb; i++)
  {
    for (j=0; j < (int) nmemb - i - 1; j++)
    {
      if (compar ((char *) base + (j + 1) * size, (char *) base + j * size) < 0)
      {
        block_swap ((char *) base + j * size, (char *) base + (j + 1) * size, size);
      }
    }
  }

  return;
}
