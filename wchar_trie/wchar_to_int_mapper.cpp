#include <iostream>
#include <unordered_map>
#include <cwchar>
// #include "wchar_to_int_mapper.cpp"

static std::unordered_map<wchar_t,int> wchar_mapper;
static std::unordered_map<int,wchar_t> wchar_reverse_mapper; // For autocomplete link search
int max_keys = 0;

/* Last element of 'chars_to_map' SHOULD be L'\0'. 
 * Else we will be in trouble.
 */
void init_wchar_mapper (wchar_t *chars_to_map)
{
  int i;
  
  for (i=0; chars_to_map[i] != L'\0'; i++)
  {
    max_keys++;
    wchar_mapper.insert (std::pair<wchar_t,int> (chars_to_map[i], i));
    wchar_reverse_mapper.insert (std::pair<int,wchar_t> (i, chars_to_map[i]));
  }
}

int wchar_map_to_int (wchar_t key)
{
  std::unordered_map<wchar_t,int>::const_iterator retpair = wchar_mapper.find (key);
  
  if (retpair == wchar_mapper.end ())
  {
    return -1;
  }

  return retpair->second;
}

wchar_t int_map_to_wchar (int key)
{
  std::unordered_map<int,wchar_t>::const_iterator retpair = wchar_reverse_mapper.find (key);
  
  if (retpair == wchar_reverse_mapper.end ())
  {
    return -1;
  }
  
  return retpair->second;
}
