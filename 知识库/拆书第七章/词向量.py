# 词向量演进动态演示
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ---------------- 1. 定义4个词和5个阶段 ----------------
words = ['的', '是', '苹果', '水果']  # 停顿词、高频词、普通词、相关词
stages = ['裸词数/BOW', 'TF-IDF', 'BM25', 'Word2Vec']
n_stage = len(stages)

# 初始向量位置（3D空间）
# "的"：停顿词，高频，初始很长
# "是"：停顿词，高频，初始很长
# "苹果"：普通词，中等长度
# "水果"：与"苹果"相关，初始距离较远
vecs_initial = {
    '的': np.array([9.0, 1.0, 0.5]),      # 停顿词，很长
    '是': np.array([8.5, 1.5, 0.3]),     # 停顿词，很长
    '苹果': np.array([4.0, 3.0, 2.0]),    # 普通词
    '水果': np.array([2.0, 5.0, 4.0])    # 相关词，初始距离较远
}

# 每个阶段对每个词的压缩系数
# 阶段0 (BOW): 所有词保持原样
# 阶段1 (TF-IDF): 打压高频词（"的"、"是"被压缩）
# 阶段2 (BM25): 进一步打压长文档中的词（"的"、"是"进一步压缩）
# 阶段3 (Word2Vec): "苹果"和"水果"被拉近（语义相似）
shrink_factors = {
    '的': [1.0, 0.4, 0.2, 0.2],      # TF-IDF打压，BM25进一步打压
    '是': [1.0, 0.45, 0.25, 0.25],   # TF-IDF打压，BM25进一步打压
    '苹果': [1.0, 1.0, 1.0, 0.8],    # 保持，最后Word2Vec稍微调整
    '水果': [1.0, 1.0, 1.0, 0.7]     # 保持，最后Word2Vec拉近
}

# Word2Vec阶段：让"苹果"和"水果"在语义空间中靠近
# 计算"苹果"和"水果"的中点，然后让它们都向中点移动
apple_pos = vecs_initial['苹果']
fruit_pos = vecs_initial['水果']
midpoint = (apple_pos + fruit_pos) / 2

# Word2Vec阶段的目标位置
word2vec_targets = {
    '的': vecs_initial['的'] * shrink_factors['的'][3],
    '是': vecs_initial['是'] * shrink_factors['是'][3],
    '苹果': midpoint + (apple_pos - midpoint) * 0.3,  # 向中点移动70%
    '水果': midpoint + (fruit_pos - midpoint) * 0.3   # 向中点移动70%
}

# ---------------- 2. 生成关键帧 ----------------
keyframes = {word: [] for word in words}
for word in words:
    for stage_idx in range(n_stage):
        if stage_idx < n_stage - 1:
            # 前三个阶段：按压缩系数缩放
            keyframes[word].append(vecs_initial[word] * shrink_factors[word][stage_idx])
        else:
            # Word2Vec阶段：移动到目标位置
            keyframes[word].append(word2vec_targets[word])

# ---------------- 3. 生成平滑过渡的中间帧 ----------------
frames_per_stage = 40  # 每个阶段之间的过渡帧数
total_frames = (n_stage - 1) * frames_per_stage + 1

def interpolate(start, end, t):
    """线性插值，t从0到1"""
    return start + (end - start) * t

trajectories = {word: [] for word in words}
for word in words:
    for i in range(n_stage - 1):
        for j in range(frames_per_stage):
            t = j / frames_per_stage
            trajectories[word].append(interpolate(keyframes[word][i], keyframes[word][i+1], t))
    # 添加最后一帧
    trajectories[word].append(keyframes[word][-1])
    trajectories[word] = np.array(trajectories[word])

# ---------------- 4. 计算词之间的距离 ----------------
def euclidean_distance(v1, v2):
    """计算欧氏距离"""
    return np.linalg.norm(v1 - v2)

# 计算"苹果"和"水果"之间的距离变化
apple_fruit_distances = [euclidean_distance(trajectories['苹果'][i], trajectories['水果'][i]) 
                         for i in range(total_frames)]

# ---------------- 5. 建图 ----------------
fig = plt.figure(figsize=(18, 6))
ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

# 3D图设置
ax1.set_xlim(-1, 10)
ax1.set_ylim(-1, 6)
ax1.set_zlim(-1, 5)
ax1.set_box_aspect((11, 7, 6))
ax1.set_xlabel('X', fontsize=10)
ax1.set_ylabel('Y', fontsize=10)
ax1.set_zlabel('Z', fontsize=10)
ax1.set_title('词向量演进过程（3D）', fontsize=12, pad=10)
ax1.view_init(elev=20, azim=45)
ax1.grid(True, alpha=0.3)

# 向量长度变化图
ax2.set_xlim(0, total_frames)
ax2.set_xlabel('帧数', fontsize=10)
ax2.set_ylabel('向量长度', fontsize=10)
ax2.set_title('向量长度变化（算法升级效果）', fontsize=12)
ax2.grid(True, alpha=0.3)

