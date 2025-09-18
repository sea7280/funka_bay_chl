
#modisの2月、3月の平均値プロット

import pandas as pd
import numpy as np
import os
import glob
import pygmt
import matplotlib.pyplot as plt

#フォント設定
plt.rcParams['font.family'] = 'Times New Roman' # font familyの設定
plt.rcParams["font.size"] = 18 # 全体のフォントサイズが変更されます。
#plt.rcParams['font.weight'] = 'bold'
#軸設定
plt.rcParams['xtick.direction'] = 'in' #x軸の目盛りの向き
plt.rcParams['ytick.direction'] = 'in' #y軸の目盛りの向き
plt.rcParams['ytick.right'] = True  #y軸の右部目盛り
#凡例設定
plt.rcParams["legend.fancybox"] = False  # 丸角OFF
plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
plt.rcParams["legend.edgecolor"] = 'black'  # edgeの色を変更
plt.rcParams["legend.markerscale"] = 2 #markerサイズ
plt.rcParams["legend.fontsize"] = 16  # 凡例フォントサイズ


def extract_data(path):

    df = pd.read_table(path)
    
    #指定範囲でフィルタリング
    df = df[(df['latitude'] >= 42.1) & (df['latitude'] <= 42.6) &
            (df['longitude'] >= 140.2) & (df['longitude'] <= 140.95)].reset_index(drop=True)
    
    #細かい箇所の除去
    df = df[~((df['latitude'] >= 42.55) & (df['longitude'] >= 140.8))].reset_index(drop=True)
    
    return df

#単体月のプロット
def plot_mean(chl_list, month):
    
    years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    
    plt.figure(figsize=(9, 4), dpi=300)
    plt.plot(years, chl_list, marker='o', color='black', linewidth=2)

    plt.ylim([0,5])
    plt.xlabel('Year')
    plt.ylabel('chlorophyll (mg/m$^3$)')
    #plt.xticks(ticks=np.arange(1, 13), labels=years)

        # レイアウトの調整
    plt.subplots_adjust(
                        left=0.1,     # 左側の余白
                        bottom=0.15,   # 下側の余白
                        right=0.95,   # 右側の余白
                        top=0.95,     # 上側の余白)  # サブプロット間の間隔を調整
    )

    savepath = f"C:\\Users\\sakum\\Desktop\\abe_paper\\chlorophyll_mean_{month}.png"
    plt.savefig(savepath)
    plt.close()

#複数月をまとめてプロット
def plot_mean_same(chl_list1, chl_list2, month):
    
    years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    
    plt.figure(figsize=(9, 4), dpi=300)
    plt.plot(years, chl_list1, marker='o', color='blue', linewidth=2, label=month[0])
    plt.plot(years, chl_list2, marker='o', color='green', linewidth=2, label=month[1])

    plt.ylim([0,5])
    plt.xlabel('Year')
    plt.ylabel('chlorophyll (mg/m$^3$)')
    plt.legend()
        # レイアウトの調整
    plt.subplots_adjust(
                        left=0.1,     # 左側の余白
                        bottom=0.15,   # 下側の余白
                        right=0.95,   # 右側の余白
                        top=0.95,     # 上側の余白)  # サブプロット間の間隔を調整
    )

    savepath = f"C:\\Users\\sakum\\Desktop\\abe_paper\\chlorophyll_mean_{month[0]}_{month[1]}.png"
    plt.savefig(savepath)
    plt.close()
    
def main():
        
    data_dir = "C:\\Users\\sakum\\Desktop\\abe_paper\\txt\\"

    # *test.txtパターンに一致するファイルパスを再帰的に検索
    pattern = os.path.join(data_dir, "**", "*.txt")
    # glob.globを使って再帰的に検索(recursive=True)
    matching_files = glob.glob(pattern, recursive=True)
    
    #2月と3月に絞り込み
    feb_files = [path for path in matching_files if ("0201_" in path)]
    mar_files = [path for path in matching_files if ("0301_" in path)]

    feb_chl_means = []
    mar_chl_means = []
    
    for path in feb_files:
        
        df = extract_data(path)
        chl_mean = df['chlorophyll'].mean()
        feb_chl_means.append(chl_mean)
        print(f"2月平均値: {chl_mean:.2f} - {path}")
        
    for path in mar_files:
        
        df = extract_data(path)
        chl_mean = df['chlorophyll'].mean()
        mar_chl_means.append(chl_mean)
        print(f"3月平均値: {chl_mean:.2f} - {path}")
        
    plot_mean(feb_chl_means, "Feb")
    plot_mean(mar_chl_means, "Mar")
    
    month_list = ["Feb", "Mar"]
    plot_mean_same(feb_chl_means, mar_chl_means, month_list)
    
    years = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
    
    #平均値のテキスト保存
    result = pd.DataFrame({
        "year": years,
        "feb":feb_chl_means,
        "mar":mar_chl_means
    })
    
    result.to_csv("C:\\Users\\sakum\\Desktop\\abe_paper\\chl_mean_result.txt", sep='\t', index=False)
    
    
if __name__ == "__main__":
    
    main()
    path = "C:\\Users\\sakum\\Desktop\\abe_paper\\txt\\2023\\AQUA_MODIS.20230301_20230331.L4b.MO.GSM.x.txt"
    
    #extract_data(path)
    