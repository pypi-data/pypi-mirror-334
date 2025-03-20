import os
import pathlib

class ModelManager:
    """模型文件管理器"""
    
    @staticmethod
    def get_model_path(model_name):
        """
        获取模型文件的完整路径
        参数:
            model_name: 模型文件名（不含路径）
        返回:
            模型文件的完整路径
        """
        # 获取当前文件所在目录
        current_dir = pathlib.Path(__file__).parent.absolute()
        # 模型文件目录
        model_dir = current_dir / 'models'
        # 模型文件完整路径
        model_path = model_dir / model_name
        
        if not model_path.exists():
            raise FileNotFoundError(f"模型文件 {model_name} 不存在，请确保模型文件已放置在正确位置")
        
        return str(model_path)

class ImageUtils:
    """图像处理工具类"""
    
    @staticmethod
    def resize_image(image, max_size=1024):
        """
        调整图像大小，保持宽高比
        参数:
            image: 输入图像
            max_size: 最大边长
        返回:
            调整后的图像
        """
        import cv2
        import numpy as np
        
        height, width = image.shape[:2]
        
        # 如果图像尺寸已经小于最大尺寸，直接返回
        if max(height, width) <= max_size:
            return image
        
        # 计算缩放比例
        scale = max_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 调整图像大小
        resized = cv2.resize(image, (new_width, new_height))
        return resized
    
    @staticmethod
    def draw_fps(image, fps):
        """
        在图像上绘制FPS
        参数:
            image: 输入图像
            fps: FPS值
        返回:
            添加FPS显示的图像
        """
        import cv2
        
        # 在左上角绘制FPS
        cv2.putText(image, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return image 