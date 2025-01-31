"""
材料计算与分析系统可视化模块 (Material Analysis Visualization Module)

本模块提供系统的可视化界面，用于直观展示和分析计算结果。
集成了力场计算、缺陷检测、DFT计算和TEM模拟的可视化功能。

主要功能 (Main Features):
1. 力场计算结果可视化
   - 原子受力分布
   - 能量分布图
   - 应力张量展示
2. 缺陷分布显示
   - 空位缺陷标记
   - 间隙原子显示
   - 缺陷密度分布
3. DFT计算结果展示
   - 能带结构图
   - 态密度分布
   - 电子密度云图
4. TEM图像显示
   - HRTEM图像展示
   - STEM图像显示
   - 衬度分析

技术特点 (Technical Features):
- 交互式显示
- 多种图表类型
- 数据导出功能
- 实时更新

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

from force_field.force_field_calculator import ForceFieldCalculator
from defect_detection.defect_detector import DefectDetector
from visualization.tem_visualizer import TEMVisualizer  # 可视化组件
from dft_calculation.dft_calculator import DFTCalculator

def main():
    """
    可视化程序主入口
    
    创建示例材料结构，执行计算，并通过可视化界面展示结果。
    包括力场、缺陷、DFT和TEM的计算结果显示。
    
    工作流程:
    1. 创建材料结构
    2. 执行各项计算
    3. 可视化显示结果
    """
    # 创建示例材料结构数据
    structure_data = {
        'atoms': ['Si', 'Si', 'O', 'O'],  # 原子类型：硅和氧原子
        'positions': [                     # 原子位置（单位：埃米）
            [0.0, 0.0, 0.0],              # 第一个Si原子位置
            [1.5, 1.5, 1.5],              # 第二个Si原子位置
            [0.5, 0.5, 0.5],              # 第一个O原子位置
            [1.0, 1.0, 1.0]               # 第二个O原子位置
        ],
        'cell': [                         # 晶胞参数（单位：埃米）
            [3.0, 0.0, 0.0],              # x方向晶格向量
            [0.0, 3.0, 0.0],              # y方向晶格向量
            [0.0, 0.0, 3.0]               # z方向晶格向量
        ]
    }

    # 初始化计算模块
    ff_calculator = ForceFieldCalculator()    # 力场计算器
    defect_detector = DefectDetector()        # 缺陷检测器
    dft_calculator = DFTCalculator()          # DFT计算器

    # 执行力场计算
    ff_results = ff_calculator.calculate_force_field(structure_data)
    print("Force Field Results:", ff_results)  # 打印力场计算结果

    # 执行缺陷检测
    defects = defect_detector.detect_defects(structure_data)
    print("Detected Defects:", defects)        # 打印检测到的缺陷

    # 执行DFT计算
    dft_results = dft_calculator.run_dft(structure_data)
    print("DFT Results:", dft_results)         # 打印DFT计算结果

    # 初始化可视化器并显示结果
    visualizer = Visualization()
    
    # 显示力场计算结果
    visualizer.plot_force_field(
        ff_results['forces'],     # 原子受力数据
        ff_results['energy']      # 系统能量数据
    )
    
    # 显示缺陷分布
    visualizer.plot_defects(defects)  # 缺陷位置和类型
    
    # 显示DFT计算结果
    visualizer.plot_dft_results(
        dft_results['density'],   # 电子密度数据
        dft_results['energy']     # 能量数据
    )

if __name__ == "__main__":
    main()