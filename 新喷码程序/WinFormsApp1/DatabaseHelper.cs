using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WinFormsApp1
{
    public static class DatabaseHelper
    {
        // 连接字符串（可改为读取配置文件）
        private static readonly string connectionString = "Server=172.16.1.9;Database=yx_test;User Id=sa;Password=Ks123456;TrustServerCertificate=True";

        /// <summary>
        /// 执行查询语句并返回结果DataTable
        /// </summary>
        public static DataTable ExecuteQuery(string sql)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                DataTable dt = new DataTable();
                try
                {
                    conn.Open();
                    using (SqlCommand cmd = new SqlCommand(sql, conn))
                    {
                        SqlDataAdapter adapter = new SqlDataAdapter(cmd);
                        adapter.Fill(dt);
                    }
                }
                catch (Exception ex)
                {
                    throw new Exception("查询失败：" + ex.Message);
                }
                return dt;
            }
        }

        /// <summary>
        /// 执行插入、更新、删除等操作，返回影响行数
        /// </summary>
        public static int ExecuteNonQuery(string sql)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                try
                {
                    conn.Open();
                    using (SqlCommand cmd = new SqlCommand(sql, conn))
                    {
                        return cmd.ExecuteNonQuery();
                    }
                }
                catch (Exception ex)
                {
                    throw new Exception("执行失败：" + ex.Message);
                }
            }
        }

        /// <summary>
        /// 执行单值查询，例如 SELECT COUNT(*)，返回 object
        /// </summary>
        public static object ExecuteScalar(string sql)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                try
                {
                    conn.Open();
                    using (SqlCommand cmd = new SqlCommand(sql, conn))
                    {
                        return cmd.ExecuteScalar();
                    }
                }
                catch (Exception ex)
                {
                    throw new Exception("执行失败：" + ex.Message);
                }
            }
        }
    }
}