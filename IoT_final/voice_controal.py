import threading
import speech_recognition as sr
import voice_output as vo
import safety_support as ss
import object_detect as od
import sending_Line as sl
#  s_safety_support 、is_object_runnung的運行狀態
is_safety_running = False
is_object_running = False
t = False

# 運作safety_support的邏輯
def run_safety_support():
    global is_safety_running
    is_safety_running = True
    print("[INFO] Safety Support Thread Started.")
    while is_safety_running:
        ss.start()  # 開始
    ss.stop()  # 停止
    
    print("[INFO] Safety Support Thread Stopped.")
def run_object_detect():
    global is_object_running
    is_object_running = True
    while is_object_running:
        od.start()
    od.stop()
    
# 語音指令區域
def voice_control():
    global is_safety_running,t,is_object_running
    recognizer = sr.Recognizer()
    if not t :
        vo.play_tts("請說話...")
        t = True
    with sr.Microphone(device_index=2) as source:
        try:
            audio = recognizer.listen(source)  
            # 轉文字
            text = recognizer.recognize_google(audio, language="zh-TW")
            print(f"辨識到的文字: {text}")

            if text == "啟動行人輔助":
                if not is_safety_running:
                    vo.play_tts("啟動行人輔助")
                    od.stop()
                    threading.Thread(target=run_safety_support, daemon=True).start()  # 啟動safety_support的序列
                    print("[INFO] Safety Support Thread Launched.")
                else:
                    vo.play_tts("行人輔助已經啟動")

            elif text == "關閉行人輔助":
                if is_safety_running:
                    is_safety_running = False  # 停止 safety_support
                    ss.stop()
                    vo.play_tts("關閉行人輔助")
                else:
                    vo.play_tts("行人輔助已經關閉")
            elif text == "啟動物件偵測":
                if not is_object_running:
                    vo.play_tts("啟動物件偵測")
                    ss.stop()  # 停止 safety_support，確保NSC2資源不衝突
                    threading.Thread(target=run_object_detect, daemon=True).start()  
                    print("[INFO] Object Detect Thread Launched.")
                else:
                    vo.play_tts("物件偵測已經啟動")
            elif text == "關閉物件偵測":
                if is_object_running:
                    is_object_running = False  # 停止 object_detect
                    od.stop()
                    vo.play_tts("關閉物件偵測")
                else:
                    vo.play_tts("物件偵測已經關閉")
            elif text == "我出發了":
                sl.sending("我出發了")
                vo.play_tts("已傳送訊息")
            elif text == "我已經安全到達":
                sl.sending("我已經安全到達")
                vo.play_tts("已傳送訊息")
                
        except sr.UnknownValueError:
            print("無法辨識語音")
        except sr.RequestError as e:
            vo.play_tts(f"語音異常: {e}")

# 主程式
if __name__ == "__main__":
    while True:
        voice_control()
