import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from .utils import ModelManager
from .base_detector import BaseMediaPipeDetector, BaseMediaPipeError

class ObjectDetectionError(BaseMediaPipeError):
    """目标检测错误"""
    pass

class ObjectDetector(BaseMediaPipeDetector):
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 max_results=5,  # 最大检测结果数
                 score_threshold=0.5,  # 检测阈值
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5,
                 enable_gpu=False,  # 是否启用GPU加速
                 result_callback=None):  # 可选的回调函数
        """
        目标检测器
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            max_results: 最大检测结果数
            score_threshold: 检测阈值
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小跟踪置信度
            enable_gpu: 是否启用GPU加速
            result_callback: 可选的回调函数，用于实时流模式
        """
        self.max_results = max_results
        self.score_threshold = score_threshold
        super().__init__(
            input_source=input_source,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            enable_gpu=enable_gpu,
            result_callback=result_callback
        )
            
    def _initialize_detector(self):
        """初始化检测器"""
        try:
            base_options = python.BaseOptions(
                model_asset_path=ModelManager.get_model_path("object_detector.tflite")
            )
            
            # 如果启用GPU，设置代理设备
            if self.enable_gpu:
                base_options.delegate = python.BaseOptions.Delegate.GPU
            
            if self.running_mode == vision.RunningMode.IMAGE:
                options = vision.ObjectDetectorOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    max_results=self.max_results,
                    score_threshold=self.score_threshold
                )
            else:
                options = vision.ObjectDetectorOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    max_results=self.max_results,
                    score_threshold=self.score_threshold,
                    result_callback=self._save_result
                )
                
            self.detector = vision.ObjectDetector.create_from_options(options)
            
        except Exception as e:
            raise ObjectDetectionError(f"初始化检测器失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        if not detection_result or not detection_result.detections:
            return None
            
        h, w = image_shape[:2]
        results = []
        
        for detection in detection_result.detections:
            bbox = detection.bounding_box
            category = detection.categories[0]
            
            results.append({
                'bbox': {
                    'x': int(bbox.origin_x),
                    'y': int(bbox.origin_y),
                    'width': int(bbox.width),
                    'height': int(bbox.height)
                },
                'label': category.category_name,
                'score': category.score,
                'index': category.index
            })
            
        return results

    def draw(self, image, detections=None):
        """在图像上绘制检测结果"""
        if not self._latest_result or not self._latest_result.detections:
            return image
            
        image_copy = image.copy()
        
        for detection in self._latest_result.detections:
            # 获取边界框
            bbox = detection.bounding_box
            x = int(bbox.origin_x)
            y = int(bbox.origin_y)
            w = int(bbox.width)
            h = int(bbox.height)
            
            # 获取类别和置信度
            category = detection.categories[0]
            label = category.category_name
            score = category.score
            
            # 绘制边界框
            cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 绘制标签和置信度
            text = f"{label}: {score:.2f}"
            cv2.putText(
                image_copy,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA
            )
            
        return image_copy 