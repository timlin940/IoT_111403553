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
1. 安裝CMack
    ```
    cd ~/
    wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4.tar.gz
    tar xvzf cmake-3.14.4.tar.gz
    cd ~/cmake-3.14.4
    ./bootstrap
    make -j4
    sudo make install
2. 安裝OpenCV
    ```
    cd ~/
    sudo apt install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libatlas-base-dev python3-scipy
    git clone --depth 1 --branch 4.5.2-openvino https://github.com/opencv/opencv.git
    cd opencv && mkdir build && cd build
    cmake –DCMAKE_BUILD_TYPE=Release –DCMAKE_INSTALL_PREFIX=/usr/local ..
    make -j4
    sudo make install
3. 安裝OpenVino
    ```
      wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.3.2/l_openvino_toolkit_debian9_2022.3.2.9279.e2c7e4d7b4d_armhf.tgz
- 解壓縮
  ```
  tar -xvf l_openvino_toolkit_debian9_2022.3.2.9279.e2c7e4d7b4d_armhf.tgz 
- 執行 OpenVINO 提供的腳本來安裝所需依賴項：
  ```
  sudo /home/user/intel/openvino_2022.3.2/install_dependencies/install_openvino_dependencies.sh
- 執行以下腳本來設置 USB 規則，確保 Movidius NCS2 可用：
  ```
  sudo /home/YaHaaaa/intel/openvino_2022.3.2/install_dependencies/install_NCS_udev_rules.sh

4. 安裝物件辨識模型：
   ```
   wget https://download.01.org/opencv/2021/openvinotoolkit/2021.2/open_model_zoo/models_bin/3/person-vehicle-bike-detection-crossroad-0078/FP16/person-vehicle-bike-detection-crossroad-0078.bin
5. 設定啟動文件:
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
- 因為播放聲音而讓畫面停頓的部分可以想辦法優化
- 可以做讓相機更加平穩的支架
## 影片demo

## 參考網址
