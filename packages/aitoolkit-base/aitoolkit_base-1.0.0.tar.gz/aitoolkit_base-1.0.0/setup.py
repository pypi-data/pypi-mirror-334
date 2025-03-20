from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aitoolkit_base",
    version="1.0.0",
    author="AIToolkit Team",
    author_email="your.email@example.com",
    description="一个面向中学生的简单AI工具包，提供人脸分析、人体分析、相机工具和图像分析功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haitao926/aitoolkit_base",
    project_urls={
        "Documentation": "https://haitao926.github.io/aitoolkit_base_docs/",
        "Bug Tracker": "https://github.com/haitao926/aitoolkit_base/issues",
    },
    packages=find_namespace_packages(include=['aitoolkit_base', 'aitoolkit_base.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'aitoolkit_base': [
            'models/face_detector.tflite',
            'models/face_landmarker.task',
            'models/hand_landmarker.task',
            'models/pose_landmarker.task',
            'models/gesture_recognizer.task',
            'models/object_detector.tflite',
            'examples/images/*.jpg',
        ],
    },
    data_files=[
        ('', ['README.md', 'requirements.txt']),
    ],
) 