#!/bin/bash

# 清理之前的构建文件
rm -rf build/ dist/ *.egg-info/

# 确保模型文件存在
mkdir -p aitoolkit_base/models
cp ../mediapipe-samples/python/mediapipe-samples/face_detector/face_detector.task aitoolkit_base/models/
cp ../mediapipe-samples/python/mediapipe-samples/face_landmarker/face_landmarker.task aitoolkit_base/models/
cp ../mediapipe-samples/python/mediapipe-samples/hand_landmarker/hand_landmarker.task aitoolkit_base/models/
cp ../mediapipe-samples/python/mediapipe-samples/pose_landmarker/pose_landmarker.task aitoolkit_base/models/
cp ../mediapipe-samples/python/mediapipe-samples/gesture_recognizer/gesture_recognizer.task aitoolkit_base/models/
cp ../mediapipe-samples/python/mediapipe-samples/face_stylizer/face_stylizer.task aitoolkit_base/models/

# 构建wheel包
python setup.py bdist_wheel

echo "Wheel包已生成在dist/目录下" 