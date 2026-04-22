using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class BackspaceStringCompare : ISolutionContract
    {
        public void Solution()
        {
            /*
            844. Backspace String Compare
            Difficulty: Easy
            https://leetcode.com/problems/backspace-string-compare/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public bool BackspaceCompare(string s, string t) {
            string joinedString = string.Join(";", s, t);

            int left = default;
            int right = joinedString.Length - 1;
            int backSpaceCounter = default;

            StringBuilder builder = new();
            HashSet<string> result = new();

            while (right >= left){
                if (joinedString[right].Equals(';')){
                    result.Add(builder.ToString());
                    builder.Clear();
                    backSpaceCounter = default;
                    right--;
                    continue;
                }

                if (joinedString[right].Equals('#')){
                    backSpaceCounter++;
                    right--;
                    continue;
                }

                if (backSpaceCounter != default){
                    backSpaceCounter--;
                    right--;
                    continue;
                }

                builder.Append(joinedString[right]);
                right--;
            }

            return !result.Add(builder.ToString());
        }
    }
}
