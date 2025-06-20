import pandas as pd
import pyodbc

# === 相对路径读取 CSV 文件 ===
csv_path = 'afge/JobHistory20250618.csv'  # ← 相对路径
df = pd.read_csv(csv_path, sep='|', dtype=str)

# === 删除空列（防止最后多出一个 NaN 列）===
df = df.dropna(axis=1, how='all')

# === 类型转换（时间 + 数值字段）===
for time_col in ['StartTime', 'EndTime']:
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')

float_fields = [
    'MediaThickness', 'MediaWidth', 'MediaLength', 'MediaSize',
    'ImageWith', 'ImageLength', 'RequestedCopyCount', 'GoodCopyCount', 'WasteCopyCount',
    'HeadGap', 'UVLeading', 'UVTrailing', 'MaskingValue', 'TransportAdjust',
    'ActualPrintTime', 'PercentagePrinted',
    'TotalInkGoodConsumption_Black', 'TotalWasteInkConsumption_Black', 'Density_Black',
    'TotalInkGoodConsumption_Cyan', 'TotalWasteInkConsumption_Cyan', 'Density_Cyan',
    'TotalInkGoodConsumption_Magenta', 'TotalWasteInkConsumption_Magenta', 'Density_Magenta',
    'TotalInkGoodConsumption_Yellow', 'TotalWasteInkConsumption_Yellow', 'Density_Yellow',
    'TotalInkGoodConsumption_LightCyan', 'TotalWasteInkConsumption_LightCyan', 'Density_LightCyan',
    'TotalInkGoodConsumption_LightBlack', 'TotalWasteInkConsumption_LightBlack', 'Density_LightBlack',
    'TotalInkGoodConsumption_White', 'TotalWasteInkConsumption_White', 'Density_White',
    'TotalInkGoodConsumption_Varnish', 'TotalWasteInkConsumption_Varnish', 'Density_Varnish'
]

for col in float_fields:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# === SQL Server 数据库连接配置 ===
server = '172.16.1.9'
database = 'yx_test'
username = 'sa'
password = 'Ks123456'

conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

table_name = 'afgePrintLog_yx'
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

# === 写入失败记录到 Excel ===
if error_rows:
    df_error = pd.DataFrame(error_rows)
    df_error.to_excel('afge/打印日志_插入失败记录.xlsx', index=False)
    print(f"⚠️ 成功 {success_count} 行，失败 {len(error_rows)} 行，失败记录已保存到 'afge/打印日志_插入失败记录.xlsx'")
else:
    print(f"🎉 所有数据导入成功，共 {success_count} 行")
