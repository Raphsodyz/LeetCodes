using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class FindAllKdistantIndicesInAnArray : ISolutionContract
    {
        public void Solution()
        {
            /*
            2200. Find All K-Distant Indices in an Array
            Difficulty: Easy
            https://leetcode.com/problems/find-all-k-distant-indices-in-an-array/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public IList<int> FindKDistantIndices(int[] nums, int key, int k) {
            int left = default; 
            int right = nums.Length - 1;
            int range = 2 * k + 1;
            HashSet<int> result = new(); 

            while (left <= right) {
                if (nums[left] == key) {
                    IEnumerable<int> leftPossibleResults = Enumerable.Range((left - k), range);
                    foreach (int possibleResult in leftPossibleResults){
                        if (possibleResult >= 0 && possibleResult <= nums.Length - 1)
                            result.Add(possibleResult);
                    }
                }
            
                if (nums[right] == key){
                    IEnumerable<int> rightPossibleResults = Enumerable.Range((right - k), range);
                    foreach (int possibleResult in rightPossibleResults){
                        if (possibleResult >= 0 && possibleResult <= nums.Length - 1)
                            result.Add(possibleResult);
                    }
                }
            
                right--; 
                left++;
            }
    
            return result.Order().ToList();
        }
    }
}
