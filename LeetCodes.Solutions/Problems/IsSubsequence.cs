using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class IsSubsequence : ISolutionContract
    {
        public void Solution()
        {
            /*
            392. Is Subsequence
            Difficulty: Easy
            https://leetcode.com/problems/is-subsequence/
            */

            // TODO: Add your test call here, e.g.:
            Console.WriteLine(IsSubsequenceSolution("abc", "axcbdfc"));
        }

        public bool IsSubsequenceSolution(string s, string t) {
            int left = 0;
            int right = t.Length - 1;
            Queue<char> sValues = new(s);

            while(left <= right){
                if (sValues.Count > 0 && sValues.First() == t[left])
                    sValues.Dequeue();

                left++;
            }

            if (sValues.Count == 0)
                return true;

            return false;
        }
    }
}
