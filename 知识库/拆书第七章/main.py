import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Binarizer
import time

class BernoulliRBM:
    """
    伯努利受限玻尔兹曼机（Bernoulli RBM）
    使用对比散度（Contrastive Divergence）算法进行训练
    """
    
    def __init__(self, n_visible=784, n_hidden=100, learning_rate=0.01, 
                 batch_size=100, n_iter=20, verbose=True):
        """
        初始化RBM
        
        参数:
        n_visible: 可见层单元数（MNIST: 28x28 = 784）
        n_hidden: 隐藏层单元数
        learning_rate: 学习率
        batch_size: 批次大小
        n_iter: 训练迭代次数
        verbose: 是否打印训练信息
        """
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.verbose = verbose
        
        # 初始化权重和偏置
        # 权重矩阵: W[i, j] 连接可见单元i和隐藏单元j
        self.W = np.random.normal(0, 0.01, (n_visible, n_hidden))
        # 可见层偏置
        self.v_bias = np.zeros(n_visible)
        # 隐藏层偏置
        self.h_bias = np.zeros(n_hidden)
        
        # 记录训练历史
        self.reconstruction_errors = []
        
    def sigmoid(self, x):
        """Sigmoid激活函数"""
        return 1 / (1 + np.exp(-np.clip(x, -250, 250)))
    
    def sample_hidden(self, v):
        """
        给定可见层状态，采样隐藏层状态
        v: 可见层状态 (batch_size, n_visible)
        返回: 隐藏层概率和采样结果
        """
        h_prob = self.sigmoid(np.dot(v, self.W) + self.h_bias)
        h_sample = (np.random.random(h_prob.shape) < h_prob).astype(np.float32)
        return h_prob, h_sample
    
    def sample_visible(self, h):
        """
        给定隐藏层状态，采样可见层状态
        h: 隐藏层状态 (batch_size, n_hidden)
        返回: 可见层概率和采样结果
        """
        v_prob = self.sigmoid(np.dot(h, self.W.T) + self.v_bias)
        v_sample = (np.random.random(v_prob.shape) < v_prob).astype(np.float32)
        return v_prob, v_sample
    
    def contrastive_divergence(self, v0, k=1):
        """
        对比散度算法（CD-k）
        v0: 初始可见层状态
        k: Gibbs采样的步数
        返回: 权重和偏置的梯度
        """
        batch_size = v0.shape[0]
        
        # 正向传播：v0 -> h0
        h0_prob, h0_sample = self.sample_hidden(v0)
        
        # Gibbs采样
        v_k = v0.copy()
        for _ in range(k):
            # h -> v
            v_k_prob, v_k_sample = self.sample_visible(h0_sample)
            v_k = v_k_sample
            # v -> h
            h_k_prob, h_k_sample = self.sample_hidden(v_k)
            h0_sample = h_k_sample
        
        # 计算梯度
        # 正相：<v0 * h0>
        pos_grad_W = np.dot(v0.T, h0_prob) / batch_size
        pos_grad_v = np.mean(v0, axis=0)
        pos_grad_h = np.mean(h0_prob, axis=0)
        
        # 负相：<v_k * h_k>
        h_k_prob_final, _ = self.sample_hidden(v_k)
        neg_grad_W = np.dot(v_k.T, h_k_prob_final) / batch_size
        neg_grad_v = np.mean(v_k, axis=0)
        neg_grad_h = np.mean(h_k_prob_final, axis=0)
        
        # 梯度更新
        grad_W = pos_grad_W - neg_grad_W
        grad_v = pos_grad_v - neg_grad_v
        grad_h = pos_grad_h - neg_grad_h
        
        return grad_W, grad_v, grad_h
    
    def reconstruct(self, v):
        """
        重构可见层数据
        v: 输入可见层状态
        返回: 重构的可见层概率
        """
        h_prob, _ = self.sample_hidden(v)
        v_recon_prob, _ = self.sample_visible(h_prob)
        return v_recon_prob
    
    def reconstruction_error(self, v):
        """
        计算重构误差（交叉熵）
        """
        v_recon = self.reconstruct(v)
        # 避免log(0)
        v_recon = np.clip(v_recon, 1e-7, 1 - 1e-7)
        error = -np.mean(np.sum(v * np.log(v_recon) + 
                                (1 - v) * np.log(1 - v_recon), axis=1))
        return error
    
    def fit(self, X):
        """
        训练RBM
        X: 训练数据 (n_samples, n_visible)，值应在[0, 1]之间
        """
        n_samples = X.shape[0]
        n_batches = n_samples // self.batch_size
        
        print(f"开始训练RBM...")
        print(f"可见层单元数: {self.n_visible}")
        print(f"隐藏层单元数: {self.n_hidden}")
        print(f"训练样本数: {n_samples}")
        print(f"批次大小: {self.batch_size}")
        print(f"迭代次数: {self.n_iter}")
        print("-" * 50)
        
        for epoch in range(self.n_iter):
            start_time = time.time()
            epoch_error = 0
            
            # 打乱数据
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            
            for batch_idx in range(n_batches):
                batch_start = batch_idx * self.batch_size
                batch_end = min(batch_start + self.batch_size, n_samples)
                v_batch = X_shuffled[batch_start:batch_end]
                
                # 对比散度更新
                grad_W, grad_v, grad_h = self.contrastive_divergence(v_batch, k=1)
                
                # 更新参数
                self.W += self.learning_rate * grad_W
                self.v_bias += self.learning_rate * grad_v
                self.h_bias += self.learning_rate * grad_h
                
                # 计算重构误差
                batch_error = self.reconstruction_error(v_batch)
                epoch_error += batch_error
            
            avg_error = epoch_error / n_batches
            self.reconstruction_errors.append(avg_error)
            
            elapsed_time = time.time() - start_time
            if self.verbose:
                print(f"Epoch {epoch+1}/{self.n_iter} - "
                      f"重构误差: {avg_error:.4f} - "
                      f"耗时: {elapsed_time:.2f}秒")
        
        print("-" * 50)
        print("训练完成！")
        return self


