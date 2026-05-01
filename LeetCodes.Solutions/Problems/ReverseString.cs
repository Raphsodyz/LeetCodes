using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class ReverseString : ISolutionContract
    {
        public void Solution()
        {
            /*
            344. Reverse String
            Difficulty: Easy
            https://leetcode.com/problems/reverse-string/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public void ReverseString(char[] s) {
            int left = 0;
            int right = s.Length - 1;

            while (left < right){
                char tmp = s[right];

                s[right] = s[left];
                s[left] = tmp;

                left++;
                right--;
            }
        }
    }
}
