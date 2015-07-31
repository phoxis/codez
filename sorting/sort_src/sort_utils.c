#include "sort_utils.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
/** Utility functions **/

/* Block Swap */
void block_swap (void *a, void *b, size_t width)
{
  char temp[MAX_WIDTH];
  
  memcpy (temp, (char *) a, width);
  memcpy ((char *) a, (char *) b, width);
  memcpy ((char *) b, temp, width);
  
  return;
}


/* Copy array from source to destination */
void copy_array (void *src, void *dest, size_t nel, size_t width)
{
  memcpy (dest, src, nel * width);
  
  return;
}

/* Fisher-Yates unoiform random shuffle */

void fy_shuffle (void *base, size_t nel, size_t width)
{
  int r;
  char *temp;
 
  temp = malloc (sizeof (width));
  srand (time (NULL));
  while (nel)
  {
    r = rand () % nel;
    block_swap (base + r * width, base + (nel - 1) * width, width);
    nel--;
  }
 
  free (temp);
}

/** Utility functions end **/
 
