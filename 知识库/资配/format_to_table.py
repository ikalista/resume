import re
import pandas as pd

# 读取提取的结果
with open('call_ids_output.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 解析每一行，提取 call_id, leader, members
data = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # 提取 call_id
    call_id_match = re.search(r'call_id:\s*([\d.]+)', line)
    call_id = call_id_match.group(1) if call_id_match else ''
    
    # 提取 leader
    leader_match = re.search(r'leader:\s*([\d.]+)', line)
    leader = leader_match.group(1) if leader_match else ''
    
    # 提取 members
    members_match = re.search(r'members:\s*(\[.*\])', line)
    members = members_match.group(1) if members_match else ''
    
    data.append({
        'call_id': call_id,
        'leader': leader,
        'members': members
    })

# 创建 DataFrame
df = pd.DataFrame(data)

# 添加 leader_url 列
df['leader_url'] = df['leader'].apply(
    lambda x: f'https://speaker-recognition-audio.oss-cn-shanghai-internal.aliyuncs.com/datasets/daily/cscrm/{x}.wav'
)

# 调整列顺序：call_id, leader, leader_url, members
df = df[['call_id', 'leader', 'leader_url', 'members']]

# 保存为 Excel 文件
df.to_excel('call_ids_table.xlsx', index=False, engine='openpyxl')
print(f"已处理 {len(df)} 条记录")
print("\n前5条数据预览:")
print(df.head())
print(f"\n结果已保存到 call_ids_table.xlsx")

# 同时保存为 CSV 文件（方便查看）
df.to_csv('call_ids_table.csv', index=False, encoding='utf-8-sig')
print(f"也保存了 CSV 格式: call_ids_table.csv")

