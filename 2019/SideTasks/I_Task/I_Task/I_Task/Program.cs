using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace I_Task
{
    class Program
    {
        static void Main(string[] args)
        {
            int[,] rooms;
            int width = 0;
            int height = 0;
            string line = "";

            using (StreamReader reader = new StreamReader("inputs.txt"))
            {
                string size = reader.ReadLine();
                width = int.Parse(size.Split(' ')[0]);
                height = int.Parse(size.Split(' ')[1]);

                rooms = new int[width, height];

                int rowIndex = 0;
                while ((line = reader.ReadLine()) != null)
                {
                    var rowElements = line.Split(' ');
                    int columnIndex = 0;
                    foreach (var element in rowElements)
                    {
                        rooms[rowIndex, columnIndex] = int.Parse(element);
                        columnIndex++;
                    }
                    rowIndex++;
                }
            }

            for (int i = 0; i < rooms.GetLength(0); i++)
            {
                for (int j = 0; j < rooms.GetLength(1); j++)
                {
                    Console.Write(rooms[i, j] + " ");
                }
                Console.Write(Environment.NewLine);
            }

            Soldier S = new Soldier();
            S.X = 0;
            S.Y = 0;
            S.Ammo = rooms[0, 0];

            #region retard_custom
            int sumX = 0;
            int sumY = 0;

            while (S.X <= width - 1 && S.Y <= height - 1)
            {
                if (S.Y < width - 1)
                {
                    sumX = S.Ammo + (rooms[S.X, S.Y + 1]);
                }
                else
                {
                    sumX = 100000;
                }
                if (S.X < height - 1)
                {
                    sumY = S.Ammo + (rooms[S.X + 1, S.Y]);
                }
                else
                {
                    sumY = 100000;
                }

                if (Math.Abs(sumX) <= Math.Abs(sumY))
                {
                    S.Ammo = sumX;
                    S.Y++;
                }
                else
                {
                    S.Ammo = sumY;
                    S.X++;
                }

                if (S.Y == width - 1 && S.X == height - 1)
                    break;
            }
            #endregion

            Console.WriteLine();
            int result = (S.Ammo <= 0 ? Math.Abs(S.Ammo) + 1 : S.Ammo);
            Console.WriteLine("Minimum ammo required: " + result);
            Console.ReadKey();
        }
    }

    class Soldier
    {
        public int Ammo { get; set; }
        public int X { get; set; }
        public int Y { get; set; }
    }

    class Vertex
    {
        public Vertex prev { get; set; }
        public int Weight { get; set; }
    }
}