def load_mnist():
    """加载MNIST数据集"""
    print("正在加载MNIST数据集...")
    mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
    X, y = mnist.data, mnist.target.astype(int)
    
    # 归一化到[0, 1]
    X = X / 255.0
    
    # 二值化（可选，但RBM通常使用二值数据）
    binarizer = Binarizer(threshold=0.5)
    X_binary = binarizer.transform(X)
    
    print(f"数据集形状: {X_binary.shape}")
    print(f"标签范围: {y.min()} - {y.max()}")
    
    return X_binary, y


def visualize_weights(rbm, n_vis=100, save_path=None):
    """
    可视化RBM学习到的权重
    每个隐藏单元对应一个权重向量，可以看作是一个特征模板
    """
    print("\n可视化权重矩阵...")
    
    # 选择要可视化的隐藏单元数量
    n_hidden_to_show = min(n_vis, rbm.n_hidden)
    
    # 计算网格大小
    n_cols = 10
    n_rows = (n_hidden_to_show + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 1.5))
    axes = axes.flatten()
    
    for i in range(n_hidden_to_show):
        # 获取第i个隐藏单元的权重向量
        weight_vector = rbm.W[:, i]
        # 重塑为28x28图像
        weight_image = weight_vector.reshape(28, 28)
        
        axes[i].imshow(weight_image, cmap='gray', interpolation='nearest')
        axes[i].set_title(f'Hidden {i}', fontsize=8)
        axes[i].axis('off')
    
    # 隐藏多余的子图
    for i in range(n_hidden_to_show, len(axes)):
        axes[i].axis('off')
    
    plt.suptitle(f'RBM学习到的特征（前{n_hidden_to_show}个隐藏单元）', 
                 fontsize=14, y=0.995)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"权重可视化已保存到: {save_path}")
    
    plt.show()


def visualize_reconstruction(rbm, X_test, n_samples=10, save_path=None):
    """
    可视化重构效果
    显示原始图像和RBM重构后的图像
    """
    print("\n可视化重构效果...")
    
    # 随机选择一些样本
    indices = np.random.choice(X_test.shape[0], n_samples, replace=False)
    samples = X_test[indices]
    
    # 重构
    reconstructions = rbm.reconstruct(samples)
    
    fig, axes = plt.subplots(2, n_samples, figsize=(n_samples * 1.5, 3))
    
    for i in range(n_samples):
        # 原始图像
        axes[0, i].imshow(samples[i].reshape(28, 28), cmap='gray', 
                         interpolation='nearest')
        axes[0, i].set_title('原始', fontsize=10)
        axes[0, i].axis('off')
        
        # 重构图像
        axes[1, i].imshow(reconstructions[i].reshape(28, 28), cmap='gray', 
                          interpolation='nearest')
        axes[1, i].set_title('重构', fontsize=10)
        axes[1, i].axis('off')
    
    plt.suptitle('RBM重构效果对比', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"重构可视化已保存到: {save_path}")
    
    plt.show()


def visualize_training_history(rbm, save_path=None):
    """
    可视化训练历史（重构误差曲线）
    """
    print("\n可视化训练历史...")
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(rbm.reconstruction_errors) + 1), 
             rbm.reconstruction_errors, 'b-', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('重构误差', fontsize=12)
    plt.title('RBM训练过程 - 重构误差变化', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"训练历史已保存到: {save_path}")
    
    plt.show()


