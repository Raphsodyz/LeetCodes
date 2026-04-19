using LeetCodes.Solutions.Factory;
using LeetCodes.Solutions.Problems;

internal static class Program
{
    private static void Main()
    {
        var question = SolutionsFactory.Create(nameof(ReverseLettersThenSpecialCharactersInAString));
        question.Solution();
    }
}