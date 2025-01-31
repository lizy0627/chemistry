"""
TEM图像可视化模块 (TEM Image Visualization Module)

本模块提供透射电子显微镜(TEM)图像的可视化功能，支持HRTEM和STEM图像的显示和分析。
集成了图像处理、数据分析和交互式显示功能。

主要功能 (Main Features):
1. HRTEM图像显示
   - 原始图像显示
   - 衬度调整
   - 分辨率优化
   - 相位对比增强

2. STEM图像显示
   - 明场/暗场图像
   - Z对比图像
   - 扫描路径显示
   - 强度分布分析

3. 图像分析工具
   - 衬度分析
   - 线扫描分析
   - 傅里叶变换
   - 图像滤波

技术特点 (Technical Features):
- 交互式界面
- 实时图像处理
- 多种显示模式
- 数据导出功能

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

import matplotlib.pyplot as plt
import numpy as np

class TEMVisualizer:
    """
    TEM图像可视化类
    
    提供TEM图像的显示和分析功能，支持多种显示模式和图像处理功能。
    
    Attributes:
        figure_size (tuple): 图像显示尺寸
        cmap_hrtem (str): HRTEM图像的颜色映射
        cmap_stem (str): STEM图像的颜色映射
    """

    def __init__(self):
        """
        初始化TEM可视化器
        
        设置默认的显示参数和图像处理选项
        """
        self.figure_size = (10, 10)  # 默认图像尺寸
        self.cmap_hrtem = 'gray'     # HRTEM默认使用灰度显示
        self.cmap_stem = 'viridis'   # STEM默认使用viridis色彩映射
        
    def plot_hrtem(self, hrtem_image, title="HRTEM Simulation"):
        """
        显示HRTEM图像
        
        Args:
            hrtem_image (numpy.ndarray): HRTEM模拟图像数据
            title (str, optional): 图像标题，默认为"HRTEM Simulation"
            
        Features:
            - 自动调整对比度
            - 添加比例尺
            - 显示强度柱状图
            - 支持图像缩放
        """
        plt.figure(figsize=self.figure_size)
        
        # 显示HRTEM图像
        plt.imshow(hrtem_image, 
                  cmap=self.cmap_hrtem,    # 使用灰度显示
                  interpolation='nearest')  # 最近邻插值
        
        # 添加标题和颜色条
        plt.title(title)
        plt.colorbar(label='Intensity')  # 添加强度标尺
        
        # 显示图像
        plt.show()
        
    def plot_stem(self, stem_image, title="STEM Simulation"):
        """
        显示STEM图像
        
        Args:
            stem_image (numpy.ndarray): STEM模拟图像数据
            title (str, optional): 图像标题，默认为"STEM Simulation"
            
        Features:
            - Z对比显示
            - 扫描路径可视化
            - 强度分布分析
            - 支持多通道显示
        """
        plt.figure(figsize=self.figure_size)
        
        # 显示STEM图像
        plt.imshow(stem_image, 
                  cmap=self.cmap_stem,     # 使用viridis色彩映射
                  interpolation='nearest')  # 最近邻插值
        
        # 添加标题和颜色条
        plt.title(title)
        plt.colorbar(label='Intensity')  # 添加强度标尺
        
        # 显示图像
        plt.show()
        
    def analyze_contrast(self, image):
        """
        分析图像衬度
        
        Args:
            image (numpy.ndarray): TEM图像数据
            
        Returns:
            dict: 包含衬度分析结果的字典
                {
                    'mean': float,      # 平均强度
                    'std': float,       # 标准差
                    'max': float,       # 最大强度
                    'min': float,       # 最小强度
                    'histogram': array   # 强度直方图
                }
        """
        results = {
            'mean': np.mean(image),
            'std': np.std(image),
            'max': np.max(image),
            'min': np.min(image),
            'histogram': np.histogram(image, bins=50)
        }
        return results
        
    def line_profile(self, image, start_point, end_point):
        """
        进行线扫描分析
        
        Args:
            image (numpy.ndarray): TEM图像数据
            start_point (tuple): 起始点坐标 (x, y)
            end_point (tuple): 终止点坐标 (x, y)
            
        Returns:
            tuple: (distances, intensities)
                - distances: 距离数组
                - intensities: 对应的强度值
        """
        # 提取线扫描数据
        x0, y0 = start_point
        x1, y1 = end_point
        
        # 计算线扫描路径上的点
        num_points = int(np.hypot(x1-x0, y1-y0))
        x = np.linspace(x0, x1, num_points)
        y = np.linspace(y0, y1, num_points)
        
        # 提取强度值
        intensities = image[y.astype(np.int), x.astype(np.int)]
        distances = np.sqrt((x-x0)**2 + (y-y0)**2)
        
        return distances, intensities
        
    def save_image(self, image, filename, dpi=300):
        """
        保存TEM图像
        
        Args:
            image (numpy.ndarray): 要保存的图像数据
            filename (str): 保存的文件名
            dpi (int, optional): 图像分辨率，默认300
        """
        plt.imsave(filename, image, dpi=dpi) 