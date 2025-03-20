# AIToolkit Base 文档

![智能模式自动切换+统一API设计+多模态检测](https://via.placeholder.com/800x200.png/0077B5/FFFFFF?text=智能模式自动切换+统一API设计+多模态检测)

## 项目简介

AIToolkit Base 是一个面向中学生的简单AI工具包，基于MediaPipe封装，提供简单易用的人脸检测、人脸关键点检测、手部关键点检测、人体姿态检测、手势识别和物体检测功能。

该工具包设计以简单、易用和教育为目标，适合在中学AI教育中使用，帮助学生快速理解和应用人工智能技术。

## 主要特性

- **简单易用的API设计**：统一的接口风格，易于上手
- **智能输入源识别**：自动区分图片/视频流输入
- **统一的接口设计**：所有检测器采用一致的初始化参数和方法
- **中文注释和文档**：提供全面的中文文档和注释
- **自动的可视化功能**：内置绘制功能，轻松可视化检测结果
- **实时处理支持**：支持摄像头实时处理和异步检测
- **资源自动管理**：内置资源管理机制，避免资源泄露
- **多种显示方式**：支持OpenCV窗口、Jupyter内联显示和网页显示

## 功能模块

### 智能检测模块
| 模块名称 | 功能描述 | 输入模式支持 | 资源管理 |
|--------------------|-----------------------------------|--------------|------------|
| FaceLandmarker | 人脸468关键点检测 | ✅ 图片/视频流 | ✅ 自动释放 |
| HandLandmarker | 双手21关键点检测 | ✅ 图片/视频流 | ✅ 自动释放 |
| PoseLandmarker | 全身33关键点检测 | ✅ 图片/视频流 | ✅ 自动释放 |
| GestureRecognizer | 20+种手势识别 | ✅ 图片/视频流 | ✅ 自动释放 |
| FaceDetector | 人脸检测与跟踪 | ✅ 图片/视频流 | ✅ 自动释放 |
| ObjectDetector | 目标检测与跟踪 | ✅ 图片/视频流 | ✅ 自动释放 |

### 辅助工具模块
- **Camera**：增强的摄像头工具，支持多线程帧捕获、自动重连等功能
- **ImageUtils**：图像处理工具类，提供调整大小、格式转换等功能
- **ModelManager**：模型管理工具，负责模型文件的查找和管理

## 安装指南

### 系统要求
- Python 3.8+
- Windows/Linux/macOS

### 安装依赖
```bash
pip install mediapipe>=0.10.0 opencv-python>=4.8.0 numpy>=1.24.0
```

### Windows系统安装
1. 下载或克隆本仓库
2. 进入项目目录：`cd aitoolkit_base`
3. 运行安装脚本：`build_wheel.bat`

### Linux/Mac系统安装
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

2. 复制模型文件到 `aitoolkit_base/models/`目录

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 安装包：
```bash
pip install -e .
```

## 快速入门

请参阅[快速入门指南](./quick_start.md)了解如何开始使用AIToolkit Base。 