using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class MaxNumberOfKsumPairs : ISolutionContract
    {
        public void Solution()
        {
            /*
            1679. Max Number of K-Sum Pairs
            Difficulty: Medium
            https://leetcode.com/problems/max-number-of-k-sum-pairs/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public int MaxOperations(int[] nums, int k) {
            int operations = default;
            List<int> values = new List<int>();
    
            for (int i = 0; i < nums.Length; i++)
            {
                if (nums[i] >= k)
                    continue;

                int value = k - nums[i];
                if (values.Contains(nums[i])){
                    values.Remove(nums[i]);
                    operations++;
                    continue;
                }
        
                values.Add(value);
            }

            return operations;
        }
    }
}
