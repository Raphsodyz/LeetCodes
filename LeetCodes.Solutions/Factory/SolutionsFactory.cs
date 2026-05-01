using LeetCodes.Solutions.Contract;
using LeetCodes.Solutions.Problems;

namespace LeetCodes.Solutions.Factory
{
    public static class SolutionsFactory
    {
        public static ISolutionContract Create(string problem)
        {
            return problem switch
            {
                nameof(LongestSubstringWithoutRepeatingCharacters) => new LongestSubstringWithoutRepeatingCharacters(),
                nameof(ReverseLettersThenSpecialCharactersInAString) => new ReverseLettersThenSpecialCharactersInAString(),
                nameof(StringToInteger) => new StringToInteger(),
                nameof(InvertBinaryTree) => new InvertBinaryTree(),
                nameof(MinimumCommonValue) => new MinimumCommonValue(),
                nameof(BackspaceStringCompare) => new BackspaceStringCompare(),
                nameof(LexicographicallySmallestPalindrome) => new LexicographicallySmallestPalindrome(),
                nameof(MaxNumberOfKsumPairs) => new MaxNumberOfKsumPairs(),
                nameof(IsSubsequence) => new IsSubsequence(),
                nameof(LargestPositiveIntegerThatExistsWithItsNegative) => new LargestPositiveIntegerThatExistsWithItsNegative(),
                nameof(FindAllKdistantIndicesInAnArray) => new FindAllKdistantIndicesInAnArray(),
                nameof(ReverseString) => new ReverseString(),
                nameof(PalindromeLinkedList) => new PalindromeLinkedList(),
                nameof(MiddleOfTheLinkedList) => new MiddleOfTheLinkedList(),
                nameof(ReverseOnlyLetters) => new ReverseOnlyLetters(),
                nameof(NumberOfPerfectPairs) => new NumberOfPerfectPairs(),
                _ => throw new ArgumentException("Invalid problem name.")
            };
        }
    }
}