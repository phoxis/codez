#include <cstdio>
#include <locale>
#include "trie.hpp"
#include "set_maps.hpp"

// To test the interfaces for bengali
int main (int argc, char *argv[])
{
  trie_t *root;
  wchar_t str[STR_MAX];
  char word_list_file[STR_MAX] = "/usr/share/dict/words";

  setlocale (LC_ALL, "");
  
  fwprintf (stdout, L"First argument is path to word list file. If not present then %s is used\n", word_list_file);
  if (argc == 2)
  {
    strcpy (word_list_file, argv[1]);
  }
  
  fwprintf (stdout, L"Loading word list: \"%s\"\n", word_list_file);
  root = trie_init (english_map);
//   root = trie_init (bengali_map);
  trie_load_word_list (root, word_list_file);

  while (1)
  {
    fwprintf (stdout, L"Word to search (\'q\' to quit): ");
    fwscanf (stdin, L"%ls", str);
    if (str[0] == L'q' && str[1] == L'\0')
    {
      break;
    }
    if (trie_search (root, str))
    {
      fwprintf (stdout, L"Found\n");
    }
    else
    {
      fwprintf (stdout, L"Not Found\n");
    }
    trie_search_autocomplete (root, str, -1);
  }

  trie_destroy (root);

  fwprintf (stdout, L"total_alloc = %d nodes\ntotal_free = %d nodes\nnode_size = %db\n", total_alloc, total_free, node_size);

  return 0;
}
