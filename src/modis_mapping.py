
#modisのマッピング処理



import pandas as pd
import numpy as np
import os
import glob
import pygmt

pygmt.config(FONT="12p,Helvetica,black")  # フォントサイズ、種類、色
pygmt.config(FONT_LABEL="12p,Helvetica,black")  # フォントサイズ、種類、色
    
def mapping(path):
    
    #データ読み込み
    df = pd.read_table(path)
    
    print(df)
    
    #保存先設定
    save_dir = f"C:\\Users\\sakum\\Desktop\\abe_paper\\map\\{path.split("_")[-1][:4]}"
    savepath = f"{save_dir}\\{path.split("\\")[-1].replace(".txt",".tif")}"
    #savepath = "C:\\Users\\sakum\\Desktop\\abe_paper\\test.png" ##test用
    
    #プロット領域設定
    min_lat = 30
    max_lat = 49
    min_lon = 130
    max_lon = 158
    area = [min_lon, max_lon, min_lat, max_lat]
    
    #マッピング
    fig = pygmt.Figure()
    fig.basemap(region=area, projection="M10c", frame=["xa10f5", "ya5f5"])    
    
    pygmt.makecpt(series=[0, 5, 0.01], cmap="jet", background="a",continuous=True)
    #データプロット
    fig.plot(
        x=df['longitude'].values,
        y=df['latitude'].values, 
        fill=df["chlorophyll"].values,  # z値に基づいて色付け
        style="c0.017c",  # 三角形のマーカー、サイズ0.5cm
        cmap=True,  # カラーマップを適用
    )
    #沿岸域のプロット
    fig.coast(shorelines=True, land="lightgray")
    
        # カラーバーを追加
    fig.colorbar(
        frame=["xa0.5+lchlorophyll (mg/m³)"],
        position="JMR+w5c/0.3c+o0.2c/0c+e"
    )
    #保存先がなければディレクトリ作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    #保存
    fig.savefig(savepath, dpi=300)
    
    
def main():
        
    data_dir = "C:\\Users\\sakum\\Desktop\\abe_paper\\txt\\"

    # *test.txtパターンに一致するファイルパスを再帰的に検索
    pattern = os.path.join(data_dir, "**", "*.txt")
    # glob.globを使って再帰的に検索(recursive=True)
    matching_files = glob.glob(pattern, recursive=True)

    #1ファイルごとに処理
    for path in matching_files:
        #マッピング
        mapping(path)
        print(f"end: {path}")

if __name__ == "__main__":
    
    main()
    
    #test = "C:\\Users\\sakum\\Desktop\\abe_paper\\test.txt"
    #mapping(test)