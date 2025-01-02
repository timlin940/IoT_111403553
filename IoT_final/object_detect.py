import cv2
import numpy as np
from openvino.runtime import Core
from coco_classes_tw import COCO_CLASSES
import voice_output as vo
import time
# 載入 OpenVINO ssdlite)mobilenet_v2 模型
model_path = "/home/YaHaaaa/IoT_final/ssdlite_mobilenet_v2/FP32/ssdlite_mobilenet_v2.xml"  # 模型的 IR 格式 (.xml)
core = Core()
model = core.read_model(model=model_path)
compiled_model = None
# 確認輸入形狀
print("模型輸入資訊")

running = False
cap = None
def start():
    last_time = 0
    last_alert = ""
    global complied_model
    compiled_model = core.compile_model(model=model_path, device_name="MYRIAD")#openvino加速棒
    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    input_shape = input_layer.shape
    
    global running
    running = True
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("無法打開相機")
            vo.play_tts("無法打開相機")
            return
# 開啟攝影機
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = time.time()
        # 預處理
        input_height, input_width = input_shape[1],input_shape[2]
        resized_frame = cv2.resize(frame, (input_height, input_width))  # 改變尺寸
        preprocessed_frame = resized_frame.astype(np.float32)
        preprocessed_frame = preprocessed_frame.transpose(2,0,1)
        input_tensor = np.expand_dims(preprocessed_frame, axis=0)
        
        # 推論
        results = compiled_model([input_tensor])

        # 提取檢測結果（假設輸出層名稱為 "detection_out"）
        output_layer = compiled_model.output(0)  # 假設第一個輸出層
        detections = results[output_layer]
        
        # 遍歷檢測結果
        for detection in detections[0][0]:  # 第一批次的結果
            confidence = float(detection[2])  # 信心分數
            if confidence > 0.8:  # 設置信心分數閾值
                class_id = detection[1] # 類別
                object_name = COCO_CLASSES.get(class_id, "未知物體")
                alert_message = f"偵測到：{object_name}"
                if current_time - last_time >=1 and last_alert != alert_message:
                    vo.play_tts(alert_message)
                    last_time = current_time
                    last_alert = alert_message
def stop():
    global compiled_model  # 声明为全局变量
    global running
    global cap
    running = False
    if cap is not None:
        cap.release()
        cap = None
    cv2.destroyAllWindows()
    if compiled_model is not None:
        del compiled_model #刪除編譯模型
        complied_model = None