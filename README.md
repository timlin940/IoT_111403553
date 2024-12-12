# IoT_盲人行走輔助系統
作者:111403553 林祐霆

---

## 專案簡介
這個裝置利用樹梅派(Raspberry pi)代替使用者的眼睛，幫助盲人可以更加清楚的感知周遭的人、車等物品。裝置考慮到使用者的不方便，所以只需要確保裝置連上網、插上電，裝置就會開始運作。

---

## 專案軟件需求
- Python 3.7.9
- gTTS 2.5.4
- Openvino_2022.3.2
- OpenCV 4.5.2-openvino
- numpy 1.19.5
  
### 軟體安裝流程
1. 安裝CMack、OpenCv、OpenVino等套件(再改)
 [Raspberry Pi OpenVINO 安裝教學](https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)

2. 安裝物件辨識模型：
   ```
   wget https://download.01.org/opencv/2021/openvinotoolkit/2021.2/open_model_zoo/models_bin/3/person-vehicle-bike-detection-crossroad-0078/FP16/person-vehicle-bike-detection-crossroad-0078.bin
3. 設定啟動文件:
- 編輯啟動腳本：
   ```
    nano /home/user/autostart.sh
- 在腳本中添加以下內容，將路徑替換為實際路徑：
  ```
  #!/bin/bash
  source /home/user/openvino_dist/bin/setupvars.sh
  python3 /path/to/code.py
- 給腳本添加執行權限：
  ```
  chmod +x /home/user/autostart.sh
## 專案硬件需求
 - Raspiberry pi 4代主機板
 - SD Card 32GB (16GB may work)
 - Raspiberry pi camera
 - NCS2 神經運算棒
 - 5v行動電源 1 顆
 - usb-typeC充電線一條
 - 3.5mm耳機一條(喇叭)
## 可以改進的部分

## 影片demo

## 參考網址
