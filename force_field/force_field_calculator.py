"""
力场计算模块 (Force Field Calculation Module)

本模块使用经典力场方法计算材料的结构性质。
主要使用LAMMPS软件包进行分子动力学模拟。

主要功能 (Main Features):
1. 结构优化
   - 能量最小化
   - 应力张量优化
   - 晶格参数优化

2. 力场计算
   - 能量计算
   - 力计算
   - 应力计算

3. 接口转换
   - ASE Atoms 转换
   - Pymatgen Structure 转换

使用要求 (Requirements):
- Python 3.6+
- ASE
- Pymatgen
- LAMMPS

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

import numpy as np
from ase.calculators.lammps import LAMMPS
from ase.io import write, read
from ase import units

class ForceFieldCalculator:
    """
    力场计算器类 (Force Field Calculator)
    
    使用LAMMPS执行分子动力学模拟,计算材料的结构性质。
    
    Attributes:
        potential_type (str): 力场类型
        calculator (LAMMPS): LAMMPS计算器对象
    """
    
    def __init__(self, potential_type='Tersoff'):
        """
        初始化力场计算器
        
        Parameters:
        -----------
        potential_type : str
            力场类型,默认为Tersoff势
        """
        self.potential_type = potential_type
        self.calculator = None
    
    def setup_calculator(self):
        """
        设置LAMMPS计算器
        
        根据力场类型,设置LAMMPS的势函数和参数。
        """
        cmds = []
        if self.potential_type == 'Tersoff':
            cmds = [
                'pair_style tersoff',
                'pair_coeff * * Si.tersoff Si'
            ]
        
        self.calculator = LAMMPS(
            command='lmp_mpi',
            tmp_dir='tmp',
            keep_tmp_files=False,
            specorder=['Si', 'O'],
            always_triclinic=True,
            commands=cmds
        )
    
    def calculate_force_field(self, structure_data):
        """
        执行力场计算
        
        使用LAMMPS计算材料结构的能量、力和应力等性质。
        
        Parameters:
        -----------
        structure_data: dict
            包含原子结构信息的字典
        
        Returns:
        --------
        dict
            包含计算结果的字典,包括:
            - energy (float): 体系总能量
            - forces (array): 每个原子上的力
            - stress (array): 应力张量
            - optimized_structure (dict): 优化后的结构
        """
        # 将结构字典转换为ASE Atoms对象
        atoms = self._convert_to_ase_atoms(structure_data)
        
        # 设置LAMMPS计算器
        if self.calculator is None:
            self.setup_calculator()
        atoms.calc = self.calculator
        
        try:
            # 计算能量、力和应力
            energy = atoms.get_potential_energy()
            forces = atoms.get_forces()
            stress = atoms.get_stress()
            
            # 结构优化
            optimized_structure = self._optimize_structure(atoms)
            
            return {
                "energy": energy,
                "forces": forces,
                "stress": stress,
                "optimized_structure": {
                    "positions": optimized_structure.positions.tolist(),
                    "cell": optimized_structure.cell.tolist()
                }
            }
            
        except Exception as e:
            print(f"力场计算出错: {str(e)}")
            return None
    
    def _optimize_structure(self, atoms):
        """
        结构优化
        
        使用BFGS算法优化材料结构,得到能量最小构型。
        
        Parameters:
        -----------
        atoms : ase.Atoms
            ASE原子对象
            
        Returns:
        --------
        ase.Atoms
            优化后的原子对象
        """
        from ase.optimize import BFGS
        
        optimizer = BFGS(atoms)
        optimizer.run(fmax=0.05)
        
        return atoms
    
    def _convert_to_ase_atoms(self, structure_data):
        """
        将结构字典转换为ASE原子对象
        
        Parameters:
        -----------
        structure_data : dict
            包含原子结构信息的字典
            
        Returns:
        --------
        ase.Atoms
            转换后的ASE原子对象
        """
        from ase import Atoms
        
        atoms = Atoms(
            symbols=structure_data['atoms'],
            positions=structure_data['positions'],
            cell=structure_data['cell'],
            pbc=True
        )
        
        return atoms