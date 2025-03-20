# 进阶使用技巧

本文档提供了AIToolkit Base的进阶使用技巧，帮助您更高效地使用这个工具包。

## 多检测器协同工作

在实际应用中，我们可能需要多个检测器协同工作，例如同时进行人脸检测和手势识别：

```python
from aitoolkit_base import Camera, FaceDetector, GestureRecognizer
import cv2

# 同时使用多个检测器
with Camera(0) as camera, FaceDetector() as face_detector, GestureRecognizer() as gesture_detector:
    for frame in camera:
        # 运行人脸检测
        faces = face_detector.run(frame)
        
        # 运行手势识别
        gestures = gesture_detector.run(frame)
        
        # 绘制人脸检测结果
        result = face_detector.draw(frame, faces)
        
        # 在同一个图像上叠加手势识别结果
        result = gesture_detector.draw(result, gestures)
        
        # 显示结果
        cv2.imshow("多检测器结果", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 性能优化技巧

### 降低分辨率

处理高分辨率图像会降低检测速度，可以考虑降低输入图像的分辨率：

```python
from aitoolkit_base import Camera, FaceDetector, ImageUtils
import cv2

with Camera(0) as camera, FaceDetector() as detector:
    for frame in camera:
        # 降低分辨率以提高速度
        small_frame = ImageUtils.resize_image(frame, width=640)
        
        # 运行检测
        faces = detector.run(small_frame)
        
        # 绘制结果
        result = detector.draw(small_frame, faces)
        
        # 显示结果
        cv2.imshow("低分辨率检测", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 减少检测频率

对于实时视频流，可以通过减少检测频率来提高性能：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

with Camera(0) as camera, FaceDetector() as detector:
    frame_count = 0
    last_faces = None
    
    for frame in camera:
        # 每3帧检测一次
        if frame_count % 3 == 0:
            faces = detector.run(frame)
            last_faces = faces
        else:
            faces = last_faces
        
        # 绘制结果
        if faces:
            result = detector.draw(frame, faces)
        else:
            result = frame
            
        # 显示结果    
        cv2.imshow("减少检测频率", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        frame_count += 1
```

### 调整检测参数

适当调整检测参数也可以提高性能：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 通过降低检测置信度阈值和最大检测数量来提高性能
with Camera(0) as camera, FaceDetector(min_detection_confidence=0.3, max_num_faces=1) as detector:
    for frame in camera:
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        cv2.imshow("优化参数", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 错误处理与异常恢复

在实际应用中，良好的错误处理非常重要：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2
import time

# 启动摄像头和检测器
try:
    camera = Camera(0, auto_reconnect=True)
    detector = FaceDetector()
    
    while True:
        try:
            # 读取帧
            ret, frame = camera.read()
            if not ret:
                print("无法读取帧，等待...")
                time.sleep(0.5)
                continue
            
            # 运行检测
            try:
                faces = detector.run(frame)
                result = detector.draw(frame, faces)
            except Exception as e:
                print(f"检测失败: {str(e)}")
                result = frame
            
            # 显示结果
            cv2.imshow("错误处理", result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except Exception as e:
            print(f"处理异常: {str(e)}")
            time.sleep(1)  # 出错时暂停一秒再继续
            
except Exception as e:
    print(f"严重错误: {str(e)}")
finally:
    # 确保资源被释放
    if 'camera' in locals():
        camera.release()
    if 'detector' in locals():
        detector.close()
    cv2.destroyAllWindows()
```

## 自定义检测结果处理

您可以自定义如何处理检测结果：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2
import time

# 自定义人脸信息处理
def process_face_info(faces):
    if not faces:
        return "未检测到人脸"
    
    result = []
    for i, face in enumerate(faces):
        confidence = face["score"] * 100
        box = face["bounding_box"]
        size = box["width"] * box["height"]
        
        result.append(f"人脸{i+1}: 置信度={confidence:.1f}%, 大小={size}像素")
    
    return "\n".join(result)

# 使用自定义处理
with Camera(0) as camera, FaceDetector() as detector:
    for frame in camera:
        # 运行检测
        faces = detector.run(frame)
        
        # 绘制基本结果
        result = detector.draw(frame, faces)
        
        # 处理并显示自定义信息
        info = process_face_info(faces)
        y_offset = 30
        for line in info.split("\n"):
            cv2.putText(result, line, (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 30
        
        # 显示结果
        cv2.imshow("自定义处理", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

## 录制视频

将检测结果保存为视频文件：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 设置视频录制参数
camera = Camera(0, width=1280, height=720)
detector = FaceDetector()

# 创建视频写入器
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1280, 720))

try:
    for frame in camera:
        # 运行检测
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        
        # 显示结果
        cv2.imshow("录制中", result)
        
        # 写入视频
        out.write(result)
        
        # 按q退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 释放资源
    camera.release()
    detector.close()
    out.release()
    cv2.destroyAllWindows()
```

## 使用异步模式

异步模式可以提高处理效率：

```python
from aitoolkit_base import Camera, FaceDetector
import cv2
import threading
import queue
import time

# 创建队列用于存储处理结果
result_queue = queue.Queue(maxsize=5)

# 异步处理线程
def process_frames(camera, detector, result_queue):
    for frame in camera:
        # 运行检测
        faces = detector.run(frame)
        result = detector.draw(frame, faces)
        
        # 将结果放入队列，如果队列满则等待
        try:
            result_queue.put((result, time.time()), block=False)
        except queue.Full:
            # 队列满，丢弃当前帧
            pass

# 主程序
with Camera(0) as camera, FaceDetector() as detector:
    # 启动处理线程
    processing_thread = threading.Thread(
        target=process_frames, 
        args=(camera, detector, result_queue)
    )
    processing_thread.daemon = True
    processing_thread.start()
    
    # 主线程负责显示
    while True:
        try:
            # 获取处理结果，超时1秒
            result, timestamp = result_queue.get(timeout=1)
            
            # 计算延迟
            delay = time.time() - timestamp
            
            # 显示结果和延迟
            cv2.putText(result, f"Delay: {delay*1000:.1f}ms", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("异步处理", result)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except queue.Empty:
            continue
```

## 组合多种机器视觉功能

将不同的机器视觉功能组合使用：

```python
from aitoolkit_base import Camera, FaceDetector, HandLandmarker
import cv2
import numpy as np

# 在同一帧上组合多种视觉功能
with Camera(0) as camera, FaceDetector() as face_detector, HandLandmarker() as hand_detector:
    for frame in camera:
        # 创建一个原始帧的副本
        display = frame.copy()
        
        # 添加人脸检测
        faces = face_detector.run(frame)
        if faces:
            display = face_detector.draw(display, faces)
        
        # 添加手部关键点检测
        hands = hand_detector.run(frame)
        if hands:
            display = hand_detector.draw(display, hands)
        
        # 显示结果
        cv2.imshow("视觉功能组合", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

以上就是AIToolkit Base的一些进阶使用技巧，通过这些技巧，您可以更高效地使用这个工具包来实现复杂的应用。 