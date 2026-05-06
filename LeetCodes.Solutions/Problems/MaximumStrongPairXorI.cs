using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class MaximumStrongPairXorI : ISolutionContract
    {
        public void Solution()
        {
            /*
            2932. Maximum Strong Pair XOR I
            Difficulty: Easy
            https://leetcode.com/problems/maximum-strong-pair-xor-i/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public int MaximumStrongPairXor(int[] nums) {
            int left = 0;
            int right = 1;
            int result = 0;

            while (left < nums.Length - 1){
                if (Math.Abs(nums[left] - nums[right]) <= Math.Min(nums[left], nums[right])){
                    int xorSum = nums[left] ^ nums[right];
                    if (xorSum > result)
                        result = xorSum;
                }

                if (right == nums.Length - 1){
                    left++;
                    right = left + 1;
                }
                else
                    right++;
            }

            return result;
        }
    }
}
