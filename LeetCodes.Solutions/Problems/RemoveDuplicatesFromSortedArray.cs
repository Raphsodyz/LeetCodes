using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class RemoveDuplicatesFromSortedArray : ISolutionContract
    {
        public void Solution()
        {
            /*
            26. Remove Duplicates from Sorted Array
            Difficulty: Easy
            https://leetcode.com/problems/remove-duplicates-from-sorted-array/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public int RemoveDuplicates(int[] nums) {
            int left = 0;
            int right = 1;

            if (nums.Length == 1)
                return 1;

            if (nums.Length == 2 && nums[left] != nums[right])
                return 2;

            while (right <= nums.Length - 1) {
                if (nums[right] != nums[left]){
                    left++;
                    nums[left] = nums[right];
                }
                else
                    right++;
            }

            return left + 1;
        }
    }
}
