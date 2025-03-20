# FaceLandmarker

`FaceLandmarker` 是用于检测和跟踪人脸468个关键点的类，可以实现精确的人脸特征定位。

## 导入

```python
from aitoolkit_base import FaceLandmarker
```

## 初始化参数

创建 `FaceLandmarker` 实例时，可以使用以下参数：

```python
FaceLandmarker(
    input_source=None,               # 输入源，决定运行模式
    min_detection_confidence=0.5,    # 最小检测置信度
    min_tracking_confidence=0.5,     # 最小跟踪置信度
    enable_gpu=False,                # 是否启用GPU加速
    result_callback=None,            # 可选的回调函数
    output_face_blendshapes=False,   # 是否输出面部表情系数
    output_facial_transformation_matrixes=False, # 是否输出面部变换矩阵
    num_faces=1                      # 最大检测人脸数
)
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| input_source | None/str/Path/np.ndarray | None | 输入源，决定运行模式 |
| min_detection_confidence | float | 0.5 | 最小检测置信度，范围[0.0, 1.0] |
| min_tracking_confidence | float | 0.5 | 最小跟踪置信度，范围[0.0, 1.0] |
| enable_gpu | bool | False | 是否启用GPU加速 |
| result_callback | callable | None | 可选的回调函数，用于实时流模式 |
| output_face_blendshapes | bool | False | 是否输出面部表情系数 |
| output_facial_transformation_matrixes | bool | False | 是否输出面部变换矩阵 |
| num_faces | int | 1 | 最大检测人脸数 |

## 主要方法

### run

运行人脸关键点检测，返回检测结果。

```python
landmarks = landmarker.run(frame=None)
```

**参数：**
- `frame` (np.ndarray, 可选): 要处理的图像帧，仅视频流模式需要。

**返回：**
- `list`: 包含检测到的人脸关键点信息的列表，每个人脸是一个字典，包括:
  - `face_landmarks` (list): 468个人脸关键点的列表，每个关键点包含x、y、z坐标
  - `face_blendshapes` (list, 可选): 面部表情系数列表
  - `facial_transformation_matrixes` (list, 可选): 面部变换矩阵列表

### draw

在图像上绘制检测结果。

```python
result_image = landmarker.draw(image, landmarks=None, connection_drawing_spec=None)
```

**参数：**
- `image` (np.ndarray): 要绘制的原始图像
- `landmarks` (list, 可选): 由 `run()` 方法返回的检测结果，如果为None则使用最近一次的结果
- `connection_drawing_spec` (dict, 可选): 连接线绘制规格，包括颜色、线宽等

**返回：**
- `np.ndarray`: 绘制了检测结果的图像

### get_fps

获取当前处理的帧率。

```python
fps = landmarker.get_fps()
```

**返回：**
- `float`: 当前的FPS

### close

释放资源。

```python
landmarker.close()
```

## 使用示例

### 图片模式

```python
from aitoolkit_base import FaceLandmarker
import cv2

# 方法1：使用图片路径
with FaceLandmarker(input_source="person.jpg") as landmarker:
    landmarks = landmarker.run()
    image = cv2.imread("person.jpg")
    result = landmarker.draw(image, landmarks)
    cv2.imwrite("landmarks_result.jpg", result)

# 方法2：使用图片数据
image = cv2.imread("person.jpg")
with FaceLandmarker(input_source=image) as landmarker:
    landmarks = landmarker.run()
    result = landmarker.draw(image, landmarks)
    cv2.imwrite("landmarks_result.jpg", result)
```

### 视频流模式

```python
from aitoolkit_base import FaceLandmarker, Camera
import cv2

# 实时检测
with Camera(0) as camera, FaceLandmarker() as landmarker:
    for frame in camera:
        # 运行检测
        landmarks = landmarker.run(frame)
        
        # 绘制结果
        result = landmarker.draw(frame, landmarks)
        
        # 显示FPS
        fps = landmarker.get_fps()
        cv2.putText(result, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 显示结果
        cv2.imshow("人脸关键点", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 获取表情系数

```python
from aitoolkit_base import FaceLandmarker, Camera
import cv2

# 启用表情系数输出
with Camera(0) as camera, FaceLandmarker(output_face_blendshapes=True) as landmarker:
    for frame in camera:
        # 运行检测
        landmarks = landmarker.run(frame)
        
        # 绘制结果
        result = landmarker.draw(frame, landmarks)
        
        # 如果检测到人脸，显示表情系数
        if landmarks and len(landmarks) > 0 and 'face_blendshapes' in landmarks[0]:
            blendshapes = landmarks[0]['face_blendshapes']
            # 找到最明显的表情
            max_expression = max(blendshapes.items(), key=lambda x: x[1])
            expression_name, confidence = max_expression
            cv2.putText(result, f"{expression_name}: {confidence:.2f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow("人脸表情", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 返回数据结构

`run()` 方法返回的数据结构示例：

```python
[
    {
        "face_landmarks": [
            {"x": 0.4, "y": 0.3, "z": 0.01},  # 第1个关键点
            {"x": 0.41, "y": 0.305, "z": 0.011},  # 第2个关键点
            # ... 共468个关键点
        ],
        "face_blendshapes": {  # 如果启用了output_face_blendshapes
            "neutral": 0.8,
            "smile": 0.1,
            "eye_blink_left": 0.05,
            # ... 其他表情系数
        },
        "facial_transformation_matrixes": [  # 如果启用了output_facial_transformation_matrixes
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
    },
    # 可能有多个人脸...
]
```

## 注意事项

1. FaceLandmarker 提供了比 FaceDetector 更详细的人脸分析结果
2. 默认情况下只检测一个人脸，如需检测多个人脸，请调整 `num_faces` 参数
3. 启用表情系数或变换矩阵会增加计算负担，可能影响实时性能
4. 关键点坐标是归一化的，范围在[0,1]之间，需要乘以图像尺寸获取实际像素坐标
5. 推荐使用上下文管理器（with语句）自动管理资源 