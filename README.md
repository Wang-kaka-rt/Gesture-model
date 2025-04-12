# 手部检测程序

## 程序概述
这是一个使用MediaPipe和OpenCV实现的手部检测程序，可以实时检测摄像头画面中的手部并绘制特征点。

## 依赖安装
```bash
pip install opencv-python mediapipe
```

## 版本支持
- Python 3.9+
- opencv-python >=4.5.0
- mediapipe >=0.8.0
- numpy >=1.20.0

## 运行方法
```bash
python hand_detection.py
```

## 功能说明
- 实时检测摄像头画面中的手部
- 绘制手部21个特征点及其连接线
- 支持同时检测多只手
- 左右手识别功能
- 手势控制音量大小
- 手势调节屏幕亮度

## 退出方式
在程序运行窗口按'q'键退出程序。