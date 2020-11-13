using System;
using System.Collections.Generic;

namespace _2A
{
    class Program
    {
        static Dictionary<char, char> decoder = new Dictionary<char, char> {
            { '1', 'I' },
            { '2', 'R' },
            { '3', 'E' },
            { '4', 'A' },
            { '5', 'S' },
            { '6', 'G' },
            { '7', 'T' },
            { '8', 'B' },
            { '9', 'P' },
            { '0', 'O' }};

        static void Main(string[] args)
        {
            var inputStr = "";
            string line;
            while ((line = Console.ReadLine()) != null && line != "")
                inputStr += line;

            var sentenceStart = true;
            var result = "";
            foreach (var c in inputStr)
            {
                var new_c = c;
                if (decoder.ContainsKey(c))
                    new_c = decoder[c];
                if (sentenceStart && 'A' <= new_c && new_c <= 'Z')
                {
                    new_c = char.ToUpper(new_c);
                    sentenceStart = false;
                }
                else
                    new_c = char.ToLower(new_c);
                if (c == '.' || c == '!' || c == '?')
                    sentenceStart = true;
                result += new_c;
            }

            Console.WriteLine(result);
        }
    }
}
