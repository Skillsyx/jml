import xml.etree.ElementTree as ET
import pandas as pd

# 载入 XML 文件
tree = ET.parse('巴贝兰\Printed Jobs20250618.xml')  # 请将此文件名改成你实际的文件名
root = tree.getroot()

# 提取所有 JmProductionDataToSerialize 节点
records = []
for item in root.findall('JmProductionDataToSerialize'):
    row = {}
    for child in item:
        # 如果标签重复，例如 ColorInkAcronym_0 ~ ColorInkAcronym_5，也会逐个作为列
        row[child.tag] = child.text
    records.append(row)

# 转为 DataFrame
df = pd.DataFrame(records)

# 保存为 Excel 和 CSV
df.to_excel('巴贝兰\output2.xlsx', index=False)
df.to_csv('巴贝兰\output2.csv', index=False, encoding='utf-8-sig')

print("✅ 转换完成，已保存为 output.xlsx 和 output.csv")
