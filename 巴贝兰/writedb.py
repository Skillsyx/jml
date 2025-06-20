import xml.etree.ElementTree as ET
import pandas as pd
import pyodbc

# === 读取 XML ===
xml_path = r'巴贝兰\Printed Jobs20250618.xml'
tree = ET.parse(xml_path)
root = tree.getroot()

# === 提取数据 ===
records = []
for item in root.findall('JmProductionDataToSerialize'):
    row = {}
    for child in item:
        row[child.tag] = child.text.strip() if child.text is not None else None
    records.append(row)

df = pd.DataFrame(records)

# === 数据库连接配置 ===
server = '172.16.1.9'
database = 'yx_test'
username = 'sa'
password = 'Ks123456'

conn_str = (
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

table_name = 'JmProductionDataToSerialize_yx'

# === 插入数据 ===
error_rows = []
success_count = 0

print(f"📦 开始导入，共 {len(df)} 行数据...")

for index, row in df.iterrows():
    row_number = index + 1
    columns = ', '.join(f'[{col}]' for col in row.index)
    placeholders = ', '.join('?' for _ in row)
    values = [None if pd.isna(v) else v for v in row.values]

    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(sql, values)
        success_count += 1
        print(f"✅ 第 {row_number} 行写入成功")
    except Exception as e:
        print(f"❌ 第 {row_number} 行写入失败: {e}")
        error_row = row.to_dict()
        error_row['ErrorMessage'] = str(e)
        error_rows.append(error_row)

conn.commit()
cursor.close()
conn.close()

# === 写入失败记录 ===
if error_rows:
    df_error = pd.DataFrame(error_rows)
    df_error.to_excel('巴贝兰/插入失败记录.xlsx', index=False)
    print(f"⚠️ 导入完成，成功 {success_count} 行，失败 {len(error_rows)} 行。错误记录已保存到 插入失败记录.xlsx")
else:
    print(f"🎉 全部导入成功，共 {success_count} 行")
