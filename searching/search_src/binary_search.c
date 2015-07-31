#include "search_routines.h"

void *binary_search (const void *key, const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  void *retptr = NULL;
  int mid, high, lo;
  
  lo = 0;
  high = nmemb - 1;
  
  while (lo <= high)
  {
    mid = (high + lo) / 2;
    if (compar (key, base + mid * size) == 0)
    {
      retptr = (void *) base + mid * size;
      break;
    }
    else if (compar (key, base + mid * size) < 0)
    {
      high = mid - 1;
    }
    else
    {
      lo = mid + 1;
    }
  }
  
  return retptr;
}
