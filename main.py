import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    # --- 1. 基本畫面設定 ---
    page.title = "YouTube 音訊下載神器"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # --- 2. 建立 UI 元件 ---
    title_text = ft.Text("YT 音訊下載器", size=24, weight="bold")
    url_input = ft.TextField(label="請貼上 YouTube 網址", width=300)
    status_text = ft.Text("準備就緒", color="blue")
    
    # --- 3. 定義按鈕點擊後的下載邏輯 ---
    def download_audio(e):
        if not url_input.value:
            status_text.value = "請先輸入網址！"
            status_text.color = "red"
            page.update()
            return

        status_text.value = "下載中，請稍候..."
        status_text.color = "orange"
        # 鎖定按鈕避免重複點擊
        download_btn.disabled = True
        page.update()

        # 判斷儲存路徑：如果在 Android 手機上，就存到內建的 Download 資料夾
        # 如果在電腦上測試，就存到程式執行的當下目錄
        if 'ANDROID_STORAGE' in os.environ:
            save_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'
        else:
            save_path = '%(title)s.%(ext)s'

        # yt-dlp 的下載設定 (指定優先抓取最佳音質的 m4a)
        ydl_opts = {
            'format': 'm4a/bestaudio/best', 
            'outtmpl': save_path,           
            'quiet': True,                  # 隱藏終端機不必要的雜訊輸出
        }

        try:
            # 執行下載
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])
            
            status_text.value = "下載完成！請到資料夾查看"
            status_text.color = "green"
            url_input.value = "" # 清空網址欄位方便下次輸入
        except Exception as ex:
            status_text.value = f"發生錯誤：{str(ex)}"
            status_text.color = "red"
        
        # 恢復按鈕狀態
        download_btn.disabled = False
        page.update()

    download_btn = ft.ElevatedButton("開始下載", on_click=download_audio)

    # --- 4. 把元件加入畫面中 ---
    page.add(
        title_text,
        url_input,
        download_btn,
        status_text
    )

# 啟動 App
ft.app(target=main)