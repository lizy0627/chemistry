"""
缓存管理模块 (Cache Management Module)

本模块提供计算结果的缓存管理功能。
通过将计算结果缓存到本地文件,可以避免重复计算,提高程序性能。

主要功能 (Main Features):
1. 缓存计算结果
   - 将结果保存到JSON文件
   - 文件名为计算ID

2. 获取缓存结果
   - 根据计算ID读取结果
   - 检查缓存是否过期

3. 清理过期缓存
   - 扫描缓存目录
   - 删除过期的缓存文件

4. 缓存大小统计
   - 统计缓存目录总大小
   - 方便进行缓存清理

使用要求 (Requirements):
- Python 3.6+

作者 (Author): [团队名称]
日期 (Date): [日期]
版本 (Version): 1.0
"""

import json
import os
from datetime import datetime, timedelta

class CacheManager:
    """
    缓存管理器类 (Cache Manager)
    
    负责管理计算结果的缓存,将结果保存到本地JSON文件,并提供读取和清理功能。
    
    Attributes:
        cache_dir (str): 缓存文件目录
    """
    
    def __init__(self, cache_dir='cache'):
        """
        初始化缓存管理器
        
        Parameters:
        -----------
        cache_dir : str
            缓存文件目录,默认为'cache'
        """
        self.cache_dir = cache_dir
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """
        确保缓存目录存在
        
        如果缓存目录不存在,则创建它。
        """
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def cache_results(self, calculation_id, results):
        """
        缓存计算结果
        
        将计算结果保存到以计算ID命名的JSON文件中。
        
        Parameters:
        -----------
        calculation_id : str
            计算任务的唯一标识符
        results : dict
            计算结果字典
        """
        cache_file = os.path.join(self.cache_dir, f'{calculation_id}.json')
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
            
    def get_results(self, calculation_id, max_age_days=30):
        """
        获取缓存的计算结果
        
        根据计算ID读取缓存的计算结果。如果缓存文件不存在或已过期,则返回None。
        
        Parameters:
        -----------
        calculation_id : str
            计算任务的唯一标识符
        max_age_days : int
            缓存的最大有效期,默认为30天
            
        Returns:
        --------
        dict or None
            缓存的计算结果字典,如果缓存无效则返回None
        """
        cache_file = os.path.join(self.cache_dir, f'{calculation_id}.json')
        
        if not os.path.exists(cache_file):
            return None
            
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        
        if datetime.now() - cache_time > timedelta(days=max_age_days):
            os.remove(cache_file)
            return None
            
        return cache_data['results']
        
    def clear_cache(self, max_age_days=None):
        """
        清理过期的缓存文件
        
        扫描缓存目录,删除超过指定天数的缓存文件。如果max_age_days为None,则清空所有缓存。
        
        Parameters:
        -----------
        max_age_days : int or None
            缓存文件的最大有效期,默认为None
        """
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            cache_file = os.path.join(self.cache_dir, filename)
            
            if max_age_days is None:
                os.remove(cache_file)
            else:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                
                if datetime.now() - cache_time > timedelta(days=max_age_days):
                    os.remove(cache_file)
            
    def get_cache_size(self):
        """
        获取缓存文件的总大小
        
        Returns:
        --------
        int
            缓存文件的总大小,单位为字节
        """
        total_size = 0
        
        for filename in os.listdir(self.cache_dir):
            cache_file = os.path.join(self.cache_dir, filename)
            total_size += os.path.getsize(cache_file)
            
        return total_size 