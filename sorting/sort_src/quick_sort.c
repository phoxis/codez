#include "sort_routines.h"
#include "sort_utils.h"

/* Primitive pivot function */
int pivot_method (void *base, int lo, int high)
{
  int piv;

  piv = base == base; // avoid warning
  piv = high == high; // avoid warning

  piv = lo;
  return piv;
}

/* Partition array */
static int partition_array (void *base, int lo, int high, size_t size, int (*compar)(const void *, const void *))
{
  int piv_index, i, j;
  char *piv_val;
  
  piv_val = malloc (sizeof (char) * size);
  
  piv_index = pivot_method (base, lo, high); /* TODO: Later we can use median as pivot, or other strategy */
  piv_val = memcpy (piv_val, (char *) base + piv_index * size, size);
  block_swap ((char *) base + lo * size, (char *) base + piv_index * size, size);

  i = lo;
  j = high;

  while (i <= j)
  {
    while ((i <= high) && (compar ((char *) base + i * size, piv_val) <= 0))
    {
      i++;
    }
    while (compar ((char *) base + j * size, piv_val) > 0)
    {
      j--;
    }
    if (i < j)
    {
      block_swap ((char *) base + i * size, (char *) base + j * size, size);
    }
  }

  block_swap ((char *) base + j * size, (char *) base + lo * size, size);
  
  free (piv_val);

  return j; 
}

/* Quick sort recursive function */
static void _quick_sort (void *base, int lo, int high, size_t size, int (*compar)(const void *, const void *))
{
  int piv_index;

  if (lo >= high)
  {
    return;
  }

  piv_index = partition_array (base, lo, high, size, compar);
  _quick_sort (base, lo, piv_index - 1, size, compar);
  _quick_sort (base, piv_index + 1, high, size, compar);

  return;  
}

/* Quick sort function to call from outside */
void quick_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  _quick_sort (base, 0, nmemb - 1, size, compar);

  return;
}
