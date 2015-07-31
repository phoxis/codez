#include <stdio.h>
#include <stdlib.h>

#include "test_utils.h"
#include "sort_utils.h"
#include "sort_routines.h"

static int compare (const void *p1, const void *p2)
{
  return *((int *) p1) - *((int *) p2);
}

struct sort_fun_holder {
  char *name;
  void (*sort_routine) (void *, size_t, size_t, int (*compar)(const void *, const void *));
};

static struct sort_fun_holder sort_obj[] = { 
                                        {"Bubble Sort"   , bubble_sort}, 
                                        {"Selection Sort", selection_sort},
                                        {"Insertion Sort", insertion_sort},
                                        {"Merge Sort"    , merge_sort},
                                        {"Quick Sort"    , quick_sort},
                                        {"Heap Sort"     , heap_sort},
                                        {""              , NULL},
                                    };


int basic_test1 (int n)
{
  int *arr, *backup_array, retval, i, total_result_flag = 1;

  scanf (" %d", &n);
  arr = malloc (sizeof (int) * n);
  backup_array = allocate_random_array (n);

  int a = 1, b = 2;
  
  printf ("a = %d, b = %d\ncompar (a, b) = %d\ncompar (b, a) = %d\ncompar (a, a) = %d\ncompare (b, b) = %d\n", a, b, compare (&a, &b), compare (&b, &a), compare (&a, &a), compare (&b, &b));
  
  for (i=0; sort_obj[i].sort_routine != NULL; i++)
  {
    copy_array (backup_array, arr, n, sizeof (int));
    sort_obj[i].sort_routine (arr, n, sizeof (int), compare);
    retval = check_sequence (arr, n);
    printf ("%s: ", sort_obj[i].name);
    retval == 1 ? printf ("[SUCCESS]\n") : printf ("[FAIL]\n");
    total_result_flag &= retval;
    //   output_array (arr, n); printf ("\n");
  }
  
  return total_result_flag;
}

 
int main (void)
{
  int elem;
  scanf (" %d", &elem);
  basic_test1 (elem);
  
  return 0;
}
