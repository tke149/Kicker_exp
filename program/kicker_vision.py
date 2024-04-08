import cv2
import numpy as np
import threading
import sys
import csv

# グローバル変数
is_running = True
trajectory = []  # 軌跡を記録するリスト

def wait_for_quit_command():
    global is_running
    while True:
        if input("Type 'quit' to exit: ") == "quit":
            is_running = False
            break

def process_video(video_path, output_file, output_file_csv):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    
    # 出力動画の設定
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # HSV色空間でのオレンジ色の範囲
    lower_orange = np.array([5, 50, 50])
    upper_orange = np.array([15, 255, 255])

    previous_center = None
    velocities = []

    while is_running:
        ret, frame = video.read()
        if not ret:
            break
        
        # HSVに変換
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        # 輪郭抽出
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            
            if radius > 10:
                center = (int(x), int(y))
                trajectory.append(center)
                
                # 軌跡を描画
                for i in range(1, len(trajectory)):
                    if trajectory[i - 1] is None or trajectory[i] is None:
                        continue
                    cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 0, 255), 2)
                
                if previous_center is not None:
                    # 速度計算（ピクセル/フレーム）
                    velocity = ((center[0] - previous_center[0]) ** 2 + (center[1] - previous_center[1]) ** 2) ** 0.5
                    velocities.append(velocity)
                
                previous_center = center
        
        out.write(frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # CSVに保存
    with open(output_file_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        for velocity in velocities:
            writer.writerow([velocity])
    
    video.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "program/exp4.mp4"
    output_file = "output.mp4"
    output_file_csv = "velocities.csv"
    
    thread = threading.Thread(target=wait_for_quit_command)
    thread.start()
    
    process_video(video_path, output_file, output_file_csv)
