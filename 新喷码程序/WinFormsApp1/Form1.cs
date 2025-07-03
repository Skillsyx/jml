using Microsoft.Identity.Client;
using System;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        // 构造函数：初始化窗体和界面状态

        private PrinterClient printerClient;
        private bool isDataSaved = false;

        public Form1()
        {
            InitializeComponent();
            InitializeStatus();
            printerClient = new PrinterClient(this); // 传入主窗体引用用于日志输出
            printerClient.Initialize("192.168.1.35", "192.168.1.30", 3000);
            //printerClient.Initialize("172.16.10.45", "172.16.10.37", 3000);
            this.textBox1.Leave += new System.EventHandler(this.textBox1_Leave);
            comboBox1.SelectedIndexChanged += comboBox1_SelectedIndexChanged;
            checkBox1.CheckedChanged += checkBox1_CheckedChanged;
            this.FormClosing += Form1_FormClosing;


        }



        // 当前时间（可供其他操作复用）
        public string newdate => DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");


        // 添加日志并自动滚动到底部,自动清空
        public void AddLog(string msg)
        {

            if (listBox1.Items.Count >= 100)
            {
                listBox1.Items.Clear();
                listBox1.Items.Add($"{newdate} 日志已清空");
            }

            listBox1.Items.Add($"{newdate} {msg}");
            listBox1.TopIndex = listBox1.Items.Count - 1;
        }

        // 初始化界面状态、日志和DataGridView列结构
        private void InitializeStatus()
        {
            this.textBox1.Text = "SCDD24060876";

            label4.Text = "打印状态：未启动";
            listBox1.Items.Clear();
            AddLog("启动成功，等待操作...");

            dataGridView1.Columns.Clear();
            dataGridView1.Columns.Add("Index", "序号");
            dataGridView1.Columns.Add("Mocode", "生产订单号");
            dataGridView1.Columns.Add("Cinvcode", "产品编码");
            dataGridView1.Columns.Add("irowno", "行号");
            dataGridView1.Columns.Add("cBatch", "批号");
            dataGridView1.Columns.Add("SendTime", "发送时间");
            dataGridView1.Columns.Add("PrintTime", "打印时间");
            dataGridView1.Columns.Add("Result", "结果");

            dataGridView1.AllowUserToAddRows = false;
            dataGridView1.ReadOnly = true;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.RowHeadersVisible = false;

            AddLog("表格加载完成");
        }

        // 定义一个字段存储 DataTable（保持行数据用于查 qty_b）
        private System.Data.DataTable comboData;

        // 绑定 comboBox 时同步保存数据
        private void textBox1_Leave(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(textBox1.Text))
            {
                AddLog("请输入工单号");
                return;
            }

            string sql = $"SELECT InvCode_b, SortSeq_b, qty_b FROM ufdata_008_2021..momlist_yx WHERE MoCode_a = '{textBox1.Text}'";

            try
            {
                var dt = DatabaseHelper.ExecuteQuery(sql);
                comboData = dt; // 保存数据表

                comboBox1.Items.Clear();
                foreach (System.Data.DataRow row in dt.Rows)
                {
                    string item = $"{row["InvCode_b"]}::{row["SortSeq_b"]}";
                    comboBox1.Items.Add(item);
                }

                if (dt.Rows.Count > 0)
                {
                    comboBox1.SelectedIndex = 0;
                    //AddLog($"工单查询成功，共 {dt.Rows.Count} 条");
                }
                else
                {
                    comboBox1.Items.Clear();
                    comboBox1.SelectedIndex = -1; // 取消选中项
                    comboBox1.Text = "";              // 清空显示文本
                    textBox2.Text = "";
                    AddLog("无数据，请检查生产订单号码");
                }




            }
            catch (Exception ex)
            {
                AddLog($"查询失败: {ex.Message}");
            }
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboData == null || comboBox1.SelectedIndex < 0) return;

            var row = comboData.Rows[comboBox1.SelectedIndex];
            decimal qty = Convert.ToDecimal(row["qty_b"]);
            textBox2.Text = Math.Floor(qty).ToString("0");
        }



        // DataGridView 单元格点击事件（暂未使用）
        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
        }

        // 测试按钮点击事件：获取选中的产品编码和行号，执行编码校验
        //private void buttontest_Click(object sender, EventArgs e)
        //{


        //    dataGridView1.Rows.Clear();

        //    for (int i = 0; i < 200; i++)
        //    {
        //        dataGridView1.Rows.Add(
        //            i + 1,
        //            $"MO{i + 1000:D4}",
        //            $"P{i + 1:D5}",
        //            (i + 1).ToString(),
        //            $"BATCH{i + 1:D3}",
        //            DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
        //            "",
        //            "待打印"
        //        );
        //    }



        //    string selectcombox = comboBox1.SelectedItem.ToString();
        //    string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
        //    string key = aaa[0];
        //    string value = aaa[1];

        //    Checksum checksum = new Checksum();
        //    string abcd = checksum.Getinfo("");

        //    AddLog(abcd); // 如果 abcd 已带格式化时间则不用加 newdate
        //}

        


        //private async void buttontest_Click(object sender, EventArgs e)
        //{
        //    // 校验 ComboBox 是否选择了项目
        //    if (comboBox1.SelectedItem == null)
        //    {
        //        AddLog("请先选择产品编码");
        //        return;
        //    }

        //    string selectcombox = comboBox1.SelectedItem.ToString();
        //    string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
        //    string cinvcode = aaa[0];
        //    string irowno = aaa[1];

        //    Checksum checksum = new Checksum();

        //    // 当前时间作为编码时间
        //    var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");

        //    // 生成 CheckValue
        //    string checkvalue = checksum.Getinfo($"{cinvcode}_{datetimes}");

        //    AddLog($"发送内容：{checkvalue}");

        //    // 记录发送时间
        //    var sendtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

        //    // 发送并等待返回
        //    var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);
        //    AddLog("fasong");

        //    // 记录打印时间
        //    var printtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

        //    if (success)
        //    {
        //        AddLog($"喷码返回成功：{result}");
        //    }
        //    else
        //    {
        //        AddLog($"喷码返回失败：{result}");
        //    }

        //    // 将发送信息 + 返回信息显示出来（暂不写入 dgv，仅输出日志）
        //    AddLog($"发送时间: {sendtime}");
        //    AddLog($"打印时间: {printtime}");
        //}


        private void comboBox1_DropDownStyleChanged(object sender, EventArgs e)
        {

        }

        private async void button1_Click(object sender, EventArgs e)
        {
            if (checkBox1.Checked)
            {
                await ExecutePrintNoMoAsync();
            }
            else
            {
                await ExecutePrintAsync();
            }

            ////声明默认值
            //string selectcombox = comboBox1.SelectedItem.ToString();
            //string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            //string cinvcode = aaa[0];
            //string irowno = aaa[1];
            //Checksum checksum = new Checksum();

            ////根据textb2中的数量循环



            ////获取检查后的值 checkvalue
            //var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
            //string checkvalue = checksum.Getinfo($"{cinvcode}" + $"_{datetimes}");


            ////发送给喷码机checkvalue


            ////记录发送时间
            //var sentiment = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");


            ////等待喷码结果的返回值



            ////记录喷码时间
            //var printime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");




            ////写入dgv ，序号 = 循环的i，生成订单号 = textbox1.text ,cinvcode = cinvcode,irowno = irowno,cbatch = 0,sentimet,printtime ,喷码结果



            ////循环完成将dgv所有值写入到sql 语句是INSERT INTO PenMaJiLu (printid,MoCode,SotSep, Batch, Sendtime, Printtime, Result) VALUES




        }


        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            bool notByMo = checkBox1.Checked;

            //textBox1.Enabled = !notByMo;
            //comboBox1.Enabled = !notByMo;

            if (notByMo)
            {
                //textBox1.Text = "";
                //comboBox1.Items.Clear();
                //comboBox1.Text = "";
                //textBox2.Text = "";
                AddLog("已切换为：不根据工单生产模式");
            }
            else
            {
                AddLog("已切换为：根据工单生产模式，请输入工单号");
            }
        }


        private async Task ExecutePrintAsync()
        {
            dataGridView1.Rows.Clear();

            // 获取订单相关信息
            string selectcombox = comboBox1.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(selectcombox)) return;

            string[] parts = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            string cinvcode = parts[0];
            string irowno = parts[1];

            if (!int.TryParse(textBox2.Text.Trim(), out int qty))
            {
                AddLog("请输入有效的数字作为打印数量");
                label4.Text = "打印状态：未启动";
                return;
            }

            if (qty <= 0)
            {
                AddLog("打印数量必须大于 0");
                label4.Text = "打印状态：未启动";
                return;
            }
            AddLog("开始打印");
            label4.Text = "打印状态：进行中~";


            Checksum checksum = new Checksum();

            for (int i = 0; i < qty; i++)
            {
                var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
                string checkvalue = checksum.Getinfo($"{cinvcode}_{datetimes}");
                string sentiment = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                AddLog($"发送第 {i + 1} 次数据");

                var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);

                string printtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                //AddLog(success ? $"接收返回：{result}" : $"接收失败：{result}");

                dataGridView1.Rows.Add(
                     i + 1,
                     textBox1.Text,
                     cinvcode,
                     irowno,
                     "0",
                     sentiment,
                     DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                     result
                 );
            }

            AddLog("喷码结束");
            label4.Text = "打印状态：未启动";

            SavePrintResultToDatabase();
        }




        private async Task ExecutePrintNoMoAsync()
        {
            dataGridView1.Rows.Clear();

            // 获取订单相关信息
            string selectcombox = comboBox1.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(selectcombox)) return;

            string[] parts = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            string cinvcode = parts[0];
            string irowno = parts[1];


            //int qty = int.TryParse(textBox2.Text, out int val) ? val : 0;
            if (!int.TryParse(textBox2.Text.Trim(), out int qty))
            {
                AddLog("请输入有效的数字作为打印数量");
                label4.Text = "打印状态：未启动";
                return;
            }

            if (qty <= 0)
            {
                AddLog("打印数量必须大于 0");
                label4.Text = "打印状态：未启动";
                return;
            }

            AddLog("开始打印（非工单模式）");
            label4.Text = "打印状态：进行中~";

            Checksum checksum = new Checksum();

            for (int i = 0; i < qty; i++)
            {
                var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
                string checkvalue = checksum.Getinfo("");  // 非工单模式传空字符串
                string sendTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                AddLog($"发送第 {i + 1} 次数据");

                var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);

                string printTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                dataGridView1.Rows.Add(
                    i + 1,         // 序号
                   textBox1.Text,
                     cinvcode,
                     irowno,          // 行号
                    "printnot",           // 批号
                    sendTime,
                    printTime,
                    result
                );
            }

            AddLog("喷码结束");
            label4.Text = "打印状态：未启动";

            SavePrintResultToDatabase();
        }

        private void SavePrintResultToDatabase()
        {

            if (dataGridView1.Rows.Count == 0)
            {
                AddLog("表格为空，无需保存");
                return;
            }

            try
            {
                int rowCount = dataGridView1.Rows.Count;
                if (rowCount == 0)
                {
                    AddLog("无打印记录需要保存");
                    return;
                }

                int successCount = 0;

                for (int i = 0; i < rowCount; i++)
                {
                    var row = dataGridView1.Rows[i];

                    string printid = row.Cells["Index"].Value?.ToString() ?? "0";
                    string MoCode = row.Cells["Mocode"].Value?.ToString() ?? "";
                    string SotSep = row.Cells["irowno"].Value?.ToString() ?? "";
                    string Batch = row.Cells["cBatch"].Value?.ToString() ?? "";
                    string Sendtime = row.Cells["SendTime"].Value?.ToString() ?? "";
                    string Printtime = row.Cells["PrintTime"].Value?.ToString() ?? "";
                    string Result = row.Cells["Result"].Value?.ToString() ?? "";

                    string sql = $@"
                INSERT INTO PenMaJiLu 
                (printid, MoCode, SotSep, Batch, Sendtime, Printtime, Result) 
                VALUES 
                ('{printid}', '{MoCode}', '{SotSep}', '{Batch}', '{Sendtime}', '{Printtime}', '{Result}')
            ";

                    int rowsAffected = DatabaseHelper.ExecuteNonQuery(sql);
                    if (rowsAffected > 0) successCount++;
                }

                AddLog($"打印记录写入数据库成功，共 {successCount} 条");
                dataGridView1.Rows.Clear();
                AddLog("打印记录已清空，防止重复保存");
            }
            catch (Exception ex)
            {
                AddLog($"保存记录到数据库失败：{ex.Message}");
            }
        }


        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            SavePrintResultToDatabase();
        }



    }
}
