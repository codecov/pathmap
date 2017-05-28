#include "unity.h"
#include "../../pathmap/lcsmodule.h"

void test_longest_common_substring() {
	int *results = _lcs("This is a string", "And a substring");

	/* The first item in the list contains the length
	 * this should be "string" = 6
	 */
	TEST_ASSERT_EQUAL_INT(6, results[0]);

	/* The second item in the list tells us
	 * the index where the substring end
	 */
	TEST_ASSERT_EQUAL_INT(15, results[1]);
}

int main(void)
{
	UNITY_BEGIN();
	RUN_TEST(test_longest_common_substring);
	return UNITY_END();
}
