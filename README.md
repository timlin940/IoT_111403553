# IoT_盲人行走輔助系統
作者:111403553 林祐霆

## 專案簡介

這個裝置利用樹梅派(Raspberry pi)代替使用者的眼睛，幫助盲人可以更加清楚的感知周遭的人、車等物品。裝置考慮到使用者的不方便，所以只需要確保裝置連上網、插上電，裝置就會開始運作。

## 專案軟件需求

- Pytohn 3.7.9
- gTTS 2.5.4
- Openvino_2022.3.2
- OpenCV 4.5.2-openvino
- numpy 1.19.5
### 軟體安裝流程
1.安裝openvino

> mkdir intel

> cd intel

> wget https://download.01.org/opencv/2019/openvinotoolkit/R3/l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz
 
 sudo apt install cmake

## 專案硬件需求

 - Raspiberry pi 4代主機板
 - SD Card 32GB (16GB may work)
 - Raspiberry pi camera
 - NCS2 神經運算棒
 - 5v行動電源 1 顆
 - usb-typeC充電線一條
 - 3.5mm耳機一條(喇叭)
