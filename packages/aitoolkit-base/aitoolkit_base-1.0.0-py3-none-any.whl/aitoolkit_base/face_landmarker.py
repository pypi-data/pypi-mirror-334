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

class FaceLandmarkerError(Exception):
    """人脸关键点检测错误"""
    pass

class FaceLandmarker:
    def __init__(self, 
                 input_source=None,  # 输入源决定模式
                 num_faces=1,  # 检测脸的最大数量
                 min_face_detection_confidence=0.5,
                 min_face_presence_confidence=0.5,
                 min_tracking_confidence=0.5,
                 output_face_blendshapes=True,
                 output_facial_transformation_matrixes=False,
                 result_callback=None):  # 可选的回调函数
        """
        面部关键点检测器
        Args:
            input_source: 输入源，决定运行模式
                - None: 实时流模式
                - np.ndarray: 图片数据，图片模式
                - str/Path: 图片路径，图片模式
            num_faces: 检测脸的最大数量
            min_face_detection_confidence: 最小脸部检测置信度
            min_face_presence_confidence: 最小脸部存在置信度
            min_tracking_confidence: 最小跟踪置信度
            output_face_blendshapes: 是否输出面部混合形状
            output_facial_transformation_matrixes: 是否输出面部变换矩阵
            result_callback: 可选的回调函数，用于实时流模式
        """
        try:
            # 资源管理
            self._latest_result = None
            self._latest_frame = None
            
            # 基础参数设置
            self.num_faces = num_faces
            self.min_face_detection_confidence = min_face_detection_confidence
            self.min_face_presence_confidence = min_face_presence_confidence
            self.min_tracking_confidence = min_tracking_confidence
            self.result_callback = result_callback
            self.output_face_blendshapes = output_face_blendshapes
            self.output_facial_transformation_matrixes = output_facial_transformation_matrixes
            
            # 模型管理
            self.model_path = ModelManager.get_model_path('face_landmarker.task')
            
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
            raise FaceLandmarkerError(f"初始化失败: {str(e)}")
            
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
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    num_faces=self.num_faces,
                    min_face_detection_confidence=self.min_face_detection_confidence,
                    min_face_presence_confidence=self.min_face_presence_confidence,
                    min_tracking_confidence=self.min_tracking_confidence,
                    output_face_blendshapes=self.output_face_blendshapes,
                    output_facial_transformation_matrixes=self.output_facial_transformation_matrixes
                )
            else:
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    running_mode=self.running_mode,
                    num_faces=self.num_faces,
                    min_face_detection_confidence=self.min_face_detection_confidence,
                    min_face_presence_confidence=self.min_face_presence_confidence,
                    min_tracking_confidence=self.min_tracking_confidence,
                    output_face_blendshapes=self.output_face_blendshapes,
                    output_facial_transformation_matrixes=self.output_facial_transformation_matrixes,
                    result_callback=self._internal_callback
                )
                
            self.detector = vision.FaceLandmarker.create_from_options(options)
            
        except Exception as e:
            raise FaceLandmarkerError(f"初始化检测器失败: {str(e)}")
            
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
            raise FaceLandmarkerError(f"处理输入源失败: {str(e)}")
            
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
            raise FaceLandmarkerError(f"检测失败: {str(e)}")

    def _process_result(self, detection_result, image_shape):
        """处理检测结果为格式化的数据"""
        faces_data = []
        if detection_result and detection_result.face_landmarks:
            h, w = image_shape[:2]
            
            for i, face_landmarks in enumerate(detection_result.face_landmarks):
                # 转换所有关键点坐标
                landmarks = []
                for landmark in face_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    z = landmark.z
                    landmarks.append((x, y, z))
                
                # 获取表情数据
                blendshapes = {}
                if detection_result.face_blendshapes:
                    for category in detection_result.face_blendshapes[i]:
                        blendshapes[category.category_name] = category.score
                
                faces_data.append({
                    'landmarks': landmarks,
                    'blendshapes': blendshapes
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
            raise FaceLandmarkerError(f"运行检测失败: {str(e)}")

    def draw(self, image, faces_data=None):
        """在图像上绘制检测结果"""
        if not self._latest_result or not self._latest_result.face_landmarks:
            return image
            
        # 转换为RGB格式进行绘制
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        annotated_image = np.copy(rgb_image)
        
        # 绘制每个检测到的人脸
        for face_landmarks in self._latest_result.face_landmarks:
            # 创建规范化的关键点列表
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in face_landmarks
            ])
            
            # 绘制面部网格
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
            )
            
            # 绘制面部轮廓
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
            )
            
            # 绘制眼睛
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style()
            )
        
        # 如果有表情数据，显示在图像上
        if faces_data:
            y_pos = 30
            for face_data in faces_data:
                if 'blendshapes' in face_data:
                    for name, score in face_data['blendshapes'].items():
                        if score > 0.5:  # 只显示明显的表情
                            text = f"{name}: {score:.2f}"
                            cv2.putText(annotated_image, text, (10, y_pos),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                      (0, 255, 0), 1)
                            y_pos += 20
        
        # 转换回BGR格式用于显示
        return cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

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