def visualize_hidden_activations(rbm, X_test, n_samples=20, save_path=None):
    """
    可视化隐藏层激活模式
    显示不同样本激活的隐藏单元
    """
    print("\n可视化隐藏层激活模式...")
    
    # 选择一些样本
    indices = np.random.choice(X_test.shape[0], n_samples, replace=False)
    samples = X_test[indices]
    
    # 获取隐藏层激活概率
    h_probs, _ = rbm.sample_hidden(samples)
    
    # 创建热图
    fig, ax = plt.subplots(figsize=(15, 8))
    im = ax.imshow(h_probs.T, cmap='hot', aspect='auto', interpolation='nearest')
    
    ax.set_xlabel('样本索引', fontsize=12)
    ax.set_ylabel('隐藏单元索引', fontsize=12)
    ax.set_title(f'隐藏层激活模式（{n_samples}个样本）', fontsize=14)
    
    plt.colorbar(im, ax=ax, label='激活概率')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"隐藏层激活可视化已保存到: {save_path}")
    
    plt.show()


def visualize_feature_evolution(rbm, X_sample, save_path=None):
    """
    可视化特征演化过程
    展示从随机初始化到训练后的权重变化
    """
    print("\n可视化特征演化...")
    
    # 选择一些隐藏单元进行可视化
    n_features = min(20, rbm.n_hidden)
    selected_indices = np.random.choice(rbm.n_hidden, n_features, replace=False)
    
    fig, axes = plt.subplots(2, n_features, figsize=(n_features * 1.2, 2.5))
    
    # 显示选中的隐藏单元权重
    for idx, hidden_idx in enumerate(selected_indices):
        weight_image = rbm.W[:, hidden_idx].reshape(28, 28)
        
        axes[0, idx].imshow(weight_image, cmap='gray', interpolation='nearest')
        axes[0, idx].set_title(f'H{hidden_idx}', fontsize=8)
        axes[0, idx].axis('off')
        
        # 显示这些隐藏单元对样本的响应
        h_prob, _ = rbm.sample_hidden(X_sample[:1])
        axes[1, idx].barh([0], [h_prob[0, hidden_idx]], height=0.5)
        axes[1, idx].set_xlim(0, 1)
        axes[1, idx].set_xticks([])
        axes[1, idx].set_yticks([])
        axes[1, idx].set_title(f'{h_prob[0, hidden_idx]:.2f}', fontsize=8)
    
    plt.suptitle('特征权重及其对样本的响应', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"特征演化可视化已保存到: {save_path}")
    
    plt.show()


def main():
    """主函数"""
    print("=" * 60)
    print("伯努利受限玻尔兹曼机 (Bernoulli RBM) - MNIST训练")
    print("=" * 60)
    
    # 1. 加载数据
    X, y = load_mnist()
    
    # 使用部分数据进行训练（加快速度，可根据需要调整）
    # 如果想使用全部数据，可以注释掉下面这行
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.9, random_state=42
    )
    print(f"\n训练集大小: {X_train.shape[0]}")
    print(f"测试集大小: {X_test.shape[0]}")
    
    # 2. 创建并训练RBM
    rbm = BernoulliRBM(
        n_visible=784,
        n_hidden=100,  # 可以调整隐藏单元数量
        learning_rate=0.01,
        batch_size=100,
        n_iter=20,  # 可以增加迭代次数以获得更好效果
        verbose=True
    )
    
    rbm.fit(X_train)
    
    # 3. 可视化结果
    print("\n" + "=" * 60)
    print("开始可视化...")
    print("=" * 60)
    
    # 可视化权重（学习到的特征）
    visualize_weights(rbm, n_vis=100, save_path='rbm_weights.png')
    
    # 可视化重构效果
    visualize_reconstruction(rbm, X_test, n_samples=10, 
                            save_path='rbm_reconstruction.png')
    
    # 可视化训练历史
    visualize_training_history(rbm, save_path='rbm_training_history.png')
    
    # 可视化隐藏层激活
    visualize_hidden_activations(rbm, X_test, n_samples=20, 
                                save_path='rbm_hidden_activations.png')
    
    # 可视化特征响应
    visualize_feature_evolution(rbm, X_test[:1], 
                              save_path='rbm_feature_response.png')
    
    print("\n" + "=" * 60)
    print("所有可视化完成！")
    print("=" * 60)
    
    # 打印一些统计信息
    print(f"\n最终重构误差: {rbm.reconstruction_errors[-1]:.4f}")
    print(f"权重矩阵统计:")
    print(f"  均值: {rbm.W.mean():.4f}")
    print(f"  标准差: {rbm.W.std():.4f}")
    print(f"  最大值: {rbm.W.max():.4f}")
    print(f"  最小值: {rbm.W.min():.4f}")


if __name__ == "__main__":
    main()

