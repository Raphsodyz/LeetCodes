using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class LargestPositiveIntegerThatExistsWithItsNegative : ISolutionContract
    {
        public void Solution()
        {
            /*
            2441. Largest Positive Integer That Exists With Its Negative
            Difficulty: Easy
            https://leetcode.com/problems/largest-positive-integer-that-exists-with-its-negative/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public int FindMaxK(int[] nums) {
            int maxValidNumber = -1;
            HashSet<int> validNumbers = new();

            foreach (int num in nums) {
                if (validNumbers.Contains(-num))
                    maxValidNumber = Math.Max(maxValidNumber, Math.Abs(num));
        
                validNumbers.Add(num);
            }
    
            return maxValidNumber;
        }
    }
}
