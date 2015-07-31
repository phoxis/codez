#include "sort_routines.h"
#include "sort_utils.h"

void insertion_sort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *))
{
  int i, j;
  char *temp;
  
  temp = malloc (sizeof (char) * size);
  
  for (i = 1; i < (int) nmemb; i++)
  {
    j = i;
    memcpy (temp, (char *) base + j * size, size);
    while ((j > 0) && (compar ((char *) temp, (char *) base + (j - 1) * size) < 0))
    {
      memcpy ((char *) base + j * size, (char *) base + (j - 1) * size, size);
      j--;
    }
    memcpy ((char *) base + j * size, (char *) temp, size);
  }
  
  free (temp);
  
  return;
}
 
