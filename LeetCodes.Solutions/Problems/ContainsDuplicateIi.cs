using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class ContainsDuplicateIi : ISolutionContract
    {
        public void Solution()
        {
            /*
            219. Contains Duplicate II
            Difficulty: Easy
            https://leetcode.com/problems/contains-duplicate-ii/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public bool ContainsNearbyDuplicate(int[] nums, int k) {
            HashSet<int> window = new();
            for (int i = 0; i <= nums.Length - 1; i++){
                if (i <= k){
                    if(!window.Add(nums[i]))
                        return true;
                }
                else {
                    window.Remove(nums[(i - k - 1)]);
                    if (!window.Add(nums[i]))
                        return true;
                }
            }

            return false;
        }
    }
}
