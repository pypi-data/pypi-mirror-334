import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from .utils import ModelManager
import time
import pathlib
from mediapipe.framework.formats import landmark_pb2
# 导入资源管理模块
from .resource_manager import register_resource, unregister_resource

class BaseMediaPipeError(Exception):
    """MediaPipe基础错误类"""
    pass

class BaseMediaPipeDetector:
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5,
                 enable_gpu=False,  # 是否启用GPU加速
                 result_callback=None):  # 可选的回调函数
        """
        MediaPipe检测器基类
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小跟踪置信度
            enable_gpu: 是否启用GPU加速
            result_callback: 可选的回调函数，用于实时流模式
        """
        try:
            # 资源管理
            self._latest_result = None
            self._latest_frame = None
            self._fps_counter = 0
            self._fps = 0
            self._start_time = time.time()
            self._fps_avg_frame_count = 10
            
            # 基础参数设置
            self.min_detection_confidence = min_detection_confidence
            self.min_tracking_confidence = min_tracking_confidence
            self.result_callback = result_callback
            self.enable_gpu = enable_gpu
            
            # 根据输入源确定模式
            self.running_mode = self._determine_mode(input_source)
            
            # 注册到资源管理器
            register_resource(self)
            
            # 初始化检测器
            self._initialize_detector()
            
            # 如果是图片模式，立即处理输入图片
            if input_source is not None:
                self._process_input_source(input_source)
                
        except Exception as e:
            raise BaseMediaPipeError(f"初始化失败: {str(e)}")
            
    def _determine_mode(self, input_source):
        """根据输入源确定运行模式"""
        if input_source is None:
            return vision.RunningMode.LIVE_STREAM
            
        if isinstance(input_source, (str, pathlib.Path)):
            path = pathlib.Path(input_source)
            if not path.exists():
                raise FileNotFoundError(f"图片文件不存在: {path}")
            if not path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'}:
                raise ValueError(f"不支持的图片格式: {path.suffix}")
                
        elif isinstance(input_source, np.ndarray):
            if len(input_source.shape) != 3:
                raise ValueError("输入图像必须是3通道图像")
                
        else:
            raise ValueError(f"不支持的输入类型: {type(input_source)}")
            
        return vision.RunningMode.IMAGE
            
    def _save_result(self, result, output_image, timestamp_ms):
        """内部回调函数，用于处理异步检测结果"""
        # 更新FPS计数
        if self._fps_counter % self._fps_avg_frame_count == 0:
            self._fps = self._fps_avg_frame_count / (time.time() - self._start_time)
            self._start_time = time.time()
        
        self._fps_counter += 1
        self._latest_result = result
        
        if self.result_callback:
            self.result_callback(result, output_image, timestamp_ms)
            
    def _initialize_detector(self):
        """初始化检测器 - 子类必须实现此方法"""
        raise NotImplementedError("子类必须实现_initialize_detector方法")
            
    def _process_input_source(self, input_source):
        """处理输入源"""
        try:
            if isinstance(input_source, (str, pathlib.Path)):
                image = cv2.imread(str(input_source))
                if image is None:
                    raise ValueError(f"无法读取图片: {input_source}")
            else:
                image = input_source
                
            # 转换为RGB格式并检测
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            self._latest_result = self.detector.detect(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise BaseMediaPipeError(f"处理输入源失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据 - 子类必须实现此方法"""
        raise NotImplementedError("子类必须实现_process_result方法")

    def run(self, frame=None):
        """运行检测"""
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    raise ValueError("图片模式下不应该传入frame参数")
                return self._latest_result and self._process_result(self._latest_result, self._latest_frame.shape)
            
            if frame is None:
                raise ValueError("实时流模式下必须传入frame参数")
            
            # 转换为RGB格式并进行异步检测
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            self.detector.detect_async(mp_image, time.time_ns() // 1_000_000)
            
            return self._latest_result and self._process_result(self._latest_result, frame.shape)
                
        except Exception as e:
            raise BaseMediaPipeError(f"运行检测失败: {str(e)}")

    def draw(self, image, detection_data=None):
        """在图像上绘制检测结果 - 子类必须实现此方法"""
        raise NotImplementedError("子类必须实现draw方法")
        
    def get_fps(self):
        """获取当前FPS"""
        return self._fps
        
    def close(self):
        """释放资源"""
        if hasattr(self, 'detector'):
            self.detector.close()
        # 从资源管理器中注销
        unregister_resource(self)

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 