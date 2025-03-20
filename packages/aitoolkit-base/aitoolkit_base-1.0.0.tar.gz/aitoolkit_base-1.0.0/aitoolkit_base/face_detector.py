import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from .utils import ModelManager
import time
import pathlib
# 导入资源管理模块
from .resource_manager import register_resource, unregister_resource

class FaceDetectorError(Exception):
    """人脸检测错误"""
    pass

class FaceDetector:
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 min_detection_confidence=0.5,
                 min_suppression_threshold=0.5,
                 result_callback=None):  # 可选的回调函数
        """
        人脸检测器
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            min_detection_confidence: 最小检测置信度，范围0-1
            min_suppression_threshold: 最小重叠抑制阈值，范围0-1
            result_callback: 可选的回调函数，用于实时流模式
        """
        try:
            # 资源管理
            self._latest_result = None
            self._latest_frame = None
            
            # 基础参数设置
            self.min_detection_confidence = min_detection_confidence
            self.min_suppression_threshold = min_suppression_threshold
            self.result_callback = result_callback
            
            # 根据输入源确定模式
            self.running_mode = self._determine_mode(input_source)
            
            # 初始化检测器
            self._initialize_detector()
            
            # 注册到资源管理器
            register_resource(self)
            
            # 如果是图片模式，立即处理输入图片
            if input_source is not None:
                self._process_input_source(input_source)
                
        except Exception as e:
            raise FaceDetectorError(f"初始化失败: {str(e)}")
            
    def _determine_mode(self, input_source):
        """
        根据输入源确定运行模式
        """
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
            
    def _internal_callback(self, result: vision.FaceDetectorResult,
                         output_image: mp.Image, timestamp_ms: int):
        """内部回调函数，用于处理异步检测结果"""
        self._latest_result = result
        
        # 如果用户提供了回调函数，则调用它
        if self.result_callback:
            self.result_callback(result, output_image, timestamp_ms)
            
    def _initialize_detector(self):
        """
        初始化检测器
        """
        try:
            base_options = python.BaseOptions(
                model_asset_path=ModelManager.get_model_path("face_detector.tflite")
            )
            
            if self.running_mode == vision.RunningMode.IMAGE:
                options = vision.FaceDetectorOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    min_detection_confidence=self.min_detection_confidence,
                    min_suppression_threshold=self.min_suppression_threshold
                )
            else:
                options = vision.FaceDetectorOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    min_detection_confidence=self.min_detection_confidence,
                    min_suppression_threshold=self.min_suppression_threshold,
                    result_callback=self._internal_callback
                )
                
            self.detector = vision.FaceDetector.create_from_options(options)
            
        except Exception as e:
            raise FaceDetectorError(f"初始化检测器失败: {str(e)}")
            
    def _process_input_source(self, input_source):
        """
        处理输入源
        """
        try:
            if isinstance(input_source, (str, pathlib.Path)):
                image = cv2.imread(str(input_source))
                if image is None:
                    raise ValueError(f"无法读取图片: {input_source}")
            else:
                image = input_source
                
            # 转换为RGB格式
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            
            # 图片模式下直接进行同步检测
            self._latest_result = self.detector.detect(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise FaceDetectorError(f"处理输入源失败: {str(e)}")
            
    def detect(self, frame):
        """
        内部使用的底层检测方法
        Args:
            frame: 输入图像帧
        Returns:
            原始检测结果
        """
        if frame is None:
            return None
            
        try:
            # 转换为MediaPipe图像格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            if self.running_mode == vision.RunningMode.LIVE_STREAM:
                # 实时流模式使用异步检测
                self.detector.detect_async(mp_image, time.time_ns() // 1_000_000)
                return self._latest_result
            else:
                # 图片模式使用同步检测
                return self.detector.detect(mp_image)
                
        except Exception as e:
            raise FaceDetectorError(f"检测失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        faces_data = []
        if detection_result and detection_result.detections:
            h, w = image_shape[:2]
            
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                faces_data.append({
                    'bbox': (
                        int(bbox.origin_x),
                        int(bbox.origin_y),
                        int(bbox.width),
                        int(bbox.height)
                    ),
                    'score': detection.categories[0].score
                })
        return faces_data

    def run(self, frame=None):
        """
        运行检测
        Args:
            frame: 输入帧（仅实时流模式需要）
        Returns:
            格式化的检测结果
        """
        try:
            if self.running_mode == vision.RunningMode.IMAGE:
                if frame is not None:
                    raise ValueError("图片模式下不应该传入frame参数")
                return self._latest_result and self._process_result(self._latest_result, self._latest_frame.shape)
            else:  # 实时流模式
                if frame is None:
                    raise ValueError("实时流模式下必须传入frame参数")
                
                self._latest_frame = frame
                result = self.detect(frame)
                
                if result:
                    return self._process_result(result, frame.shape)
                return None
                
        except Exception as e:
            raise FaceDetectorError(f"运行检测失败: {str(e)}")

    def draw(self, image, faces_data=None):
        """
        在图像上绘制检测结果
        Args:
            image: BGR格式的图像
            faces_data: 人脸检测数据，如果为None则使用最新结果
        Returns:
            标注后的图像
        """
        image_copy = image.copy()
        
        # 获取原始的MediaPipe检测结果
        if self.running_mode == vision.RunningMode.IMAGE:
            result = self._latest_result
        else:
            result = self._latest_result

        # 如果有检测结果，手动绘制检测框和关键点
        if result and result.detections:
            for detection in result.detections:
                # 获取边界框
                bbox = detection.bounding_box
                x = int(bbox.origin_x)
                y = int(bbox.origin_y)
                w = int(bbox.width)
                h = int(bbox.height)
                
                # 绘制边界框
                cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # 如果有关键点，绘制关键点
                if hasattr(detection, 'keypoints'):
                    for keypoint in detection.keypoints:
                        kp_x = int(keypoint.x * image.shape[1])
                        kp_y = int(keypoint.y * image.shape[0])
                        cv2.circle(image_copy, (kp_x, kp_y), 2, (0, 255, 0), 2)
                
                # 显示置信度
                if detection.categories:
                    score = detection.categories[0].score
                    text = f"Score: {score:.2f}"
                    cv2.putText(image_copy, text, (x, y - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                              
        return image_copy

    def get_fps(self):
        """获取当前FPS - 已弃用，请使用camera模块的get_fps方法"""
        raise NotImplementedError("请使用camera模块的get_fps方法获取帧率")
        
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

