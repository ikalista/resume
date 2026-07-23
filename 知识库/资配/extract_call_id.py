import re

# 读取文件
with open('log.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 提取包含 call_id 的行，并从 call_id 开始到行尾的内容
results = []
for line in lines:
    if 'call_id:' in line:
        # 找到 call_id: 的位置，提取从这里开始到行尾的内容
        start_pos = line.find('call_id:')
        extracted = line[start_pos:].strip()
        results.append(extracted)

# 输出结果，每个一行
print(f"找到 {len(results)} 条记录:")
print("-" * 80)
for result in results:
    print(result)

# 将结果保存到文件
with open('call_ids_output.txt', 'w', encoding='utf-8') as f:
    for result in results:
        f.write(result + '\n')

print("-" * 80)
print(f"结果已保存到 call_ids_output.txt")

