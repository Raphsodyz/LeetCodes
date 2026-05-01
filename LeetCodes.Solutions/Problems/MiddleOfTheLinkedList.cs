using LeetCodes.Solutions.Contract;

namespace LeetCodes.Solutions.Problems
{
    public class MiddleOfTheLinkedList : ISolutionContract
    {
        public void Solution()
        {
            /*
            876. Middle of the Linked List
            Difficulty: Easy
            https://leetcode.com/problems/middle-of-the-linked-list/
            */

            // TODO: Add your test call here, e.g.:
            // Console.WriteLine(YourMethod(input));
        }

        public ListNode MiddleNode(ListNode head) {
            ListNode car = head;
            int sizeOfTheList = 1;

            while (car.next != null){
                car = car.next;
                sizeOfTheList++;
            }

            bool isOdd = sizeOfTheList % 2 != 0 ? true : false;
            int middleOfTheList = (int)Math.Ceiling((double)sizeOfTheList / 2);
            middleOfTheList = isOdd ? middleOfTheList : middleOfTheList + 1;

            for (int i = 1; i != middleOfTheList; i++)
                head = head.next;

            return head;
        }
    }
}
