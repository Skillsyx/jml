using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WinFormsApp1
{
    class Checksum
    {
        // 计算校验和并返回附加校验和的字符串
        private string GetChecksum(string str)
        {
            int CheckSum = 0x00;

            // 将字符串中的每个字符转换为其16进制表示的数值并累加
            for (int i = 0; i < str.Length; i++)
            {
                int value = Convert.ToInt32(str[i]);
                // Console.WriteLine($"字符: {str[i]}, 值: {value:X}, 当前校验和: {CheckSum:X}");
                CheckSum += value;
            }


            // 取总和的模65536
            CheckSum %= 65536;

            // 对模65536的结果取反并加1
            CheckSum = (CheckSum ^ 0xFFFF) + 1;

            // 将校验和附加到原字符串末尾，并加上回车字符 (0x0D)
            return "~" + str + CheckSum.ToString("X4") + "\r\n";
        }


        // 将输入信息转化为特定格式，并计算其校验和
        public string Getinfo(string Info)
        {
            string info = "";

            // 将输入信息中的每个字符转化为其16进制Unicode表示并拼接
            for (int i = 0; i < Info.Length; i++)
            {
                info += ((int)Info[i]).ToString("X4");
            }

            // 拼接其他固定部分和info
            string fixedPart1 = "00580030";
            string fixedPart2 = "001F";
            string fixedPart3 = "0201";

            string info2 = fixedPart1 + info + fixedPart2;
            string fixedPart4 = info2.Length.ToString("X4");
            string info3 = fixedPart3 + fixedPart4 + info2;
            // 计算info2的校验和
            string asinfo = GetChecksum(info3);

            return asinfo;
        }
    }
}
