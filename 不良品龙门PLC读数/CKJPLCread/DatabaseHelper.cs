using System;
using System.Data;
using System.Data.SqlClient;

namespace CKJPLCread
{
    public class DatabaseHelper
    {
        private readonly string connectionString;

        public DatabaseHelper()
        {
            // 构建数据库连接字符串
            connectionString = "Server=172.16.1.9;Database=YX_test;User Id=sa;Password=Ks123456;";
        }

        public void InsertPLCRecord(int initialValue, int currentValue, DateTime captureTime, DateTime dropTime, string productionLine)
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();

                    string insertQuery = @"INSERT INTO PLC_Run_Records_yx 
                                         (InitialValue, CurrentValue, CaptureTime, DropTime, ProductionLine)
                                         VALUES (@InitialValue, @CurrentValue, @CaptureTime, @DropTime, @ProductionLine)";

                    using (SqlCommand command = new SqlCommand(insertQuery, connection))
                    {
                        command.Parameters.AddWithValue("@InitialValue", initialValue);
                        command.Parameters.AddWithValue("@CurrentValue", currentValue);
                        command.Parameters.AddWithValue("@CaptureTime", captureTime);
                        command.Parameters.AddWithValue("@DropTime", dropTime);
                        command.Parameters.AddWithValue("@ProductionLine", productionLine);

                        command.ExecuteNonQuery();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"数据库操作错误: {ex.Message}");
                throw;
            }
        }

        public void TestConnection()
        {
            try
            {
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    Console.WriteLine("数据库连接测试成功！");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"数据库连接测试失败: {ex.Message}");
                throw;
            }
        }
    }
}