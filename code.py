from openvino.runtime import Core
import cv2
import numpy as np
import time
from gtts import gTTS
import os

def play_tts(text):#播放語音
    tts = gTTS(text=text, lang='zh-CN')
    tts.save("alert.mp3")
    os.system("mpg321 alert.mp3")
    os.remove("alert.mp3")

play_tts("啟動中")
# 初始化 OpenVINO
model_path = "/home/YaHaaaa/Downloads/person-vehicle-bike-detection-crossroad-0078.xml"
core = Core()
compiled_model = core.compile_model(model=model_path, device_name="MYRIAD")#設定NCS2裝置
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)
input_shape = input_layer.shape  # e.g., [1, 3, 300, 300]

object_sizes = {#設定物件高度
    1:("人",1.7),#1.7公尺
    2:("汽車",1.5)#1.5公尺
    
} 
FOCAL_LENGTH = 300
last_alert = ""
# 打開相機
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("無法打開相機")
    play_tts("無法打開相機")
    exit()
    
play_tts("打開相機")
# 設置時間條件
last_detection_time = 0
def calculate_distance(object_height_px, actual_height):#估算距離
    """計算物體與相機的距離"""
    if object_height_px > 0 and actual_height is not None:
        return round((actual_height * FOCAL_LENGTH) / object_height_px)
    return -1  # 無法計算距離

try:
    while True:
        ret, frame = cap.read()
        current_time = time.time()
        if not ret:
            print("無法讀取影像")
            break

        # 模型推論 解省效能  1秒後才推論
        if current_time - last_detection_time > 1:
            # 調整影像大小並進行預處理
            input_image = cv2.resize(frame, (input_shape[3], input_shape[2]))
            input_image = input_image.transpose(2, 0, 1)  # HWC to CHW
            input_image = np.expand_dims(input_image, axis=0)  # 增加 batch 維度
            results = compiled_model([input_image])[output_layer]
            last_detection_time = current_time
            # 解析推論結果
            height, width, _ = frame.shape  # 取得畫面高度和寬度
            frame_center = width / 2  # 計算畫面中心點
            detections = []
            
            for detection in results[0][0]:
                confidence = detection[2]
                if confidence > 0.65:  # 信心門檻 
                    xmin, ymin, xmax, ymax = (
                        int(detection[3] * frame.shape[1]),
                        int(detection[4] * frame.shape[0]),
                        int(detection[5] * frame.shape[1]),
                        int(detection[6] * frame.shape[0]),
                    )
                    class_id = detection[1]
                    detections.append((class_id, confidence, xmin, ymin, xmax, ymax))
            # 將偵測結果可視化
            nearest_alert = None
            min_dis = float('inf')
            for detection in detections:
                class_id, confidence, xmin, ymin, xmax, ymax = detection
                 # 計算邊界框的中心點
                box_center = (xmin + xmax) / 2
                # 判斷物品在畫面中的位置
                position = ""
                if box_center < frame_center:
                    position = "左前方"
                elif box_center > frame_center:
                    position = "右前方"
                else:
                    position = "前方"
                
                if class_id in object_sizes:
                    obj_name = object_sizes.get(class_id)  # 取得名稱和大小
                    obj_h = ymax - ymin  # 計算框的高度 (像素)
                    obj_dis = calculate_distance(obj_h, obj_name[1])  # 計算距離
                    if obj_dis < min_dis:#判斷距離更近的物體
                        min_dis = obj_dis
                        nearest_alert = f"有{obj_name[0]}在{position}, 距離約 {obj_dis:.2f} 公尺"
                # 添加標註文字 (名稱、信心值和距離)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    text = (f" {obj_name[0]} Confidence:{confidence:.2f} ")
                    cv2.putText(frame,text, (xmin, ymin + 15),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            if nearest_alert and nearest_alert != last_alert:
                print(nearest_alert)
                play_tts(nearest_alert)
                last_alert = nearest_alert
                                 
            # 顯示影像
            cv2.imshow("Detection", frame)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists("alert.mp3"):
        os.remove("alert.mp3")
