"""
TEM模拟计算模块 (TEM Simulation Module)

本模块基于abTEM库实现透射电子显微镜(TEM)图像的模拟计算。
支持高分辨TEM(HRTEM)和扫描TEM(STEM)两种模式。

主要功能 (Main Features):
1. 电子波函数计算
   - 电压设置
   - 球差校正
   
2. 原子势场计算
   - 投影势场
   - 势场采样

3. 多切片模拟
   - 入射波设置
   - 出射波计算
   - 扫描模式支持

4. 图像模拟
   - HRTEM图像模拟
   - STEM图像模拟
   - 像差和噪声效应

5. 数据转换
   - 材料结构数据转ASE Atoms对象

使用要求 (Requirements):
- Python 3.6+
- ASE
- NumPy
- abTEM

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

from abtem import *
import numpy as np

class TEMCalculator:
    """
    TEM模拟计算器类 (TEM Simulation Calculator)
    
    执行TEM图像模拟计算的主要控制类。
    
    Attributes:
        voltage (float): 加速电压(单位:kV)
        waves (abtem.Waves): 电子波函数对象
        potential (abtem.Potential): 势场对象
        ctf (abtem.CTF): 对比度传递函数对象
    """
    
    def __init__(self, voltage=300):
        """
        初始化TEM计算器
        
        Parameters:
        -----------
        voltage : float
            电子束加速电压(单位:kV),默认为300kV
        """
        self.voltage = voltage
        self.waves = None
        self.potential = None
        
    def setup_microscope(self, aberrations=None):
        """
        设置显微镜参数
        
        根据提供的像差参数,创建对比度传递函数(CTF)对象。
        
        Parameters:
        -----------
        aberrations : dict
            包含像差系数的字典,默认为 {'C1': 1.0, 'C3': 1.0}
            
        Returns:
        --------
        None
        """
        if aberrations is None:
            aberrations = {'C1': 1.0, 'C3': 1.0}
            
        self.ctf = CTF(energy=self.voltage * 1e3,  # 转换为电子伏特
                      aperture=30,                 # 光阑大小(mrad)
                      **aberrations)               # 像差系数
    
    def calculate_potential(self, structure_data):
        """
        计算原子势场
        
        根据提供的材料结构数据,创建投影势场对象。
        
        Parameters:
        -----------
        structure_data : dict
            包含材料结构信息的字典
            
        Returns:
        --------
        abtem.Potential
            创建的势场对象
        """
        # 将structure_data转换为ASE Atoms对象
        atoms = self._convert_to_ase_atoms(structure_data)
        
        # 创建投影势场对象
        self.potential = Potential(atoms,
                                 sampling=0.05,        # 势场采样间距(埃)
                                 projection='infinite')  # 投影方式
        
        return self.potential
        
    def run_multislice(self, structure_data, scan_params=None):
        """
        执行多切片模拟计算
        
        根据提供的材料结构,计算电子波在样品中的传播。
        如果提供了扫描参数,则执行STEM模式模拟。
        
        Parameters:
        -----------
        structure_data : dict
            包含材料结构信息的字典
        scan_params : dict, optional
            STEM扫描参数,默认为None(即HRTEM模式)
            
        Returns:
        --------
        abtem.Waves or abtem.Measurement
            如果是HRTEM模式,返回出射波函数对象；
            如果是STEM模式,返回探测器测量结果对象。
        """
        # 设置入射波函数
        self.waves = Waves(energy=self.voltage * 1e3)  # 转换为电子伏特
        
        # 计算势场(如果之前没有计算过)
        if self.potential is None:
            self.calculate_potential(structure_data)
            
        # 执行多切片算法,计算出射波函数
        exit_waves = self.waves.multislice(self.potential)
        
        # 如果是STEM模式
        if scan_params:
            scan = GridScan(**scan_params)  # 创建扫描对象
            measurements = scan.scan(exit_waves)  # 执行扫描
            return measurements
            
        return exit_waves
    
    def simulate_stem(self, structure_data, scan_params):
        """
        模拟STEM图像
        
        根据提供的材料结构和扫描参数,执行STEM成像模拟。
        
        Parameters:
        -----------
        structure_data : dict
            包含材料结构信息的字典
        scan_params : dict
            STEM扫描参数
            
        Returns:
        --------
        numpy.ndarray
            模拟得到的STEM图像
        """
        # 设置环形暗场探测器
        detector = AnnularDetector(inner=70, outer=200)  # 内外接收角(mrad)
        
        # 执行STEM模拟
        measurements = self.run_multislice(structure_data, scan_params)
        
        # 获取探测器测量结果
        stem_image = detector.detect(measurements)
        
        return stem_image
    
    def simulate_hrtem(self, structure_data):
        """
        模拟HRTEM图像
        
        根据提供的材料结构,执行HRTEM成像模拟。
        
        Parameters:
        -----------
        structure_data : dict
            包含材料结构信息的字典
            
        Returns:
        --------
        numpy.ndarray
            模拟得到的HRTEM图像
        """
        # 执行多切片算法,计算出射波函数
        exit_waves = self.run_multislice(structure_data)
        
        # 应用对比度传递函数(CTF)
        image_waves = exit_waves.apply_ctf(self.ctf)
        
        # 计算图像强度
        hrtem_image = image_waves.intensity()
        
        return hrtem_image
    
    def _convert_to_ase_atoms(self, structure_data):
        """
        将材料结构字典转换为ASE Atoms对象
        
        Parameters:
        -----------
        structure_data : dict
            包含材料结构信息的字典
            
        Returns:
        --------
        ase.Atoms
            转换后的ASE Atoms对象
        """
        from ase import Atoms
        
        atoms = Atoms(
            symbols=structure_data['atoms'],
            positions=structure_data['positions'],
            cell=structure_data['cell'],
            pbc=True
        )
        
        return atoms 