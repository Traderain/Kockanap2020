using System;
using System.Collections.Generic;

namespace _3B
{
    class Program
    {
        static void Main(string[] args)
        {
            string currstr = "";
            long idx = 1;
            long v = 1;
            long n = long.Parse(Console.ReadLine());
            string[] vresults = new string[n];
            bool countingUp = false;
            long strnum = 1;
            while (v <= n)
            {
                currstr += idx;
                if (idx == 4 || idx == 1)
                    countingUp = !countingUp;
                if (countingUp)
                    idx++;
                else
                    idx--;

                if (v == strnum)
                {
                    vresults[v - 1] = currstr;
                    currstr = "";
                    v++;
                    strnum = 0;
                }
                strnum += idx;
            }
            
            // Adding byte by byte...
            for (int i = 0; i < vresults.Length - 1; i++)
            {
                var strlen = Math.Max(vresults[i].TrimStart('0').Length, vresults[i + 1].TrimStart('0').Length) + 1;
                vresults[i] = vresults[i].PadLeft(strlen, '0');
                vresults[i + 1] = vresults[i + 1].PadLeft(strlen, '0');
                int carrier = 0;
                byte[] newstr = new byte[strlen];
                for (int j = strlen - 1; j >= 0; j--)
                {
                    var newval = vresults[i][j] + vresults[i + 1][j] - 2 * '0' + carrier;
                    carrier = newval / 10;
                    newstr[j] = (byte)(newval % 10);
                }
                vresults[i + 1] = string.Join("", newstr);
            }
            string sum = vresults[vresults.Length - 1];

            // Do step by step division
            long mod = 0;
            long m = 123454321;
            string res = "";
            for (int i = 0; i < sum.Length; i++)
            {
                int digit = sum[i] - '0';

                // Update modulo by concatenating 
                // current digit. 
                mod = mod * 10 + digit;

                // Update quotient  
                long quo = mod / m;
                res += quo;

                // Update mod for next iteration. 
                mod = mod % m;
            }

            Console.WriteLine(mod);
        }
    }
}
