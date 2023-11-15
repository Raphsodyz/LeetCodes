namespace Program
{
/*
    3. Longest Substring Without Repeating Characters
    Solved
    Medium
    Topics
    Companies

    Given a string s, find the length of the longest
    substring
    without repeating characters.

    Example 1:

    Input: s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with the length of 3.

    Example 2:

    Input: s = "bbbbb"
    Output: 1
    Explanation: The answer is "b", with the length of 1.

    Example 3:

    Input: s = "pwwkew"
    Output: 3
    Explanation: The answer is "wke", with the length of 3.
    Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

    Constraints:
        0 <= s.length <= 5 * 104
        s consists of English letters, digits, symbols and spaces.

*/
    class Program{
        static int LengthOfLongestSubstring(string s) {
            int n = s.Length;
            int maxLength = 0;
            HashSet<char> charSet = new();
            int left = 0;
            
            for (int right = 0; right < n; right++) {
                if (charSet.Add(s[right])) 
                    maxLength = Math.Max(maxLength, right - left + 1);
                else {
                    while (charSet.Contains(s[right])) {
                        charSet.Remove(s[left]);
                        left++;
                    }
                    charSet.Add(s[right]);
                }
            }
            return maxLength;
        }

        public static void Main(string[] args)
        {
            string input = "abcabcbb";
            Console.WriteLine(LengthOfLongestSubstring(input));
        }
    }
}