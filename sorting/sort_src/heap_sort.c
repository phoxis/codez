#include "sort_routines.h"
#include "sort_utils.h"


/** Heap sort functions **/
static void heapify (void *base, int *h_size, int i, size_t size, int (*compar)(const void *, const void *))
{
  int left, right, max_or_min;
  left  = 2 * i;
  right = 2 * i + 1;

  if ((left < *h_size) && (compar ((char *) base + left * size, (char *) base + i * size) > 0))
  {
    max_or_min = left;
  }
  else
  {
    max_or_min = i;
  }

  if ((right < *h_size) && (compar ((char *) base + max_or_min * size, (char *) base + right * size) < 0))
  {
    max_or_min = right;
  }

  if (max_or_min != i)
  {
    block_swap ((char *) base + i * size, (char *) base + max_or_min * size, size);
    heapify (base, h_size, max_or_min, size, compar);
  }
  return;
}

static void build_heap (void *base, int *h_size, size_t size, int (*compar)(const void *, const void *))
{
  int i;

  for (i=*h_size/2; i>=0; i--)
  {
    heapify (base, h_size, i, size, compar);
  }

  return;
}

void heap_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  int h_size = nmemb, i;
  
  build_heap (base, &h_size, size, compar);
  for (i=nmemb-1; i>=0; i--)
  {
    block_swap (base + 0 * size, base + i * size, size);
    h_size--;
    heapify (base, &h_size, 0, size, compar);
  }

  return;
}
