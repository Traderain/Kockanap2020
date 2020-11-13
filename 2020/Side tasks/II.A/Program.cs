using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace II.A
{
    class Program
    {
        static List<string> CollectResults<T>(List<T> nums, List<string> outerResultStr = null)
        {
            var resultStr = new List<string>();
            var collectedNums = new List<List<T>>();
            for (int i = 0; i < nums.Count; i++)
            {
                dynamic currVal = nums[i];
                var currcollectedNums = new List<T>();
                currcollectedNums.Add(currVal);
                while (i + 1 < nums.Count && currVal + 1 == nums[i + 1])
                {
                    currVal++;
                    i++;
                    currcollectedNums.Add(currVal);
                }
                collectedNums.Add(currcollectedNums);
            }
            for (int i = 0; i < collectedNums.Count; i++)
            {
                var collectedNumsItem = collectedNums[i];
                if (collectedNumsItem.Count >= 3)
                {
                    resultStr.Add($"{collectedNumsItem.First()}-{collectedNumsItem.Last()}");
                }
                else
                {
                    for (int j = 0; j < collectedNumsItem.Count; j++)
                    {
                        dynamic item = collectedNumsItem[j];
                        if (outerResultStr != null)
                        {
                            // Do not add same upper chars
                            if (!outerResultStr.Contains(char.ToLower(item).ToString()))
                                outerResultStr.Add(item.ToString()); 
                        }
                        else
                            resultStr.Add(item.ToString());
                    }
                }
            }

            return resultStr;
        }

        static void Main(string[] args)
        {
            var line = Console.ReadLine();
            var splittedObj = line.Split(new char[] { ',', '[', ']' });
            var splitted = new List<string>();
            foreach (var item in splittedObj)
            {
                if (!string.IsNullOrEmpty(item))
                    splitted.Add(item);
            }
            var resultObj = new List<object>();
            for (var i = 0; i < splitted.Count; i++)
            {
                object item = splitted[i];
                if (int.TryParse(item.ToString(), out int num))
                    item = num;
                else
                    item = splitted[i][0];
                resultObj.Add(item);
            }

            var orderedNumbers = new List<int>();
            var orderedUpperChars = new List<char>();
            var orderedLowerChars = new List<char>();
            foreach (var item in resultObj)
            {
                if (item is int && !orderedNumbers.Contains((int)item))
                    orderedNumbers.Add((int)item);
                if (item is char && char.IsUpper((char)item) && !orderedUpperChars.Contains((char)item))
                    orderedUpperChars.Add((char)item);
                if (item is char && char.IsLower((char)item) && !orderedUpperChars.Contains((char)item))
                    orderedLowerChars.Add((char)item);
            }

            orderedNumbers.Sort();
            orderedLowerChars.Sort();
            orderedUpperChars.Sort();

            var resultStr = new List<string>();
            resultStr.AddRange(CollectResults(orderedNumbers));
            resultStr.AddRange(CollectResults(orderedLowerChars));
            resultStr.AddRange(CollectResults(orderedUpperChars, resultStr));

            Console.WriteLine(string.Join(",", resultStr));
        }
    }
}
