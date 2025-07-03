using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public class PrinterClient
    {
        private string localIp;
        private string remoteIp;
        private int port;

        private UdpClient udpClient;
        private IPEndPoint printerEndpoint;
        private System.Windows.Forms.Timer reconnectTimer;
        private Form1 formRef; // 主窗体引用，用于输出日志

        public bool IsConnected => udpClient != null;

        public PrinterClient(Form1 form)
        {
            formRef = form;
        }

        // 初始化并尝试连接
        public void Initialize(string localIp, string remoteIp, int port)
        {
            this.localIp = localIp;
            this.remoteIp = remoteIp;
            this.port = port;

            TryConnect();

            reconnectTimer = new System.Windows.Forms.Timer();
            reconnectTimer.Interval = 5000; // 每5秒重连一次
            reconnectTimer.Tick += (s, e) =>
            {
                if (!IsConnected)
                    TryConnect();
            };
            reconnectTimer.Start();
        }

        private void TryConnect()
        {
            try
            {
                udpClient?.Close(); // 先关闭旧连接
                udpClient = new UdpClient(new IPEndPoint(IPAddress.Parse(localIp), 3000));
                printerEndpoint = new IPEndPoint(IPAddress.Parse(remoteIp), port);
                //formRef?.AddLog(udpClient.ToString());
                //formRef?.AddLog(printerEndpoint.ToString());

                formRef?.AddLog($"连接成功: {localIp} → {remoteIp}:{port}");
            }
            catch (Exception ex)
            {
                udpClient = null;
                formRef?.AddLog($"连接失败: {ex.Message}");
            }
        }

        public async Task<(bool success, string result)> SendAndReceiveAsync(string data, int timeoutMs = 60000)
        {
            if (udpClient == null)
            {
                formRef?.AddLog("未连接喷码机，无法发送数据");
                return (false, "未连接喷码机");
            }

            try
            {
                byte[] bytesToSend = Encoding.ASCII.GetBytes(data);
                await udpClient.SendAsync(bytesToSend, bytesToSend.Length, printerEndpoint);

                var deadline = DateTime.UtcNow.AddMilliseconds(timeoutMs);

                while (DateTime.UtcNow < deadline)
                {
                    // 使用超时控制等待返回
                    if (udpClient.Available > 0)
                    {
                        var result = await udpClient.ReceiveAsync();
                        string response = Encoding.ASCII.GetString(result.Buffer);

                        // 检查是否是我们期望的以 ~FF 开头的返回
                        if (response.StartsWith("~FF", StringComparison.OrdinalIgnoreCase))
                        {
                            return (true, response);
                        }
                        else
                        {
                            formRef?.AddLog($"忽略非目标返回: {response}");
                        }
                    }
                    else
                    {
                        await Task.Delay(50); // 等一会再查
                    }
                }

                formRef?.AddLog("等待 ~FF 返回超时");
                return (false, "超时未返回 ~FF");
            }
            catch (Exception ex)
            {
                formRef?.AddLog($"发送或接收出错: {ex.Message}");
                return (false, "通信异常");
            }
        }



        public void Dispose()
        {
            reconnectTimer?.Stop();
            reconnectTimer?.Dispose();
            udpClient?.Close();
            udpClient = null;
        }
    }
}
