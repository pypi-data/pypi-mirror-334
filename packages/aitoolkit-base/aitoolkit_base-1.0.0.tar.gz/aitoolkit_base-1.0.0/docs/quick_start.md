# 快速入门指南

本文档将帮助您迅速上手AIToolkit Base，了解如何使用各种检测器和摄像头工具。

## 基本概念

AIToolkit Base的所有检测器都遵循相同的使用模式：

1. **创建检测器**：使用适当的参数初始化检测器
2. **运行检测**：调用`run()`方法进行检测
3. **可视化结果**：使用`draw()`方法将结果绘制在图像上
4. **释放资源**：使用`close()`方法或上下文管理器释放资源

## 运行模式

所有检测器支持两种运行模式：

1. **图片模式**：处理单张图片，通过初始化参数指定
2. **视频流模式**：处理实时视频流，需要在每次调用`run()`时提供新的帧

## 检测器使用示例

### 1. 人脸检测

```python
from aitoolkit_base import FaceDetector
import cv2

# 方法1：图片模式 - 使用图片路径
detector = FaceDetector(input_source="person.jpg")  
faces = detector.run()  # 不需要传入frame
result = detector.draw(cv2.imread("person.jpg"), faces)
cv2.imwrite("result.jpg", result)
detector.close()

# 方法2：图片模式 - 使用图片数据
image = cv2.imread("person.jpg")
detector = FaceDetector(input_source=image)
faces = detector.run()
result = detector.draw(image, faces)
detector.close()

# 方法3：视频流模式 - 普通使用
detector = FaceDetector()  # 不指定input_source表示视频流模式
camera = cv2.VideoCapture(0)
while True:
    ret, frame = camera.read()
    if not ret:
        break
    faces = detector.run(frame)  # 视频模式需要传入frame
    result = detector.draw(frame, faces)
    cv2.imshow("人脸检测", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
detector.close()

# 方法4：视频流模式 - 使用上下文管理器（推荐）
with FaceDetector() as detector:
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        cv2.imshow("人脸检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
```

### 2. 人脸关键点检测

```python
from aitoolkit_base import FaceLandmarker
import cv2

# 图片模式 - 使用上下文管理器
with FaceLandmarker(input_source="person.jpg") as landmarker:
    landmarks = landmarker.run()
    image = cv2.imread("person.jpg")
    result = landmarker.draw(image, landmarks)
    cv2.imwrite("face_landmarks.jpg", result)
    
# 视频流模式 - 使用上下文管理器
with FaceLandmarker() as landmarker:
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        landmarks = landmarker.run(frame)
        result = landmarker.draw(frame, landmarks)
        cv2.imshow("人脸关键点", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
```

### 3. 手势识别

```python
from aitoolkit_base import GestureRecognizer
import cv2

# 图片模式
with GestureRecognizer(input_source="gesture.jpg") as recognizer:
    gestures = recognizer.run()
    image = cv2.imread("gesture.jpg")
    result = recognizer.draw(image, gestures)
    cv2.imwrite("gesture_result.jpg", result)
    
# 视频流模式
with GestureRecognizer() as recognizer:
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        gestures = recognizer.run(frame)
        result = recognizer.draw(frame, gestures)
        cv2.imshow("手势识别", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
```

## 使用摄像头工具

AIToolkit Base提供了增强的摄像头工具`Camera`，具有多线程帧捕获、自动重连等功能：

```python
from aitoolkit_base import Camera, FaceDetector, cv_imshow
import cv2

# 方法1：使用Camera类替代cv2.VideoCapture
camera = Camera(0)  # 0表示第一个摄像头
detector = FaceDetector()

try:
    while True:
        ret, frame = camera.read()  # 与cv2.VideoCapture接口相同
        if not ret:
            continue
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        cv2.imshow("人脸检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.release()
    detector.close()

# 方法2：使用迭代器语法（更简洁）
with Camera(0) as camera, FaceDetector() as detector:
    for frame in camera:  # 迭代器自动读取每一帧
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        cv2.imshow("人脸检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # 或使用 camera.stop_iteration() 停止迭代

# 方法3：使用增强的显示函数
with Camera(0) as camera, FaceDetector() as detector:
    for frame in camera:
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        # 可选显示方式：'cv2'、'inline'（Jupyter）、'web'
        cv_imshow(result, show_method="cv2", window_name="人脸检测")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 异步处理（回调函数）

所有检测器都支持异步处理模式，通过回调函数处理结果：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 定义回调函数
def process_result(result, image, timestamp_ms):
    if result:
        processed = detector.draw(image, result)
        cv2.imshow("异步处理", processed)

# 使用回调函数的异步处理
with Camera(0) as camera, FaceDetector(result_callback=process_result) as detector:
    for frame in camera:
        detector.run(frame)  # 结果会通过回调函数处理
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 继续学习

- [API参考文档](./api/index.md) - 详细的API参考
- [Camera类详解](./api/camera.md) - 了解摄像头工具的全部功能
- [资源管理机制](./resource_management.md) - 了解资源管理的工作原理
- [检测器进阶用法](./advanced_usage.md) - 学习更高级的使用技巧 