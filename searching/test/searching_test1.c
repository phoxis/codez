#include <stdio.h>
#include <stdlib.h>

#include "search_routines.h"

struct search_fun_holder {
  char *name;
  void * (*search_routine) (const void *, const void *, size_t, size_t, int (*compar)(const void *, const void *));
};

static struct search_fun_holder search_obj[] = {
                                             {"Binary Search",   binary_search},
                                             {""             ,   NULL},
                                            };

static int compare (const void *p1, const void *p2)
{
  return *((int *) p1) - *((int *) p2);
}

int *allocate_searial_array (int n)
{
  int *arr, i;
  arr = malloc (sizeof (int) * n);
  
  for (i=0; i<n; i++)
  {
    arr[i] = i * 5;
  }
  
  return arr;
}

int basic_test1 (int n)
{
  int *arr, i, fun, key, success = 1, total_success = 1;
  void *obj;
  
  arr = allocate_searial_array (n);
  printf ("Array base: %p\n", arr);
  for (fun = 0; search_obj[fun].search_routine != NULL; fun++)
  {
    printf ("dd\n");fflush (stdout);
    printf ("%s: ", search_obj[fun].name);
    success = 1;
    
    for (i=0; i<n; i++)
    {
      key = i * 5;
      obj = search_obj[fun].search_routine (&key, arr, n, sizeof (int), compare);
      if (obj == NULL)
      {
        printf ("key = %d Not found\n", key);
        success = 0;
      }
      else
      {
        printf ("key = %d Found at location %d with value %d\n", key, (int) ((int *) obj - arr), *((int *)obj));
      }
    }
    
    for (i=0; i<n; i++)
    {
      key = i * 5  + 1;
      obj = search_obj[fun].search_routine (&key, arr, n, sizeof (int), compare);
      if (obj == NULL)
      {
        printf ("key = %d Not found\n", key);
      }
      else
      {
        printf ("key = %d Found at location %d with value %d\n", key, (int) ((int *) obj - arr), *((int *)obj));
        success = 0;
      }
    }
    
    if (success == 1)
    {
      printf ("[SUCCESS]\n");
    }
    else
    {
      total_success = 0;
    }
  }
  
  free (arr);
  
  return total_success;
}

int main (void)
{
  int elem;
  
  scanf (" %d", &elem);
  
  basic_test1 (elem);
  
  return 0;
}

