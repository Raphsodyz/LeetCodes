using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class MinimumCommonValue : ISolutionContract
    {
        public void Solution()
        {
            /*
            2540. Minimum Common Value
            Difficulty: Easy
            https://leetcode.com/problems/minimum-common-value/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public int GetCommon(int[] nums1, int[] nums2) {
            int nums1Pointer = default;
            int nums2Pointer = default;

            while (nums1Pointer < nums1.Length && nums2Pointer < nums2.Length){
                if (nums1[nums1Pointer] == nums2[nums2Pointer])
                    return nums1[nums1Pointer];
                else if (nums1[nums1Pointer] > nums2[nums2Pointer])
                    nums2Pointer++;
                else
                    nums1Pointer++;
            }

            return -1;
        }
    }
}
