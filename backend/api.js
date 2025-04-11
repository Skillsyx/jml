// api.js

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const sql = require('mssql');

const app = express();
const port = 9889;

// 允许跨域请求
app.use(cors());

// 使用 body-parser 解析 JSON 请求体
app.use(bodyParser.json());

// SQL Server 连接参数（根据实际情况修改）
const dbConfig = {
  user: 'sa',
  password: 'Ks123456',
  server: '172.16.1.9',
  database: 'ufdata_008_2021',
  options: {
    encrypt: false,
    enableArithAbort: true
  }
};

// 定义查询 API 接口
app.post('/api/getTableData', async (req, res) => {
  try {
    // 从请求体中获取参数
    const { ordercode, startnum, endnum, company } = req.body;
    if (!ordercode || !startnum || !endnum || !company) {
      return res.status(400).send("缺少必要的查询参数");
    }

    // 连接数据库
    await sql.connect(dbConfig);

    // 定义查询语句变量
    let query = "";

    if (company === '金米龙（江苏）科技材料有限公司') {
      query = `
        SELECT ISNULL(cBusCode, cOrderCode) AS code,
               CAST(cWhCode AS NVARCHAR) + ' / ' + CAST(cPosName AS NVARCHAR) AS wp,
               ABS(iQuantity) AS iQuantity,
               cComUnitName,
               cBatch,
               cInvCode,
               cWhCode,
               cPosName,
               autoid,
               cinvname
        FROM ufdata_001_2021..rdall_yx
        WHERE (class IN ('01','08','10','41','32','11')
              AND (class <> '11' OR (class = '11' AND iQuantity < 0))
              AND (class <> '32' OR (class = '32' AND iQuantity < 0))
              AND (class <> '41' OR (class = '41' AND brdflag = 1)))
          AND CASE WHEN class = '08' THEN cBusCode ELSE cCode END = '${ordercode} '
          AND irowno >= ${startnum}
          AND irowno <= ${endnum}
      `;
    } else {
      query = `
        SELECT ISNULL(cBusCode, cOrderCode) AS code,
               CAST(cWhCode AS NVARCHAR) + ' / ' + CAST(cPosName AS NVARCHAR) AS wp,
               ABS(iQuantity) AS iQuantity,
               cComUnitName,
               cBatch,
               cInvCode,
               cWhCode,
               cPosName,
               autoid,
               cinvname
        FROM ufdata_008_2021..rdall_yx
        WHERE (class IN ('01','08','10','41','32','11')
              AND (class <> '11' OR (class = '11' AND iQuantity < 0))
              AND (class <> '32' OR (class = '32' AND iQuantity < 0))
              AND (class <> '41' OR (class = '41' AND brdflag = 1)))
          AND CASE WHEN class = '08' THEN cBusCode ELSE cCode END = '${ordercode} '
          AND irowno >= ${startnum}
          AND irowno <= ${endnum}
      `;
    }

    // 打印查询语句到后端控制台（调试用）
    console.log("执行的 SQL 查询语句：", query);

    // 执行查询
    const result = await new sql.Request()
      .input("ordercode", sql.VarChar, ordercode)
      .input("startnum", sql.Int, startnum)
      .input("endnum", sql.Int, endnum)
      .input("company", sql.VarChar, company)
      .query(query);

    // 返回查询结果，同时附带查询语句用于调试（生产中建议移除 query 字段）
    res.json(result.recordset || []);

  } catch (err) {
    console.error("查询错误:", err);
    res.status(500).send(err.message);
  }
});

app.listen(port, () => {
  console.log(`API server listening at http://localhost:${port}`);
});
