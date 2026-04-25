using System.Text;
using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class LexicographicallySmallestPalindrome : ISolutionContract
    {
        public void Solution()
        {
            /*
            2697. Lexicographically Smallest Palindrome
            Difficulty: Easy
            https://leetcode.com/problems/lexicographically-smallest-palindrome/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public string MakeSmallestPalindrome(string s) {
            int right = 0;
            int left = s.Length - 1;

            StringBuilder result = new(s);
            while (right < left){
                if (result[right] != result[left]){
                    if (result[left] > result[right])
                        result[left] = result[right];
                    else
                        result[right] = result[left];
                }

                left--;
                right++;
            }

            return result.ToString();
        }
    }
}
