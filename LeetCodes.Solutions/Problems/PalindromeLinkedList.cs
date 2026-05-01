using LeetCodes.Solutions.Contract;
using static LeetCodes.Solutions.Problems.MiddleOfTheLinkedList;

namespace LeetCodes.Solutions.Problems
{
    public class PalindromeLinkedList : ISolutionContract
    {
        public void Solution()
        {
            /*
            234. Palindrome Linked List
            Difficulty: Easy
            https://leetcode.com/problems/palindrome-linked-list/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public bool IsPalindrome(ListNode head) {
            List<int> originalValues = new();
            while (head != null){
                originalValues.Add(head.val);
                head = head.next;
            }

            List<int> reversedValues = new(originalValues);
            reversedValues.Reverse();
    
            if (originalValues.SequenceEqual(reversedValues))
                return true;
            else
                return false;
        }
    }
}
