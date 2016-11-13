#include "trie.hpp"
#include "wchar_to_int_mapper.hpp"
#include <locale>

unsigned int total_alloc = 0;
unsigned int total_free = 0;
int max_edges = 0;
int node_size = 0;

static void __trie_show (trie_t *root, int depth, wchar_t *prefix, int max_depth);

trie_t *trie_init (wchar_t *lang_map)
{
  init_wchar_mapper (lang_map);
  max_edges = max_keys;
  node_size = sizeof (trie_t) + (max_edges * sizeof (trie_t *));
  
  return trie_alloc_node ();
}

trie_t *trie_alloc_node (void)
{
  trie_t *node;
  int i;

  node = new trie_t;
  node->edge = new trie_t*[max_edges];
  for (i=0; i<max_edges; i++)
  {
    node->edge[i] = NULL;
  }
  node->mark = 0;

  total_alloc++;

  return node;
}

void trie_free_node (trie_t *node)
{
  if (node == NULL)
  {
    return;
  }
  delete [] node->edge;
  delete node;
  total_free++;
}

int toindex (wchar_t x)
{
  return wchar_map_to_int (x);
}

int validate_string (wchar_t *str)
{
  int i;
  for (i=0; str[i] != L'\0'; i++)
  {
    if (wchar_map_to_int (str[i]) == -1)
    {
      return 0;
    }
  }
  return 1;
}

int trie_add_word (trie_t *root, wchar_t *str)
{
  trie_t *cur = root;
  int i;

  if (!validate_string (str))
  {
    return 0;
  }

  for (i=0; str[i] != '\0'; i++)
  {
    if (cur->edge[toindex(str[i])] == NULL)
    {
      cur->edge[toindex(str[i])] = trie_alloc_node ();
    }
    cur = cur->edge[toindex(str[i])];
  }
  cur->mark = 1;
  return 1;
}

int trie_search (trie_t *root, wchar_t *str)
{
  trie_t *cur = root;
  int i;
  
  if (!validate_string (str))
  {
    return 0;
  }

  for (i=0; str[i] != L'\0'; i++)
  {
    if (cur->edge[toindex(str[i])] ==  NULL)
    {
      return 0;
    }
    cur = cur->edge[toindex(str[i])];
  }
  if (cur->mark == 1)
  {
    return 1;
  }

  return 0;
}

static void __trie_show (trie_t *root, int depth, wchar_t *prefix, int max_depth)
{
  static wchar_t postfix[STR_MAX];
  int i;
  
  if (   ((max_depth != -1) && (depth >= max_depth))
      || (root == NULL))
  {
    return;
  }
  
  if (root->mark == 1)
  {
    postfix[depth] = L'\0';
    fwprintf (stdout, L"[%ls%ls]\n", prefix, postfix);
  }
  
  for (i=0; i<max_edges; i++)
  {
    if (root->edge[i]  != NULL)
    {
      postfix[depth] = int_map_to_wchar (i);
      __trie_show (root->edge[i], depth + 1, prefix, max_depth);
    }
  }
  
}

void trie_show (trie_t *root, wchar_t *prefix, int max_depth)
{
  __trie_show (root, 0, prefix, max_depth);
}


int trie_search_autocomplete (trie_t *root, wchar_t *str, int max_depth)
{
  trie_t *cur = root;
  int i;
  wchar_t compiled_string[STR_MAX];
  int char_index = 0;
  int retval = 0;
  
  if (!validate_string (str))
  {
    return 0;
  }

  for (i=0; str[i] != L'\0'; i++)
  {
    if (cur->edge[toindex(str[i])] ==  NULL)
    {
      return 0;
    }
    compiled_string[char_index++] = str[i];
    cur = cur->edge[toindex(str[i])];
  }
  if (cur->mark == 1)
  {
    retval = 1;
  }
  
  compiled_string[char_index] = L'\0';
  fwprintf (stdout, L"Auto-complete List: for partial match: \"%ls\"\n", compiled_string);
  trie_show (cur, compiled_string, max_depth);
  
  return retval;
}

int trie_load_word_list (trie_t *root, char *file)
{
  FILE *fp = fopen (file, "r");
  wchar_t str[STR_MAX];
  int count = 0;

  setlocale (LC_ALL, "");
  
  if (fp == NULL)
  {
    return 0;
  }
  while (fwscanf (fp, L" %ls", str) != EOF)
  {
    if (validate_string (str))
    {
      trie_add_word (root, str);
      count++;
    }
  }
  fwprintf (stdout, L"%d words loaded\n", count);

  if (TRIE_VERIFY == 1)
  {
    count = 0;
    rewind (fp);
    while (fwscanf (fp, L" %ls", str) != EOF)
    {
      if (validate_string (str))
      {
        if (trie_search (root, str))
        {
          count++;
        }
      }
    }
    fwprintf (stdout, L"%d words verified\n", count);
  }
  
  fclose (fp);
  return 1;
}

void trie_destroy (trie_t *root)
{
  int i;

  if (root == NULL)
  {
    return;
  }

  for (i=0; i<max_edges; i++)
  {
    trie_destroy (root->edge[i]);
  }

  trie_free_node (root);
}
