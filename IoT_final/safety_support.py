from openvino.runtime import Core
import cv2
import numpy as np
import time
import voice_output as vo
#控制start、stop
running = False
#家仔模型
model_path = "/home/YaHaaaa/IoT_final/ssdlite_mobilenet_v2/FP32/ssdlite_mobilenet_v2.xml"
core = Core()
compiled_model = None
cap = None
def calculate_distance(object_height_px, actual_height,FOCAL_LENGTH):
    """計算物體與相機的距離"""
    if object_height_px > 0 and actual_height is not None:
        return round((actual_height * FOCAL_LENGTH) / object_height_px)
    return -1  # 無法計算距離
def start():
    object_sizes = {
    1:("人",1.6),
    2:("汽車",1.5)
    
    } # 添加完整 COCO 類別
    FOCAL_LENGTH = 200
    last_alert = ""
    last_detection_time = 0
    global complied_model
    compiled_model = core.compile_model(model=model_path, device_name="MYRIAD")#openvino加速棒
    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)
    input_shape = input_layer.shape
    
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 45)
        if not cap.isOpened():
            print("無法打開相機")
            vo.play_tts("無法打開相機")
            return
    
    global running 
    running = True
    vo.play_tts("打開相機")
    frame_skip = 5 # 5s 1 times
    frame_count = 0
    while running:
            ret, frame = cap.read()
            current_time = time.time()
            if not ret:
                print("無法讀取影像")
                break
            frame_count+=1
            if frame_count % frame_skip != 0:
                continue
            # 模型推論
            if current_time - last_detection_time > 1:
                # 預處理
                input_height, input_width = input_shape[1],input_shape[2]
                input_image = cv2.resize(frame, (input_width, input_height))
                input_image = input_image.transpose(2, 0, 1)# HWC -> CHW
                input_image = np.expand_dims(input_image, axis=0)
                input_image = input_image.astype(np.float32)
                
                # 推論
                results = compiled_model([input_image])[output_layer]
                
                # 解析推論結果
                height, width, _ = frame.shape  # 取得畫面高度和寬度
                frame_center = width / 2  # 計算畫面中心點
                detections = []
                
                for detection in results[0][0]:
                    confidence = detection[2]
                    if confidence > 0.7:  # 信心門檻
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
                min_dis = 0
                for detection in detections:
                    class_id, confidence, xmin, ymin, xmax, ymax = detection
                    # 計算邊界框的中心點
                    box_center = (xmin + xmax) / 2
                    # 判斷物品在畫面中的位置
                    position = ""
                    if box_center < frame_center-5:
                        position = "左前方"
                    elif box_center > frame_center+5:
                        position = "右前方"
                    else:
                        position = "前方"
                    
                    if class_id in object_sizes:
                        obj_name = object_sizes.get(class_id)  # 取得名稱和大小
                        obj_h = ymax - ymin  # 計算框的高度 (像素)
                        obj_dis = calculate_distance(obj_h, obj_name[1],FOCAL_LENGTH)  # 計算距離
                        if obj_dis < min_dis:
                            min_dis = obj_dis
                            nearest_alert = f"有{obj_name[0]}在{position}, 距離約 {obj_dis:.2f} 公尺"
                if nearest_alert and nearest_alert != last_alert:
                    print(nearest_alert)
                    vo.play_tts(nearest_alert)
                    last_alert = nearest_alert
            
def stop():
    global compiled_model  # 確立為全域變數
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
