using Microsoft.Identity.Client;
using System;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        // ���캯������ʼ������ͽ���״̬

        private PrinterClient printerClient;
        private bool isDataSaved = false;

        public Form1()
        {
            InitializeComponent();
            InitializeStatus();
            printerClient = new PrinterClient(this); // ��������������������־���
            printerClient.Initialize("192.168.1.35", "192.168.1.30", 3000);
            //printerClient.Initialize("172.16.10.45", "172.16.10.37", 3000);
            this.textBox1.Leave += new System.EventHandler(this.textBox1_Leave);
            comboBox1.SelectedIndexChanged += comboBox1_SelectedIndexChanged;
            checkBox1.CheckedChanged += checkBox1_CheckedChanged;
            this.FormClosing += Form1_FormClosing;


        }



        // ��ǰʱ�䣨�ɹ������������ã�
        public string newdate => DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");


        // �����־���Զ��������ײ�,�Զ����
        public void AddLog(string msg)
        {

            if (listBox1.Items.Count >= 100)
            {
                listBox1.Items.Clear();
                listBox1.Items.Add($"{newdate} ��־�����");
            }

            listBox1.Items.Add($"{newdate} {msg}");
            listBox1.TopIndex = listBox1.Items.Count - 1;
        }

        // ��ʼ������״̬����־��DataGridView�нṹ
        private void InitializeStatus()
        {
            this.textBox1.Text = "SCDD24060876";

            label4.Text = "��ӡ״̬��δ����";
            listBox1.Items.Clear();
            AddLog("�����ɹ����ȴ�����...");

            dataGridView1.Columns.Clear();
            dataGridView1.Columns.Add("Index", "���");
            dataGridView1.Columns.Add("Mocode", "����������");
            dataGridView1.Columns.Add("Cinvcode", "��Ʒ����");
            dataGridView1.Columns.Add("irowno", "�к�");
            dataGridView1.Columns.Add("cBatch", "����");
            dataGridView1.Columns.Add("SendTime", "����ʱ��");
            dataGridView1.Columns.Add("PrintTime", "��ӡʱ��");
            dataGridView1.Columns.Add("Result", "���");

            dataGridView1.AllowUserToAddRows = false;
            dataGridView1.ReadOnly = true;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.RowHeadersVisible = false;

            AddLog("���������");
        }

        // ����һ���ֶδ洢 DataTable���������������ڲ� qty_b��
        private System.Data.DataTable comboData;

        // �� comboBox ʱͬ����������
        private void textBox1_Leave(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(textBox1.Text))
            {
                AddLog("�����빤����");
                return;
            }

            string sql = $"SELECT InvCode_b, SortSeq_b, qty_b FROM ufdata_008_2021..momlist_yx WHERE MoCode_a = '{textBox1.Text}'";

            try
            {
                var dt = DatabaseHelper.ExecuteQuery(sql);
                comboData = dt; // �������ݱ�

                comboBox1.Items.Clear();
                foreach (System.Data.DataRow row in dt.Rows)
                {
                    string item = $"{row["InvCode_b"]}::{row["SortSeq_b"]}";
                    comboBox1.Items.Add(item);
                }

                if (dt.Rows.Count > 0)
                {
                    comboBox1.SelectedIndex = 0;
                    //AddLog($"������ѯ�ɹ����� {dt.Rows.Count} ��");
                }
                else
                {
                    comboBox1.Items.Clear();
                    comboBox1.SelectedIndex = -1; // ȡ��ѡ����
                    comboBox1.Text = "";              // �����ʾ�ı�
                    textBox2.Text = "";
                    AddLog("�����ݣ�����������������");
                }




            }
            catch (Exception ex)
            {
                AddLog($"��ѯʧ��: {ex.Message}");
            }
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboData == null || comboBox1.SelectedIndex < 0) return;

            var row = comboData.Rows[comboBox1.SelectedIndex];
            decimal qty = Convert.ToDecimal(row["qty_b"]);
            textBox2.Text = Math.Floor(qty).ToString("0");
        }



        // DataGridView ��Ԫ�����¼�����δʹ�ã�
        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
        }

        // ���԰�ť����¼�����ȡѡ�еĲ�Ʒ������кţ�ִ�б���У��
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
        //            "����ӡ"
        //        );
        //    }



        //    string selectcombox = comboBox1.SelectedItem.ToString();
        //    string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
        //    string key = aaa[0];
        //    string value = aaa[1];

        //    Checksum checksum = new Checksum();
        //    string abcd = checksum.Getinfo("");

        //    AddLog(abcd); // ��� abcd �Ѵ���ʽ��ʱ�����ü� newdate
        //}

        


        //private async void buttontest_Click(object sender, EventArgs e)
        //{
        //    // У�� ComboBox �Ƿ�ѡ������Ŀ
        //    if (comboBox1.SelectedItem == null)
        //    {
        //        AddLog("����ѡ���Ʒ����");
        //        return;
        //    }

        //    string selectcombox = comboBox1.SelectedItem.ToString();
        //    string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
        //    string cinvcode = aaa[0];
        //    string irowno = aaa[1];

        //    Checksum checksum = new Checksum();

        //    // ��ǰʱ����Ϊ����ʱ��
        //    var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");

        //    // ���� CheckValue
        //    string checkvalue = checksum.Getinfo($"{cinvcode}_{datetimes}");

        //    AddLog($"�������ݣ�{checkvalue}");

        //    // ��¼����ʱ��
        //    var sendtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

        //    // ���Ͳ��ȴ�����
        //    var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);
        //    AddLog("fasong");

        //    // ��¼��ӡʱ��
        //    var printtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

        //    if (success)
        //    {
        //        AddLog($"���뷵�سɹ���{result}");
        //    }
        //    else
        //    {
        //        AddLog($"���뷵��ʧ�ܣ�{result}");
        //    }

        //    // ��������Ϣ + ������Ϣ��ʾ�������ݲ�д�� dgv���������־��
        //    AddLog($"����ʱ��: {sendtime}");
        //    AddLog($"��ӡʱ��: {printtime}");
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

            ////����Ĭ��ֵ
            //string selectcombox = comboBox1.SelectedItem.ToString();
            //string[] aaa = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            //string cinvcode = aaa[0];
            //string irowno = aaa[1];
            //Checksum checksum = new Checksum();

            ////����textb2�е�����ѭ��



            ////��ȡ�����ֵ checkvalue
            //var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
            //string checkvalue = checksum.Getinfo($"{cinvcode}" + $"_{datetimes}");


            ////���͸������checkvalue


            ////��¼����ʱ��
            //var sentiment = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");


            ////�ȴ��������ķ���ֵ



            ////��¼����ʱ��
            //var printime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");




            ////д��dgv ����� = ѭ����i�����ɶ����� = textbox1.text ,cinvcode = cinvcode,irowno = irowno,cbatch = 0,sentimet,printtime ,������



            ////ѭ����ɽ�dgv����ֵд�뵽sql �����INSERT INTO PenMaJiLu (printid,MoCode,SotSep, Batch, Sendtime, Printtime, Result) VALUES




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
                AddLog("���л�Ϊ�������ݹ�������ģʽ");
            }
            else
            {
                AddLog("���л�Ϊ�����ݹ�������ģʽ�������빤����");
            }
        }


        private async Task ExecutePrintAsync()
        {
            dataGridView1.Rows.Clear();

            // ��ȡ���������Ϣ
            string selectcombox = comboBox1.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(selectcombox)) return;

            string[] parts = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            string cinvcode = parts[0];
            string irowno = parts[1];

            if (!int.TryParse(textBox2.Text.Trim(), out int qty))
            {
                AddLog("��������Ч��������Ϊ��ӡ����");
                label4.Text = "��ӡ״̬��δ����";
                return;
            }

            if (qty <= 0)
            {
                AddLog("��ӡ����������� 0");
                label4.Text = "��ӡ״̬��δ����";
                return;
            }
            AddLog("��ʼ��ӡ");
            label4.Text = "��ӡ״̬��������~";


            Checksum checksum = new Checksum();

            for (int i = 0; i < qty; i++)
            {
                var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
                string checkvalue = checksum.Getinfo($"{cinvcode}_{datetimes}");
                string sentiment = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                AddLog($"���͵� {i + 1} ������");

                var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);

                string printtime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                //AddLog(success ? $"���շ��أ�{result}" : $"����ʧ�ܣ�{result}");

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

            AddLog("�������");
            label4.Text = "��ӡ״̬��δ����";

            SavePrintResultToDatabase();
        }




        private async Task ExecutePrintNoMoAsync()
        {
            dataGridView1.Rows.Clear();

            // ��ȡ���������Ϣ
            string selectcombox = comboBox1.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(selectcombox)) return;

            string[] parts = selectcombox.Split(new string[] { "::" }, StringSplitOptions.None);
            string cinvcode = parts[0];
            string irowno = parts[1];


            //int qty = int.TryParse(textBox2.Text, out int val) ? val : 0;
            if (!int.TryParse(textBox2.Text.Trim(), out int qty))
            {
                AddLog("��������Ч��������Ϊ��ӡ����");
                label4.Text = "��ӡ״̬��δ����";
                return;
            }

            if (qty <= 0)
            {
                AddLog("��ӡ����������� 0");
                label4.Text = "��ӡ״̬��δ����";
                return;
            }

            AddLog("��ʼ��ӡ���ǹ���ģʽ��");
            label4.Text = "��ӡ״̬��������~";

            Checksum checksum = new Checksum();

            for (int i = 0; i < qty; i++)
            {
                var datetimes = DateTime.Now.ToString("yyyy/MM/dd_HH:mm:ss");
                string checkvalue = checksum.Getinfo("");  // �ǹ���ģʽ�����ַ���
                string sendTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                AddLog($"���͵� {i + 1} ������");

                var (success, result) = await printerClient.SendAndReceiveAsync(checkvalue);

                string printTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");

                dataGridView1.Rows.Add(
                    i + 1,         // ���
                   textBox1.Text,
                     cinvcode,
                     irowno,          // �к�
                    "printnot",           // ����
                    sendTime,
                    printTime,
                    result
                );
            }

            AddLog("�������");
            label4.Text = "��ӡ״̬��δ����";

            SavePrintResultToDatabase();
        }

        private void SavePrintResultToDatabase()
        {

            if (dataGridView1.Rows.Count == 0)
            {
                AddLog("���Ϊ�գ����豣��");
                return;
            }

            try
            {
                int rowCount = dataGridView1.Rows.Count;
                if (rowCount == 0)
                {
                    AddLog("�޴�ӡ��¼��Ҫ����");
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

                AddLog($"��ӡ��¼д�����ݿ�ɹ����� {successCount} ��");
                dataGridView1.Rows.Clear();
                AddLog("��ӡ��¼����գ���ֹ�ظ�����");
            }
            catch (Exception ex)
            {
                AddLog($"�����¼�����ݿ�ʧ�ܣ�{ex.Message}");
            }
        }


        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            SavePrintResultToDatabase();
        }



    }
}
