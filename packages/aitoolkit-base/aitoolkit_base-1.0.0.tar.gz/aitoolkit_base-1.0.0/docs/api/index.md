# AI视觉工具包使用指南

本指南将帮助老师和同学们了解AI视觉工具包中各个组件的使用方法，让AI技术在课堂上变得简单有趣！

## 视觉识别工具

这些是AI视觉工具包提供的各种识别工具，可以帮助你实现丰富多彩的互动教学活动：

- [人脸检测器](face_detector.md) - 检测人脸位置，可用于点名、互动游戏等
- [人脸特征分析](face_landmarker.md) - 分析人脸特征点，可用于表情识别、专注度跟踪等
- [手部姿态识别](hand_landmarker.md) - 识别手部动作，可用于手语教学、互动控制等
- [人体姿态识别](pose_landmarker.md) - 分析人体姿态，可用于体育动作指导、舞蹈教学等
- [手势识别器](gesture_recognizer.md) - 识别常见手势，可用于课堂互动、无接触控制等
- [物体识别器](object_detector.md) - 识别物体种类，可用于科学探索、自然观察等

## 辅助工具

这些是AI视觉工具包提供的实用辅助工具，帮助老师更轻松地设计互动课程：

- [相机工具](camera.md) - 增强的摄像头功能，拍摄更稳定、更清晰
- [图像处理](image_utils.md) - 图像处理工具，让教学素材处理更简单
- [资源管理](resource_manager.md) - 自动管理系统资源，不用担心程序卡顿
- [模型管理](model_manager.md) - 智能管理识别模型，让程序运行更流畅

## 通用参数

所有识别工具都支持的基本设置：

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `input_source` | 无/图片路径/视频路径/图像数据 | 无 | 输入源，可以是拍摄画面、图片或视频 |
| `min_detection_confidence` | 数值 | 0.5 | 识别可信度阈值，值越高要求越严格 |
| `min_tracking_confidence` | 数值 | 0.5 | 跟踪可信度阈值，值越高跟踪越精确 |
| `enable_gpu` | 是/否 | 否 | 是否启用图形加速，适用于性能较好的电脑 |
| `result_callback` | 回调函数 | 无 | 结果处理函数，适用于高级用户 |

## 通用方法

所有识别工具都支持的基本操作：

| 方法名 | 描述 |
|--------|------|
| `run(frame=None)` | 执行识别并返回结果 |
| `draw(image, results=None)` | 在图像上标记识别结果 |
| `get_fps()` | 查看当前处理速度 |
| `close()` | 关闭识别器并释放资源 |

## 教学应用示例

以下是几个简单的教学应用示例，帮助你快速开始：

### 课堂点名助手

```python
from aitoolkit_base import FaceDetector
import cv2

# 创建人脸检测器
detector = FaceDetector()

# 打开摄像头拍摄全班同学
image = cv2.imread("全班合影.jpg")

# 执行人脸检测
faces = detector.run(image)

# 在图像上标记每个同学
result_image = detector.draw(image, faces)

# 显示标记后的结果
cv2.imshow("课堂点名助手", result_image)
cv2.waitKey(0)

# 完成后释放资源
detector.close()
cv2.destroyAllWindows()
```

### 互动课堂小游戏

```python
from aitoolkit_base import FaceDetector, Camera
import cv2

# 使用简洁的方式启动
with Camera(0) as camera, FaceDetector() as detector:
    while True:
        # 获取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
            
        # 检测人脸
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        
        # 显示当前识别到的同学数量
        cv2.putText(result, f"识别到{len(faces)}位同学", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow("互动课堂", result)
        if cv2.waitKey(1) == 27:  # 按ESC键退出
            break
```

### 多功能教学助手

```python
from aitoolkit_base import FaceDetector, HandLandmarker, Camera
import cv2

# 同时使用多个识别工具
with Camera(0) as camera, \
     FaceDetector() as face_detector, \
     HandLandmarker() as hand_detector:
    
    while True:
        # 获取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
        
        # 同时分析人脸和手部
        faces = face_detector.run(frame)
        frame = face_detector.draw(frame, faces)
        
        hands = hand_detector.run(frame)
        frame = hand_detector.draw(frame, hands)
        
        # 在画面上显示检测到的人脸和手的数量
        cv2.putText(frame, f"发现{len(faces)}个人脸, {len(hands)}只手", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow("多功能教学助手", frame)
        if cv2.waitKey(1) == 27:
            break
``` 