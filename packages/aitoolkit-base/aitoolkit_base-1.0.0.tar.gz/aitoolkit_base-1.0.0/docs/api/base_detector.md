# 识别工具基础知识

本页介绍AI视觉工具包中各种识别工具的共同特点和基础知识，帮助老师和同学们更好地理解如何在课堂中使用这些有趣的工具。

## 我们能用什么识别工具？

AI视觉工具包提供了多种识别工具，每种工具都有特定的用途：

- **人脸检测器**：找出图像中人脸的位置，适用于点名、课堂互动等
- **人脸特征分析**：识别人脸上的468个关键点，可分析表情、专注度等
- **手部姿态识别**：捕捉手部的21个关键点，适用于手语教学、互动控制等
- **人体姿态识别**：捕捉全身33个关键点，适用于体育指导、舞蹈教学等
- **手势识别器**：识别常见手势，适用于无接触控制、互动游戏等
- **物体识别器**：识别常见物体，适用于科学探索、自然观察等

## 识别工具的共同特点

虽然每种识别工具功能不同，但它们都遵循相似的使用方式，让你可以轻松切换不同工具：

### 1. 创建识别工具

所有识别工具都可以通过类似的方式创建：

```python
from aitoolkit_base import FaceDetector  # 导入你需要的识别工具

# 创建识别工具
detector = FaceDetector(
    input_source=None,               # 可以是None、图片路径或视频
    min_detection_confidence=0.5,    # 识别可信度
    min_tracking_confidence=0.5,     # 跟踪可信度
    enable_gpu=False                 # 是否使用图形加速
)
```

### 2. 执行识别

所有识别工具都使用`run()`方法执行识别：

```python
# 给识别工具提供一张图片
results = detector.run(image)
```

### 3. 显示结果

所有识别工具都使用`draw()`方法显示结果：

```python
# 在图片上标记识别结果
marked_image = detector.draw(image, results)
```

### 4. 释放资源

使用完毕后，记得释放资源：

```python
# 释放识别工具占用的资源
detector.close()
```

## 使用"with"语句简化操作

推荐使用"with"语句创建识别工具，这样会自动释放资源：

```python
from aitoolkit_base import FaceDetector
import cv2

# 使用with语句创建识别工具
with FaceDetector() as detector:
    # 读取图片
    image = cv2.imread("学生照片.jpg")
    
    # 识别人脸
    faces = detector.run(image)
    
    # 标记结果
    result = detector.draw(image, faces)
    
    # 显示结果
    cv2.imshow("识别结果", result)
    cv2.waitKey(0)
# 离开with块时自动释放资源
```

## 识别工具的工作模式

识别工具有三种主要工作模式：

### 1. 图片模式

适用于对单张图片进行分析，例如班级合影人脸统计：

```python
with FaceDetector() as detector:
    # 分析班级合影
    image = cv2.imread("班级合影.jpg")
    faces = detector.run(image)
    result = detector.draw(image, faces)
    cv2.imwrite("标记后的合影.jpg", result)
```

### 2. 视频模式

适用于实时互动，例如课堂互动游戏：

```python
with Camera(0) as camera, FaceDetector() as detector:
    while True:
        # 获取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
            
        # 识别人脸
        faces = detector.run(frame)
        
        # 标记结果
        result = detector.draw(frame, faces)
        
        # 显示结果
        cv2.imshow("课堂互动", result)
        if cv2.waitKey(1) == 27:  # 按ESC键退出
            break
```

### 3. 图片文件夹模式

适用于处理多张图片，例如学生作品分析：

```python
import os
from aitoolkit_base import ObjectDetector
import cv2

# 创建识别工具
with ObjectDetector() as detector:
    # 处理文件夹中的所有图片
    folder = "学生作品"
    for filename in os.listdir(folder):
        if filename.endswith((".jpg", ".png")):
            # 读取图片
            image_path = os.path.join(folder, filename)
            image = cv2.imread(image_path)
            
            # 识别物体
            objects = detector.run(image)
            
            # 标记结果
            result = detector.draw(image, objects)
            
            # 保存结果
            output_path = os.path.join("分析结果", filename)
            cv2.imwrite(output_path, result)
```

## 多识别工具组合使用

可以组合多种识别工具创建更丰富的教学活动：

```python
with Camera(0) as camera, \
     FaceDetector() as face_detector, \
     HandLandmarker() as hand_detector:
    
    while True:
        # 获取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
        
        # 同时识别人脸和手部
        faces = face_detector.run(frame)
        frame = face_detector.draw(frame, faces)
        
        hands = hand_detector.run(frame)
        frame = hand_detector.draw(frame, hands)
        
        # 显示结果
        cv2.imshow("多功能识别", frame)
        if cv2.waitKey(1) == 27:  # 按ESC退出
            break
```

## 教学小贴士

1. **准备工作**：确保教室光线充足，摄像头位置合适
2. **参数调整**：根据实际需要调整识别可信度，值越高越严格
3. **资源管理**：使用`with`语句自动管理资源，避免程序卡顿
4. **先测试**：正式课堂前先测试识别效果，确保流畅
5. **简单开始**：先从单一识别工具开始，熟悉后再尝试组合使用
6. **创意思考**：鼓励学生思考AI识别工具在各学科中的创新应用
7. **安全第一**：注意保护学生隐私，不要存储或分享个人识别数据 