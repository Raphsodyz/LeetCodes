using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class NumberOfPerfectPairs : ISolutionContract
    {
        public void Solution()
        {
            /*
            3649. Number of Perfect Pairs
            Difficulty: Medium
            https://leetcode.com/problems/number-of-perfect-pairs/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public long PerfectPairs(int[] nums) {
            Array.Sort(nums, (a, b) => Math.Abs(a).CompareTo(Math.Abs(b)));

            int left = 0;
            int right = 0;
            long perfectPairsCount = default;

            while (left < nums.Length) {
                while (right < nums.Length && Math.Abs(nums[right]) <= 2L * Math.Abs(nums[left]))
                    right++;

                perfectPairsCount += right - left - 1;
                left++;
            }

            return perfectPairsCount;
        }
    }
}
