# 人脸检测器

人脸检测器能够在图像或视频中找出人脸的位置，是许多有趣教学活动的基础工具。

## 导入方法

```python
from aitoolkit_base import FaceDetector
```

## 创建人脸检测器

创建人脸检测器时，可以设置以下参数：

```python
detector = FaceDetector(
    input_source=None,               # 输入源，可以是图片或视频
    min_detection_confidence=0.5,    # 识别可信度，0.0到1.0之间
    min_tracking_confidence=0.5,     # 跟踪可信度，0.0到1.0之间
    enable_gpu=False,                # 是否启用图形加速
    result_callback=None             # 结果处理函数
)
```

## 主要功能

### 检测人脸

```python
faces = detector.run(frame=None)
```

**输入：**
- `frame`：需要分析的图像，如果创建检测器时已提供输入源，则可不填

**输出：**
- 包含人脸信息的列表，每个人脸包含位置和置信度信息

### 在图像上标记人脸

```python
result_image = detector.draw(image, faces=None)
```

**输入：**
- `image`：要在其上标记人脸的图像
- `faces`：由`run()`返回的人脸信息，不填则使用最近一次的检测结果

**输出：**
- 标记了人脸的图像

### 查看处理速度

```python
fps = detector.get_fps()
```

**输出：**
- 当前每秒处理的帧数

### 释放资源

```python
detector.close()
```

释放检测器占用的资源，使用完毕后记得调用此方法。

## 教学应用示例

### 课堂点名系统

```python
from aitoolkit_base import FaceDetector
import cv2

# 创建人脸检测器
detector = FaceDetector(min_detection_confidence=0.7)  # 设置较高的识别可信度

# 读取班级合影
class_photo = cv2.imread("班级合影.jpg")

# 检测照片中的所有人脸
faces = detector.run(class_photo)

# 在照片上标记每个人脸
result = detector.draw(class_photo, faces)

# 显示结果和人数统计
cv2.putText(result, f"共发现{len(faces)}位同学", (10, 30), 
           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow("班级点名系统", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 关闭检测器
detector.close()
```

### 专注度监测

```python
from aitoolkit_base import FaceDetector, Camera
import cv2
import time

# 创建相机和人脸检测器
with Camera(0) as camera, FaceDetector() as detector:
    # 上次看到学生脸的时间
    last_face_time = time.time()
    
    while True:
        # 读取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
            
        # 检测人脸
        faces = detector.run(frame)
        
        # 分析学生是否在看屏幕
        current_time = time.time()
        
        if faces:  # 检测到人脸
            last_face_time = current_time
            status = "专注学习中"
            color = (0, 255, 0)  # 绿色
        else:  # 未检测到人脸
            time_away = current_time - last_face_time
            if time_away < 3:
                status = "暂时离开"
                color = (0, 255, 255)  # 黄色
            else:
                status = "注意力分散"
                color = (0, 0, 255)  # 红色
        
        # 在画面上显示状态
        result = detector.draw(frame, faces)
        cv2.putText(result, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # 显示结果
        cv2.imshow("专注度监测", result)
        if cv2.waitKey(1) == 27:  # 按ESC键退出
            break
```

### 趣味互动游戏

```python
from aitoolkit_base import FaceDetector, Camera
import cv2
import random
import time

# 创建趣味互动游戏
with Camera(0) as camera, FaceDetector(min_detection_confidence=0.6) as detector:
    # 游戏状态
    score = 0
    target_time = time.time() + random.uniform(3, 8)
    waiting_for_face = True
    game_over = False
    
    while not game_over:
        # 读取摄像头画面
        ret, frame = camera.read()
        if not ret:
            break
            
        # 检测人脸
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        
        current_time = time.time()
        
        # 游戏逻辑
        if waiting_for_face:
            if current_time > target_time:
                waiting_for_face = False
                cv2.putText(result, "现在！快做鬼脸！", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                target_time = current_time + 2  # 给学生2秒时间做鬼脸
            else:
                cv2.putText(result, "保持微笑，等待指令...", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if current_time < target_time:
                if not faces:  # 没检测到脸，可能是做鬼脸了
                    score += 1
                    waiting_for_face = True
                    target_time = current_time + random.uniform(3, 8)
            else:
                # 本轮结束
                waiting_for_face = True
                target_time = current_time + random.uniform(3, 8)
        
        # 显示得分
        cv2.putText(result, f"得分: {score}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # 显示结果
        cv2.imshow("趣味互动游戏", result)
        key = cv2.waitKey(1)
        if key == 27:  # ESC退出
            game_over = True
        elif key == ord('r'):  # R键重置
            score = 0
```

## 检测结果数据

`run()`方法返回的数据结构示例：

```python
[
    {
        "bbox": {
            "xmin": 125,    # 人脸左边界的X坐标
            "ymin": 86,     # 人脸上边界的Y坐标
            "width": 175,   # 人脸宽度
            "height": 200   # 人脸高度
        },
        "confidence": 0.92  # 检测的可信度，值越高越准确
    },
    # 可能有多个人脸...
]
```

## 使用技巧

1. 检测可信度(`min_detection_confidence`)设置越高，误检率越低，但可能会漏检一些难以辨认的人脸
2. 对于班级活动，建议调低检测可信度，确保能捕捉到所有同学
3. 光线充足的环境下检测效果更好
4. 推荐使用`with`语句自动管理资源（见教学应用示例）
5. 可以根据课程需要，调整不同的参数来获得最佳效果
6. 检测结果中的坐标可用于自定义标记或特效 