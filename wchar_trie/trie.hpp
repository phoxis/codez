#ifndef TRIE_H
#define TRIE_H

#include <iostream>
#include <cstring>
#include <cstdio>
#include "wchar_to_int_mapper.hpp"

// TODO
#define STR_MAX 256

#define TRIE_VERIFY 1

typedef struct _trie_t {
  int mark;
  struct _trie_t **edge;
} trie_t;

extern unsigned int total_alloc, total_free;
extern int max_edges, node_size;

trie_t *trie_alloc_node (void);
void trie_free_node (trie_t *node);
int toindex (wchar_t x);
int validate_string (wchar_t *str);
int trie_add_word (trie_t *root, wchar_t *str);
int trie_search (trie_t *root, wchar_t *str);
int trie_load_word_list (trie_t *root, char *file);
void trie_show (trie_t *root, wchar_t *prefix, int max_depth);
trie_t *trie_init (wchar_t *lang_map);
void trie_destroy (trie_t *root);
int trie_search_autocomplete (trie_t *root, wchar_t *str, int max_depth);


#endif