# 词间距离变化图
ax3.set_xlim(0, total_frames)
ax3.set_xlabel('帧数', fontsize=10)
ax3.set_ylabel('欧氏距离', fontsize=10)
ax3.set_title('"苹果"与"水果"的距离变化', fontsize=12)
ax3.grid(True, alpha=0.3)

# 颜色映射
colors = {
    '的': 'red',
    '是': 'orange',
    '苹果': 'green',
    '水果': 'blue'
}

# 初始化箭头和轨迹线
quivers = {}
lines = {}
for word in words:
    quivers[word] = ax1.quiver([0], [0], [0], 
                               [trajectories[word][0][0]], 
                               [trajectories[word][0][1]], 
                               [trajectories[word][0][2]],
                               color=colors[word], arrow_length_ratio=.08, lw=2.5)
    lines[word], = ax2.plot([], [], color=colors[word], linewidth=2, 
                           label=f'"{word}"', marker='o', markersize=4)

# 词间距离线
dist_line, = ax3.plot([], [], 'purple', linewidth=2, label='苹果-水果距离', marker='o', markersize=4)
ax3.legend(loc='upper right', fontsize=9)
ax2.legend(loc='upper right', fontsize=9)

# 阶段文字
stage_txt = ax1.text2D(0.5, 0.95, '', transform=ax1.transAxes, 
                       ha='center', fontsize=16, weight='bold',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
info_txt = ax1.text2D(0.5, 0.88, '', transform=ax1.transAxes, 
                      ha='center', fontsize=10, style='italic')

# 存储轨迹点（用于绘制轨迹线）
traced_points = {word: [] for word in words}
# 词标签文本对象（存储以便清除）
word_labels = {word: None for word in words}
# 轨迹线对象（存储以便清除）
trajectory_lines = {word: None for word in words}

def update(frame):
    global quivers, traced_points, word_labels, trajectory_lines
    
    # 移除旧箭头、旧标签和旧轨迹线
    for word in words:
        quivers[word].remove()
        if word_labels[word] is not None:
            word_labels[word].remove()
        if trajectory_lines[word] is not None:
            trajectory_lines[word].remove()
    
    # 添加轨迹点
    for word in words:
        traced_points[word].append(trajectories[word][frame])
        if len(traced_points[word]) > 20:  # 只保留最近20帧，减少残影
            traced_points[word] = traced_points[word][-20:]
    
    # 画新箭头并创建新标签
    for word in words:
        vec = trajectories[word][frame]
        quivers[word] = ax1.quiver([0], [0], [0], 
                                   [vec[0]], [vec[1]], [vec[2]],
                                   color=colors[word], arrow_length_ratio=.08, lw=2.5)
        
        # 创建词标签
        word_labels[word] = ax1.text(vec[0]*1.1, vec[1]*1.1, vec[2]*1.1, f'"{word}"', 
                                     fontsize=9, color=colors[word], weight='bold')
    
    # 重新绘制轨迹线（只显示最近的轨迹）
    for word in words:
        if len(traced_points[word]) > 1:
            traced_arr = np.array(traced_points[word])
            trajectory_lines[word], = ax1.plot(traced_arr[:, 0], traced_arr[:, 1], traced_arr[:, 2], 
                                              color=colors[word], alpha=0.3, linewidth=1)
    
    # 动态旋转视角
    ax1.view_init(elev=20, azim=45 + frame * 0.3)
    
    # 更新阶段名
    stage_idx = min(frame // frames_per_stage, n_stage - 1)
    stage_txt.set_text(f'阶段: {stages[stage_idx]}')
    
    # 更新信息文字
    if stage_idx == 0:
        info = 'BOW: 停顿词"的"、"是"很长'
    elif stage_idx == 1:
        info = 'TF-IDF: 打压高频词，"的"、"是"被压缩'
    elif stage_idx == 2:
        info = 'BM25: 进一步打压长文档中的词'
    else:
        info = 'Word2Vec: "苹果"和"水果"语义拉近'
    info_txt.set_text(info)
    
    # 更新向量长度曲线
    for word in words:
        lengths = [np.linalg.norm(trajectories[word][i]) for i in range(frame + 1)]
        lines[word].set_data(range(frame + 1), lengths)
    
    # 更新词间距离曲线
    dist_line.set_data(range(frame + 1), apple_fruit_distances[:frame + 1])
    
    # 动态调整Y轴范围
    if frame > 0:
        all_lengths = []
        for word in words:
            all_lengths.extend([np.linalg.norm(trajectories[word][i]) for i in range(frame + 1)])
        if all_lengths:
            ax2.set_ylim(0, max(all_lengths) * 1.1)
        
        if apple_fruit_distances[:frame + 1]:
            ax3.set_ylim(0, max(apple_fruit_distances[:frame + 1]) * 1.1)
    
    label_objs = [v for v in word_labels.values() if v is not None]
    line_objs = [v for v in trajectory_lines.values() if v is not None]
    return list(quivers.values()) + list(lines.values()) + line_objs + \
           label_objs + [stage_txt, info_txt, dist_line]

ani = animation.FuncAnimation(fig, update, frames=total_frames, 
                              interval=60, repeat=True, blit=False)
plt.tight_layout()
plt.show()
