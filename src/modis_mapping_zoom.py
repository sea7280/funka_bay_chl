
#対象海域に絞り込んでマッピング
#対象は2月と3月


import pandas as pd
import numpy as np
import os
import glob
import pygmt


pygmt.config(
    FONT="12p,Times-Roman,black",
    FONT_LABEL="12p,Times-Roman,black",
    FORMAT_GEO_MAP="ddd.xF",           # 十進度表示
    MAP_DEGREE_SYMBOL="degree",        # 度記号の形式
)
    
def mapping(path):
    df = pd.read_table(path)
    
    print(df)
    
    save_dir = f"C:\\Users\\sakum\\Desktop\\abe_paper\\map_zoom\\"
    savepath = f"{save_dir}\\{path.split("\\")[-1].replace(".txt",".tif")}"
    #savepath = "C:\\Users\\sakum\\Desktop\\abe_paper\\test.png" ##test用
    
    min_lat = 42
    max_lat = 42.7
    min_lon = 140.2
    max_lon = 141.2
    area = [min_lon, max_lon, min_lat, max_lat]
    
    fig = pygmt.Figure()
    fig.basemap(region=area, projection="M10c", frame=["xa0.2f0.1", "ya0.2f0.1"])    
    
    pygmt.makecpt(series=[0, 5, 0.01], cmap="jet", background="a",continuous=True)
    
    #data_array = pygmt.xyz2grd(
    #    x=df['longitude'], 
    #    y=df['latitude'], 
    #    z=df["chlorophyll"], 
    #    spacing= "0.05/0.05",
    #    region=[min_lon-0.25, max_lon+0.25, min_lat-0.25, max_lat+0.25]
    #)
    #fig.grdimage(grid=data_array, region=area)
    fig.plot(
        x=df['longitude'].values,
        y=df['latitude'].values, 
        fill=df["chlorophyll"].values,  # z値に基づいて色付け
        style="c0.65c",  # 三角形のマーカー、サイズ0.5cm
        cmap=True,  # カラーマップを適用
    )
    
    fig.coast(shorelines=True, land="lightgray")
    
        # カラーバーを追加
    fig.colorbar(
        frame=["xa0.5+lchlorophyll (mg/m³)"],
        position="JBC+w10c/0.3c+e"
    )
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    fig.savefig(savepath, dpi=300)
    
    
def main():
        
    data_dir = "C:\\Users\\sakum\\Desktop\\abe_paper\\txt\\"

    # *test.txtパターンに一致するファイルパスを再帰的に検索
    pattern = os.path.join(data_dir, "**", "*.txt")
    # glob.globを使って再帰的に検索(recursive=True)
    matching_files = glob.glob(pattern, recursive=True)
    
    #2月と3月に絞り込み
    matching_files = [path for path in matching_files if ("0201_" in path) or ("0301_" in path)]

    for path in matching_files:

        mapping(path)
        print(f"end: {path}")

if __name__ == "__main__":
    
    main()
    
    #test = "C:\\Users\\sakum\\Desktop\\abe_paper\\test.txt"
    #mapping(test)