namespace WinFormsApp1
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            textBox1 = new TextBox();
            comboBox1 = new ComboBox();
            textBox2 = new TextBox();
            checkBox1 = new CheckBox();
            label4 = new Label();
            button1 = new Button();
            dataGridView1 = new DataGridView();
            listBox1 = new ListBox();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(23, 35);
            label1.Name = "label1";
            label1.Size = new Size(80, 17);
            label1.TabIndex = 0;
            label1.Text = "生产订单号：";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(268, 35);
            label2.Name = "label2";
            label2.Size = new Size(68, 17);
            label2.TabIndex = 1;
            label2.Text = "产品信息：";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(23, 84);
            label3.Name = "label3";
            label3.Size = new Size(68, 17);
            label3.TabIndex = 2;
            label3.Text = "生产数量：";
            // 
            // textBox1
            // 
            textBox1.Location = new Point(97, 29);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(153, 23);
            textBox1.TabIndex = 4;
            // 
            // comboBox1
            // 
            comboBox1.FormattingEnabled = true;
            comboBox1.Location = new Point(330, 27);
            comboBox1.Name = "comboBox1";
            comboBox1.Size = new Size(216, 25);
            comboBox1.TabIndex = 5;
            comboBox1.DropDownStyleChanged += comboBox1_DropDownStyleChanged;
            // 
            // textBox2
            // 
            textBox2.Location = new Point(97, 78);
            textBox2.Name = "textBox2";
            textBox2.Size = new Size(153, 23);
            textBox2.TabIndex = 6;
            // 
            // checkBox1
            // 
            checkBox1.AutoSize = true;
            checkBox1.Font = new Font("Microsoft Tai Le", 9F, FontStyle.Bold);
            checkBox1.ForeColor = Color.Navy;
            checkBox1.Location = new Point(268, 78);
            checkBox1.Name = "checkBox1";
            checkBox1.Size = new Size(65, 20);
            checkBox1.TabIndex = 9;
            checkBox1.Text = "不喷码";
            checkBox1.UseVisualStyleBackColor = true;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(23, 129);
            label4.Name = "label4";
            label4.Size = new Size(43, 17);
            label4.TabIndex = 10;
            label4.Text = "label4";
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(45, 79, 140);
            button1.Font = new Font("Microsoft YaHei UI", 15F, FontStyle.Bold, GraphicsUnit.Point, 134);
            button1.ForeColor = SystemColors.ControlLightLight;
            button1.Location = new Point(635, 50);
            button1.Name = "button1";
            button1.Size = new Size(265, 51);
            button1.TabIndex = 11;
            button1.Text = "开始喷码";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Location = new Point(-1, 170);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.Size = new Size(952, 345);
            dataGridView1.TabIndex = 12;
            dataGridView1.CellContentClick += dataGridView1_CellContentClick;
            // 
            // listBox1
            // 
            listBox1.FormattingEnabled = true;
            listBox1.ItemHeight = 17;
            listBox1.Location = new Point(-1, 513);
            listBox1.Name = "listBox1";
            listBox1.Size = new Size(952, 123);
            listBox1.TabIndex = 13;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 17F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(951, 631);
            Controls.Add(listBox1);
            Controls.Add(dataGridView1);
            Controls.Add(button1);
            Controls.Add(label4);
            Controls.Add(checkBox1);
            Controls.Add(textBox2);
            Controls.Add(comboBox1);
            Controls.Add(textBox1);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Name = "Form1";
            Text = "肤感线喷码工具";
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private Label label2;
        private Label label3;
        private TextBox textBox1;
        private ComboBox comboBox1;
        private TextBox textBox2;
        private CheckBox checkBox1;
        private Label label4;
        private Button button1;
        private DataGridView dataGridView1;
        private ListBox listBox1;
    }
}
