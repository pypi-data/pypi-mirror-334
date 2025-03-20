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

class GestureRecognizerError(Exception):
    """手势识别错误"""
    pass

class GestureRecognizer:
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 num_hands=2,
                 min_hand_detection_confidence=0.5,
                 min_hand_presence_confidence=0.5,
                 min_tracking_confidence=0.5,
                 result_callback=None):  # 可选的回调函数
        """
        手势识别器
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            num_hands: 检测手的最大数量
            min_hand_detection_confidence: 最小手部检测置信度
            min_hand_presence_confidence: 最小手部存在置信度
            min_tracking_confidence: 最小跟踪置信度
            result_callback: 可选的回调函数，用于实时流模式
        """
        try:
            # 资源管理
            self._latest_result = None
            self._latest_frame = None
            
            # 基础参数设置
            self.num_hands = num_hands
            self.min_hand_detection_confidence = min_hand_detection_confidence
            self.min_hand_presence_confidence = min_hand_presence_confidence
            self.min_tracking_confidence = min_tracking_confidence
            self.result_callback = result_callback
            
            # 模型管理
            self.model_path = ModelManager.get_model_path('gesture_recognizer.task')
            
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
            raise GestureRecognizerError(f"初始化失败: {str(e)}")
            
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
            
    def _internal_callback(self, result, output_image, timestamp_ms):
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
                model_asset_path=self.model_path
            )
            
            if self.running_mode == vision.RunningMode.IMAGE:
                options = vision.GestureRecognizerOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    num_hands=self.num_hands,
                    min_hand_detection_confidence=self.min_hand_detection_confidence,
                    min_hand_presence_confidence=self.min_hand_presence_confidence,
                    min_tracking_confidence=self.min_tracking_confidence
                )
            else:
                options = vision.GestureRecognizerOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    num_hands=self.num_hands,
                    min_hand_detection_confidence=self.min_hand_detection_confidence,
                    min_hand_presence_confidence=self.min_hand_presence_confidence,
                    min_tracking_confidence=self.min_tracking_confidence,
                    result_callback=self._internal_callback
                )
                
            self.detector = vision.GestureRecognizer.create_from_options(options)
            
        except Exception as e:
            raise GestureRecognizerError(f"初始化检测器失败: {str(e)}")
            
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
            self._latest_result = self.detector.recognize(mp_image)
            self._latest_frame = image
            
        except Exception as e:
            raise GestureRecognizerError(f"处理输入源失败: {str(e)}")
            
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
                self.detector.recognize_async(mp_image, time.time_ns() // 1_000_000)
                return self._latest_result
            else:
                # 图片模式使用同步检测
                return self.detector.recognize(mp_image)
                
        except Exception as e:
            raise GestureRecognizerError(f"检测失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        gestures = []
        if detection_result and detection_result.gestures:
            h, w = image_shape[:2]
            for gesture, hand_landmarks, handedness in zip(
                detection_result.gestures,
                detection_result.hand_landmarks,
                detection_result.handedness):
                
                # 转换关键点坐标
                landmarks = []
                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    z = landmark.z
                    landmarks.append((x, y, z))
                
                gestures.append({
                    'gesture_type': gesture[0].category_name,
                    'score': gesture[0].score,
                    'hand_landmarks': landmarks,
                    'handedness': handedness[0].category_name
                })
        return gestures

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
            raise GestureRecognizerError(f"运行检测失败: {str(e)}")

    def draw(self, image, gestures=None):
        """在图像上绘制检测结果"""
        if not self._latest_result or not self._latest_result.hand_landmarks:
            return image
            
        image_copy = image.copy()
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands
        
        # 绘制每个检测到的手部
        for idx, hand_landmarks in enumerate(self._latest_result.hand_landmarks):
            # 创建规范化的关键点列表
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in hand_landmarks
            ])
            
            # 绘制手部关键点和连接线
            mp_drawing.draw_landmarks(
                image=image_copy,
                landmark_list=hand_landmarks_proto,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # 如果有手势识别结果，显示在图像上
            if self._latest_result.gestures:
                gesture = self._latest_result.gestures[idx]
                category_name = gesture[0].category_name
                score = round(gesture[0].score, 2)
                
                # 计算手部边界框用于放置文本
                frame_height, frame_width = image.shape[:2]
                x_min = min([landmark.x for landmark in hand_landmarks]) * frame_width
                y_min = min([landmark.y for landmark in hand_landmarks]) * frame_height
                
                # 绘制手势文本
                text = f'{category_name} ({score})'
                cv2.putText(image_copy, text, 
                          (int(x_min), max(0, int(y_min - 10))),
                          cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 2,
                          cv2.LINE_AA)
        
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