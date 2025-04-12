import cv2
import mediapipe as mp
import math
import os

# 初始化MediaPipe手部模型
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 初始化摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("无法获取摄像头画面")
        continue

    # 转换颜色空间BGR到RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 处理图像并检测手部
    results = hands.process(image)
    
    # 转换回BGR颜色空间以便OpenCV显示
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # 绘制手部特征点并检测手势
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 获取食指和拇指的坐标
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # 计算两点之间的距离
            distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
            
            # 获取手的左右属性
            hand_label = results.multi_handedness[0].classification[0].label
            
            # 根据左右手分别控制音量和亮度
            if hand_label == 'Left':
                # 左手控制音量
                if distance < 0.05:
                    os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 5)'")
                elif distance > 0.15:
                    os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 5)'")
                
                # 在画面上显示距离值和手属性
                cv2.putText(image, f'Left Hand - Volume', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # 右手控制亮度
                if distance < 0.05:
                    os.system("osascript -e 'tell application \"System Events\" to key code 145'")
                elif distance > 0.15:
                    os.system("osascript -e 'tell application \"System Events\" to key code 144'")
                
                # 在画面上显示距离值和手属性
                cv2.putText(image, f'Right Hand - Brightness', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 绘制食指和拇指之间的连接线
            height, width, _ = image.shape
            thumb_pixel = (int(thumb_tip.x * width), int(thumb_tip.y * height))
            index_pixel = (int(index_tip.x * width), int(index_tip.y * height))
            
            # 根据距离范围设置不同颜色
            line_color = (0, 255, 0)  # 默认绿色
            text_color = (0, 0, 255)  # 默认红色
            if distance < 0.05:
                line_color = (255, 0, 0)  # 红色表示音量减小
                text_color = (255, 255, 255)  # 白色文字
            elif distance > 0.15:
                line_color = (0, 0, 255)  # 蓝色表示音量增大
                text_color = (255, 255, 0)  # 黄色文字
            
            # 绘制更粗的连接线
            cv2.line(image, thumb_pixel, index_pixel, line_color, 4)
            
            # 在连线中间显示更醒目的距离数值
            mid_point = ((thumb_pixel[0] + index_pixel[0]) // 2, (thumb_pixel[1] + index_pixel[1]) // 2)
            cv2.putText(image, f'{distance:.2f}', mid_point, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 3)
            
            # 添加距离范围提示
            cv2.putText(image, 'Volume Down' if distance < 0.05 else 'Volume Up' if distance > 0.15 else 'Normal', 
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # 显示结果
    cv2.imshow('Hand Detection', image)
    
    # 按'q'键退出
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()