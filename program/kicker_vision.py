import cv2
import numpy as np

def track_ball(video_path):
    # 動画ファイルを読み込む
    cap = cv2.VideoCapture(video_path)

    # 軌跡を記録するための空リスト
    trajectory = []

    while True:
        # フレームを読み込む
        ret, frame = cap.read()
        if not ret:
            break  # 動画が終了したらループを抜ける

        # BGR色空間からHSV色空間へ変換
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # オレンジ色の範囲を定義（HSV色空間）(H,S,V)
        lower_orange = np.array([10, 60, 79])
        upper_orange = np.array([25, 75, 110])

        # マスクを作成してオレンジ色のみを抽出
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # マスクを使用して輪郭を見つける
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 最大の輪郭を見つける
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

            if radius > 10:  # ノイズを除外するための最小サイズ
                # 軌跡に中心点を追加
                trajectory.append((int(x), int(y)))

                # 軌跡を描画
                for i in range(1, len(trajectory)):
                    if trajectory[i - 1] is None or trajectory[i] is None:
                        continue
                    cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 0, 255), 5)

        # 結果を表示
        cv2.imshow('Frame', frame)

        # 'q'を押してウィンドウを閉じる
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # リソース解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "program/exp.mp4"  # 動画ファイルのパスを指定
    track_ball(video_path)
