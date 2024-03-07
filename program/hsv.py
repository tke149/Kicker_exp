import cv2
import pandas as pd
import numpy as np
 
picture_filename = "program/color.jpg"
Excel_filename = "program/HSV.xlsx"
num = 10
 
def Calc_HSV(R, G, B):
    Max = max(R, G, B)
    Min = min(R, G, B)
 
    #グレースケール画像の時RGBは同じ値。不定形によるNaNエラーの回避？の想定。
    if R == G == B:
        if Max == 255:#真っ白の時
            return 0, 0, 100
        if Max == 0:#真っ黒の時
            return 0, 0, 0
 
    try:
        if R == Max:#Rが最大の時
            H = int(60 * (G - B) / (Max - Min))
        if G == Max:#Gが最大の時
            H = int(60 * (B - R) / (Max - Min) + 120)
        if B == Max:#Bが最大の時
            H = int(60 * (R - G) / (Max - Min) + 240)
        if H < 0:   #Hが負の時+360
            H += 360
    except :#passではなく、何かしらの処理はしたほうが良い
        pass
 
    S = int(100 * (Max - Min) / Max)
    V = int(100 * Max / 255)
 
    return H, S, V
 
def onMouse(event, x, y, flags, params):
    global value, count #グローバル変数の利用
    
    if event == cv2.EVENT_LBUTTONDOWN:#左クリックがされたら
        count += 1
        crop_img = img[[y], [x]]
        B = crop_img.T[0].flatten().mean()#返り値はBGRの順番
        G = crop_img.T[1].flatten().mean()
        R = crop_img.T[2].flatten().mean()
 
        H, S, V = Calc_HSV(R, G, B)#自作関数の利用
        value.append([R, G, B, H, S, V])
            
        print("{}回目, R: {}, G: {}, B: {}, H: {}, S: {}, V: {}".format(count, R, G, B, H, S, V))
 
        if num <= count:#一定回数後にExcelに出力
            Print_Excel()
            cv2.destroyAllWindows()
 
def Print_Excel():#出力内容の決定
    df = pd.DataFrame([rows for rows in value])
    df.columns = ['R', 'G', 'B' ,'H', 'S', 'V']#列の設定
    df.index = [i for i in range(1, num + 1)]  #行の設定
    df.to_excel(Excel_filename)                #Excelへ出力
    df
 
    
if __name__ == "__main__":#メイン関数
    value = []#RGB, HSVの値の格納用配列
    count = 0
    img = cv2.imread(picture_filename, cv2.IMREAD_COLOR)
    window_name = 'img'
    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, onMouse)
    cv2.waitKey(0)