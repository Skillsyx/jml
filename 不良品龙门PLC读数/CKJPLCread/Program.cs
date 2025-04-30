using S7.Net;
using System;
using CKJPLCread;

class Program
{
    static void Main(string[] args)
    {
        try
        {
            // 创建PLC连接实例，使用S7-1200/1500
            using (var plc = new Plc(CpuType.S71500, "192.168.1.20", 0, 1))
            {
                while (true)
                {
                    try
                    {
                        // 连接到PLC
                        Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] 尝试连接到PLC...");
                        plc.Open();
                        Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] PLC连接成功！");
                        break; // 连接成功，跳出重试循环
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] 连接失败: {ex.Message}");
                        Console.WriteLine("5秒后重试...");
                        System.Threading.Thread.Sleep(5000);
                    }
                }
                
                // 接收记录初始值
                int initialvalue = (int)plc.Read(DataType.DataBlock, 17, 44, VarType.DInt, 1);
                
                while (true)
                {
                    // 读取DB17.DBD44的DINT值
                    int value1 = (int)plc.Read(DataType.DataBlock, 17, 44, VarType.DInt, 1);
                    
                    // 读取DB19.DBW10的Int值
                    short value2 = (short)plc.Read(DataType.DataBlock, 19, 10, VarType.Int, 1);
                    
                    Console.WriteLine($"DB17.DBD44的值为: {value1} , DB19.DBW10的值为: {value2}");
                    
                    
                    if (value2 >= 1000){
                        // 记录抓取时间
                        DateTime now = DateTime.Now;
                        while (true){
                            int value3 = (int)plc.Read(DataType.DataBlock, 17, 44, VarType.DInt, 1);
                            short value4 = (short)plc.Read(DataType.DataBlock, 19, 10, VarType.Int, 1);

                            if (value4 == 0 ){
                                // 记录放下时间
                                DateTime now2 = DateTime.Now;
                                
                                // 创建数据库帮助类实例
                                var dbHelper = new DatabaseHelper();
                                // 插入PLC记录
                                dbHelper.InsertPLCRecord(initialvalue, value3, now, now2, "肤感线");
                                break; // 退出内层循环
                            }

                            System.Threading.Thread.Sleep(1000);
                        }
                    }
                    
                    // 等待1秒
                    System.Threading.Thread.Sleep(1000);
                }

                
                // 关闭连接
                plc.Close();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"发生错误: {ex.Message}");
        }
       
    }
}
