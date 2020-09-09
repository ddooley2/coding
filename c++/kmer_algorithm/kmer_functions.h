#include <vector>

const std::vector<int> bitap_bitwise_search(const char *text, const char *pattern)
{
	int m = strlen(pattern);
	unsigned long R;
	unsigned long pattern_mask[CHAR_MAX + 1];
	int i;
	std::vector<int> indices;
	/* Initialize the bit array R */
	R = ~1;
	/* Initialize the pattern bitmasks */
	for (int i = 0; i <= CHAR_MAX; ++i)
		pattern_mask[i] = ~0;
	for (int i = 0; i < m; ++i)
		pattern_mask[pattern[i]] &= ~(1UL << i);
	for (int i = 0; text[i] != '\0'; ++i) {
		/* Update the bit array */
		R |= pattern_mask[text[i]];
		R <<= 1;
		if (0 == (R & (1UL << m)))
			indices.push_back(i - m + 1);
			//return i - m + 1;
	}
	return indices;
}