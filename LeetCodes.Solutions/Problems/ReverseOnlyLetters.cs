using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class ReverseOnlyLetters : ISolutionContract
    {
        public void Solution()
        {
            /*
            917. Reverse Only Letters
            Difficulty: Easy
            https://leetcode.com/problems/reverse-only-letters/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public string ReverseOnlyLetters(string s) {
            int left = 0;
            int right = s.Length - 1;
            char[] result = new char[s.Length];

            while(left <= right) {
                if (!char.IsLetter(s[left])) {
                    result[left] = s[left];
                    left++;
                }
                else if (!char.IsLetter(s[right])) {
                    result[right] = s[right];
                    right--;
                }
                else {
                    result[left] = s[right];
                    result[right] = s[left];
                    left++;
                    right--;
                }
            }

            return new string(result);
        }
    }
}
