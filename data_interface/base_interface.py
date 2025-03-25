"""
数据接口模块 (Data Interface Module)

本模块定义了数据接口的基类和实现类。
数据接口用于从外部数据源获取材料结构数据和属性数据。

主要功能 (Main Features):
1. 定义数据接口基类
   - 指定接口方法
   - 规范数据格式

2. 实现MaterialProject接口
   - 从MaterialProject数据库获取数据
   - 处理API请求和响应

3. 扩展其他数据源接口
   - 如OQMD、AFLOW等
   - 统一数据访问方式

使用要求 (Requirements):
- Python 3.6+
- requests库

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

from abc import ABC, abstractmethod
import requests
from pymatgen.ext.matproj import MPRester

class DataInterface(ABC):
    """
    数据接口抽象基类 (Data Interface Abstract Base Class)
    
    定义了数据接口的通用方法,包括获取结构数据和材料属性数据。
    所有具体的数据接口实现类都需要继承该基类,并实现这些抽象方法。
    """
    
    @abstractmethod
    def get_structure(self, material_id: str):
        """
        获取材料结构数据
        
        from data source获取指定材料的结构数据,包括原子种类、位置、晶胞等。
        
        Parameters:
        -----------
        material_id : str
            材料的唯一标识符,如MaterialProject中的material_id
            
        Returns:
        --------
        dict
            包含材料结构数据的字典,格式为:
            {
                "material_id": "mp-123",
                "atoms": ["Si", "O"],
                "positions": [[0, 0, 0], [0.5, 0.5, 0.5]],
                "lattice": [[4.2, 0, 0], [0, 4.2, 0], [0, 0, 4.2]]
            }
        """
        pass
    
    @abstractmethod
    def get_properties(self, material_id: str):
        """
        获取材料属性数据
        
        from data source获取指定材料的各种属性数据,如形成能、带隙、弹性模量等。
        
        Parameters:
        -----------
        material_id : str
            材料的唯一标识符,如MaterialProject中的material_id
            
        Returns:
        --------
        dict
            包含材料属性数据的字典,格式为:
            {
                "material_id": "mp-123",
                "formation_energy": -1.234,
                "band_gap": 3.0,
                "elastic_modulus": 150.0
            }
        """
        pass

class MaterialProjectInterface(DataInterface):
    """
    MaterialProject数据接口 (MaterialProject Data Interface)
    
    实现了从MaterialProject数据库获取材料结构和属性数据的功能。
    
    Attributes:
        api_key (str): MaterialProject API密钥
    """
    
    def __init__(self, api_key: str):
        """
        初始化MaterialProject数据接口
        
        Parameters:
        -----------
        api_key : str
            MaterialProject API密钥,用于验证身份
        """
        self.api_key = api_key
        
    def get_structure(self, material_id: str):
        """
        获取MaterialProject中的材料结构数据
        
        通过MaterialProject API获取指定材料的结构数据。
        
        Parameters:
        -----------
        material_id : str
            MaterialProject中的材料ID,如"mp-123"
            
        Returns:
        --------
        dict
            包含材料结构数据的字典
        """
       try:
            with MPRester(self.api_key) as m:
                structure = m.get_structure_by_material_id(material_id)
            structure_data = {
                "material_id": material_id,
                "atoms": [str(site.specie) for site in structure.sites],
                "positions": [site.coords.tolist() for site in structure.sites],
                "lattice": structure.lattice.matrix.tolist()
            }
            return structure_data
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")
        return None
    
    def get_properties(self, material_id: str):
        """
        获取MaterialProject中的材料属性数据
        
        通过MaterialProject API获取指定材料的各种属性数据。
        
        Parameters:
        -----------
        material_id : str
            MaterialProject中的材料ID,如"mp-123"
            
        Returns:
        --------
        dict
            包含材料属性数据的字典
        """
       try:
            with MPRester(self.api_key) as m:
                doc = m.get_doc(material_id)
            property_data = {
                "material_id": material_id,
                "formation_energy": doc.get("formation_energy_per_atom", None),
                "band_gap": doc.get("band_gap", None),
                "elastic_modulus": doc.get("elasticity", {}).get("K_VRH", None)
            }
            return property_data
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")
        return None
