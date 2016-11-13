#ifndef WCHAR_TO_INT_MAPPER_H
#define WCHAR_TO_INT_MAPPER_H

int wchar_map_to_int (wchar_t key);
void init_wchar_mapper (wchar_t *chars_to_map);
wchar_t int_map_to_wchar (int key);

extern int max_keys;


#endif