#include "test_utils.h"
#include "sort_utils.h"

/* Allocate a uniformly random shuffled array */
int *allocate_random_array (int n)
{
  int *arr, i;

  arr = malloc (sizeof (int) * n);
  for (i=0; i<n; i++)
  {
    arr[i] = i;
  }

  fy_shuffle (arr, n, sizeof (int));

  return arr;
}


/* Check sorted ascending order */
int check_sort_order_up (int *arr, int n)
{
  int i;

  for (i=0; i<n-1; i++)
  {
    if (arr[i] > arr[i+1])
    {
      return 0;
    }
  }
  return 1;
}


int check_sequence_up (int *arr, int n)
{
  int i;
  
  for (i=0; i<n; i++)
  {
    if (arr[i] != i)
    {
      return 0;
    }
  }
  
  return 1;
}

int check_sequence_down (int *arr, int n)
{
  int i;
  
  for (i=0; i<n; i++)
  {
    if (arr[i] != n-i-1)
    {
      return 0;
    }
  }
  
  return 1;
}


/* Input array from stdin */
void input_array (int *arr, int n)
{
  int i;

  for (i=0; i<n; i++)
  {
    scanf (" %d", &arr[i]);
  }

  return;
}

/* Output array in stdout */
void output_array (int *arr, int n)
{
  int i;
  
  for (i=0; i<n; i++)
  {
    printf ("%d ", arr[i]);
  }
  
  return;
}

