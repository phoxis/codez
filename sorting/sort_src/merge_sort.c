#include "sort_routines.h"
#include "sort_utils.h"

/* Merge function */
static void merge_fn (int *base, int st, int sp, int mid, size_t size, int (*compar)(const void *, const void *))
{
  int i, j, k;
  int *temp;

  temp = malloc (size * (sp - st + 1));
  i = st;
  j = mid + 1;
  k = 0;

  while ((i <= mid) && (j <= sp))
  {
    if (compar ((char *) base + i * size, (char *) base + j * size) < 0)
    {
      memcpy ((char *) temp + k * size, (char *) base + i * size, size);
      k++;
      i++;
    }
    else
    {
      memcpy ((char *) temp + k * size, (char *) base + j * size, size);
      k++;
      j++;
    }
  }

  while (i <= mid)
  {
    memcpy ((char *) temp + k * size, (char *) base + i * size, size);
    k++;
    i++;
  }

  while (j <= sp)
  {
    memcpy ((char *) temp + k * size, (char *) base + j * size, size);
    k++;
    j++;
  }

  for (k=0, i=st; i<=sp; i++, k++)
  {
    memcpy ((char *) base + i * size, (char *) temp + k * size, size);
  }

  free (temp);
}

/* Recursive merge sort function */
static void _merge_sort (void *base, int lo, int high, size_t size, int (*compar)(const void *, const void *))
{
  int mid;

  if (lo >= high)
  {
    return;
  }

  mid = (high + lo)/2;
  _merge_sort (base, lo, mid, size, compar);
  _merge_sort (base, mid + 1, high, size, compar);
  merge_fn (base, lo, high, mid, size, compar);

  return;
}

/* Merge sort function to call from outside */
void merge_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  _merge_sort (base, 0, nmemb - 1, size, compar);

  return;
}

