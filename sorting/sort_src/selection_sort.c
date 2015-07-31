#include "sort_routines.h"
#include "sort_utils.h"

void selection_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  int i, j;

  for (i=0; i < (int) nmemb; i++)
  {
    for (j = i + 1; j < (int) nmemb; j++)
    {
      if (compar ((char *) base + j * size, (char *) base + i * size) < 0)
      {
        block_swap ((char *) base + i * size, (char *) base + j * size, size);
      }
    }
  }

  return;
}
