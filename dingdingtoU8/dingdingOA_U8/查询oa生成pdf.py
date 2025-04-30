import json
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Spacer, Paragraph
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class DingTalkAPI:
    """ 钉钉 API 封装 """

    def __init__(self, corp_id, corp_secret):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """ 获取 Access Token """
        url = "https://oapi.dingtalk.com/gettoken"
        params = {"appkey": self.corp_id, "appsecret": self.corp_secret}
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("access_token") if data.get("errcode") == 0 else None

    def get_approval_instance(self, process_instance_id):
        """ 查询单个审批实例数据 """
        url = "https://oapi.dingtalk.com/topapi/processinstance/get"
        headers = {"Content-Type": "application/json"}
        params = {"access_token": self.access_token}
        data = {"process_instance_id": process_instance_id}

        response = requests.post(url, headers=headers, params=params, json=data)
        return response.json()

def generate_pdf(data, filename="采购订单.pdf"):
    """ 生成审批单 PDF（表格样式 + Paragraph 自动换行 + 标题） """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    # **注册 Windows 自带宋体**
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))

    # **准备基本段落样式，支持中文自动换行**
    stylesheet = getSampleStyleSheet()
    style_cjk = stylesheet["BodyText"]
    style_cjk.fontName = "SimSun"
    style_cjk.fontSize = 10
    style_cjk.leading = 12
    style_cjk.wordWrap = 'CJK'

    # **准备标题样式：更大字体、居中**
    style_title = ParagraphStyle(
        name="TitleStyle",
        parent=style_cjk,
        fontSize=16,
        leading=20,
        alignment=1  # 1 表示居中
    )

    # ========== 0. 标题 ==========
    title_para = Paragraph("采购订单审批", style_title)
    elements.append(title_para)
    elements.append(Spacer(1, 20))  # 标题下留白

    # ========== 1. 基本信息表格 ==========
    basic_info_data = [
        ["审批编号", make_paragraph(data.get("process_instance_id", ""), style_cjk)],
        ["创建人", make_paragraph(data.get("originator_userid", ""), style_cjk)],
        ["创建人部门", make_paragraph(data.get("originator_dept_name", ""), style_cjk)],
        ["业务类型", make_paragraph(get_value(data, "业务类型"), style_cjk)],
        ["单据编号", make_paragraph(get_value(data, "单据编号"), style_cjk)],
        ["单据日期", make_paragraph(get_value(data, "单据日期"), style_cjk)],
        ["供应商名称", make_paragraph(get_value(data, "供应商名称"), style_cjk)],
        ["收货地址", make_paragraph(get_value(data, "收货地址"), style_cjk)],
        ["部门", make_paragraph(get_value(data, "部门"), style_cjk)],
        ["业务员", make_paragraph(get_value(data, "业务员"), style_cjk)],
        ["币种", make_paragraph(get_value(data, "币种"), style_cjk)],
        ["制单人", make_paragraph(get_value(data, "制单人"), style_cjk)]
    ]
    basic_table = Table(basic_info_data, colWidths=[150, 350])
    basic_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "SimSun"),
    ]))
    elements.append(basic_table)
    elements.append(Spacer(1, 10))

    # ========== 2. 子表单（表格） ==========
    sub_form_values = get_value(data, "表格", default="[]")
    sub_form_data = json.loads(sub_form_values) if sub_form_values else []
    if sub_form_data:
        # **表头**
        table_header = [
            "销售订单号","存货名称","数量","含税单价","无税单价","税率","无税金额","税额","价税合计","交期"
        ]
        # 转换为 Paragraph
        header_row = [make_paragraph(h, style_cjk) for h in table_header]
        table_data = [header_row]

        # **解析子表单数据**
        for row in sub_form_data:
            row_values = {item["label"]: item["value"] for item in row["rowValue"]}
            row_cells = [
                make_paragraph(row_values.get("销售订单号", ""), style_cjk),
                make_paragraph(row_values.get("存货名称", ""), style_cjk),
                make_paragraph(row_values.get("数量", ""), style_cjk),
                make_paragraph(row_values.get("含税单价", ""), style_cjk),
                make_paragraph(row_values.get("无税单价", ""), style_cjk),
                make_paragraph(row_values.get("税率", ""), style_cjk),
                make_paragraph(row_values.get("无税金额", ""), style_cjk),
                make_paragraph(row_values.get("税额", ""), style_cjk),
                make_paragraph(row_values.get("价税合计", ""), style_cjk),
                make_paragraph(row_values.get("交期", ""), style_cjk)
            ]
            table_data.append(row_cells)

        order_table = Table(table_data, colWidths=[50]*10)  # 10列×50=500总宽
        order_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "SimSun"),
        ]))
        elements.append(order_table)
        elements.append(Spacer(1, 10))

    # ========== 3. 总金额表格 ==========
    total_amount = get_value(data, "总金额")
    total_table_data = [
        ["总金额", make_paragraph(total_amount, style_cjk)]
    ]
    total_table = Table(total_table_data, colWidths=[150, 350])
    total_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "SimSun"),
    ]))
    elements.append(total_table)

    doc.build(elements)
    print(f"✅ 审批单已导出为 {filename}")

def get_value(data, field_name, default=""):
    """ 从表单项中获取指定字段的值 """
    for item in data.get("form_component_values", []):
        if item.get("name") == field_name:
            return item.get("value", default)
    return default

def make_paragraph(text, style):
    """ 将文本转换为支持自动换行的 Paragraph """
    return Paragraph(text, style)

# =============== 测试调用 ===============
if __name__ == "__main__":
    ding_api = DingTalkAPI(
        "dingg4komkiirlidfnag",
        "WcrjxsKA8Jay95sbge_wF5njoK7f6WR7CYqpMswYbIZwv_45xLDq2ZDzjAMWCS0U"
    )
    process_instance_id = "H5aBCJ4hSVW7Tmq485KLSQ04501741306798"
    instance_data = ding_api.get_approval_instance(process_instance_id)

    if instance_data.get("errcode") == 0:
        generate_pdf(instance_data["process_instance"], filename="采购订单.pdf")
    else:
        print(f"❌ 获取审批数据失败: {instance_data.get('errmsg')}")
