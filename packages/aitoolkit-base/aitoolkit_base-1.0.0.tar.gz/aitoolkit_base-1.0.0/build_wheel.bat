@echo off

REM 清理之前的构建文件
rmdir /s /q build dist *.egg-info 2>nul

REM 确保模型文件存在
mkdir aitoolkit_base\models 2>nul

REM 检查并复制模型文件（如果不存在）
if not exist "aitoolkit_base\models\face_detector.tflite" (
    copy ..\mediapipe-samples\python\mediapipe-samples\face_detector\face_detector.tflite aitoolkit_base\models\face_detector.tflite
)
if not exist "aitoolkit_base\models\face_landmarker.task" (
    copy ..\mediapipe-samples\python\mediapipe-samples\face_landmarker\face_landmarker.task aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\hand_landmarker.task" (
    copy ..\mediapipe-samples\python\mediapipe-samples\hand_landmarker\hand_landmarker.task aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\pose_landmarker.task" (
    copy ..\mediapipe-samples\python\mediapipe-samples\pose_landmarker\pose_landmarker.task aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\gesture_recognizer.task" (
    copy ..\mediapipe-samples\python\mediapipe-samples\gesture_recognizer\gesture_recognizer.task aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\face_stylizer.task" (
    copy ..\mediapipe-samples\python\mediapipe-samples\face_stylizer\face_stylizer.task aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\interactive_segmenter.tflite" (
    copy ..\mediapipe-samples\python\mediapipe-samples\interactive_segmenter\interactive_segmenter.tflite aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\text_embedder.tflite" (
    copy ..\mediapipe-samples\python\mediapipe-samples\text_embedder\text_embedder.tflite aitoolkit_base\models\
)
if not exist "aitoolkit_base\models\image_embedder.tflite" (
    copy ..\mediapipe-samples\python\mediapipe-samples\image_embedder\image_embedder.tflite aitoolkit_base\models\
)

REM 构建wheel包
python setup.py bdist_wheel

echo Wheel包已生成在dist/目录下 