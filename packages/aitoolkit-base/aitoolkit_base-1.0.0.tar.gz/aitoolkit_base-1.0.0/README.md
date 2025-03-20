# AIToolkit Base

一个面向中学生的简单AI工具包，基于MediaPipe封装，提供简单易用的人脸检测、人脸关键点检测、手部关键点检测、人体姿态检测、手势识别和物体检测功能。

## 功能特点

- 简单易用的API设计
- 统一的接口风格
- 中文注释和文档
- 自动的可视化功能
- 实时处理支持

## 1.0版本固化功能

### 人脸分析
- **人脸检测**：提升多人脸检测稳定性
- **人脸关键点**：优化478点精确定位

### 人体分析
- **手部关键点**：提升21点3D坐标准确性
- **人体姿态**：优化33点检测与多人跟踪
- **手势识别**：扩展更多手势类型识别

### 相机工具
- **相机工具**：增强实时处理功能
- 支持cv2，web api 等多种网页端显示功能
- **迭代器支持**：可使用`for frame in camera:`语法直接遍历视频帧

### 图像分析
- **物体检测**：提升检测速度与精度

## 安装说明

### Windows系统

1. 下载或克隆本仓库
2. 进入项目目录：`cd aitoolkit_base`
3. 运行安装脚本：`build_wheel.bat`

### Linux/Mac系统

1. 下载或克隆本仓库
2. 进入项目目录：`cd aitoolkit_base`
3. 添加执行权限：`chmod +x build_wheel.sh`
4. 运行安装脚本：`./build_wheel.sh`

### 手动安装

如果安装脚本不起作用，可以手动安装：

1. 创建模型目录：
```bash
mkdir -p aitoolkit_base/models
```

2. 复制模型文件（从mediapipe-samples目录）到 `aitoolkit_base/models/`

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 安装包：
```bash
pip install -e .
```

## 使用方法

### 1. 人脸检测

```python
from aitoolkit_base import FaceDetector
import cv2

# 创建检测器
detector = FaceDetector()

# 读取图像
image = cv2.imread('test.jpg')

# 运行检测
faces = detector.run(image)

# 绘制结果
result = detector.draw(image, faces)
```

### 2. 手势识别

```python
from aitoolkit_base import GestureRecognizer
import cv2

# 创建识别器
recognizer = GestureRecognizer()

# 读取图像
image = cv2.imread('test.jpg')

# 运行识别
gestures = recognizer.run(image)

# 绘制结果
result = recognizer.draw(image, gestures)
```

### 3. 相机实时处理

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 创建相机和检测器
camera = Camera()
detector = FaceDetector()

# 实时检测循环
while True:
    frame = camera.read()
    faces = detector.run(frame)
    result = detector.draw(frame, faces)
    cv2.imshow("人脸检测", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
```

### 4. 相机迭代器用法

```python
from aitoolkit_base import Camera, FaceDetector
import cv2

# 创建相机和检测器
camera = Camera()
detector = FaceDetector()

# 使用迭代器语法直接遍历视频帧
for frame in camera:
    # 处理每一帧
    faces = detector.run(frame)
    result = detector.draw(frame, faces)
    
    # 显示结果
    cv2.imshow("人脸检测", result)
    
    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# 释放资源
camera.release()
cv2.destroyAllWindows()
```

## 实时处理示例

查看 `examples` 目录获取更多实时处理的示例代码。

## 常见问题

1. 模型文件找不到
   - 确保模型文件已正确复制到 `aitoolkit_base/models/` 目录
   - 检查模型文件名是否正确

2. 实时处理速度慢
   - 尝试降低输入图像分辨率
   - 使用 `ImageUtils.resize_image()` 调整图像大小
   - 考虑使用性能更好的硬件

3. 检测不准确
   - 调整 `min_detection_confidence` 参数
   - 确保光线充足
   - 保持适当的距离 