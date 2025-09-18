import netCDF4 as nc4
import pandas as pd
import numpy as np
import os
import glob
import math

def to_txt(path):
    
    with nc4.Dataset(path, "r") as nc:
        print(nc.groups)
        print(nc.groups['level-3_binned_data'].variables['chl_gsm'])
        print(nc)
        
        l3_group = nc.groups['level-3_binned_data']
        # 地理的範囲を取得
        lat_min = nc.getncattr('southernmost_latitude')
        lat_max = nc.getncattr('northernmost_latitude')
        lon_min = nc.getncattr('westernmost_longitude')
        lon_max = nc.getncattr('easternmost_longitude')
        resolution = nc.getncattr('spatialResolution')

        # データ読み込み
        bin_list = l3_group['BinList'][:]
        chl_data = l3_group['chl_gsm'][:]
        
        # 有効データのマスク
        valid_mask = (bin_list['nobs'] > 0) & (bin_list['weights'] > 0) & (chl_data['sum'] > 0)
        
        # データ抽出
        bin_nums = bin_list['bin_num'][valid_mask]
        weights = bin_list['weights'][valid_mask]
        chl_sum = chl_data['sum'][valid_mask]
        nobs = bin_list['nobs'][valid_mask]
        
        # 複数の平均計算方法をテスト
        print("=== データ構造分析 ===")
        print(f"総ビン数: {len(bin_nums)}")
        print(f"観測数の範囲: {nobs.min()} - {nobs.max()}")
        print(f"重みの範囲: {weights.min():.3f} - {weights.max():.3f}")
        print(f"合計値の範囲: {chl_sum.min():.3f} - {chl_sum.max():.3f}")
    
    # 重み付き平均を計算
    chl_weighted = chl_sum / weights
    
    # 座標変換
    lats, lons = bin_to_coords(bin_nums)
    print(f"緯度範囲: {lats.min():.2f} - {lats.max():.2f}")
    print(lats.shape)
    print(f"経度範囲: {lons.min():.2f} - {lons.max():.2f}")
    print(lons.shape)

    df = pd.DataFrame({
        'bin_number': bin_nums,
        'latitude': lats,
        'longitude': lons,  # 修正: latsではなくlons
        'chlorophyll': chl_weighted
    })
    
    return df
    
# グローバルなルックアップテーブル（初回のみ計算）
_lookup_tables = None

def init_lookup_tables():
    """ルックアップテーブル初期化（1回のみ実行）"""
    global _lookup_tables
    if _lookup_tables is not None:
        return _lookup_tables
    
    print("ルックアップテーブル初期化中...")
    
    # 各rowの列数を事前計算
    cols_per_row = np.zeros(4320, dtype=int)
    for row in range(4320):
        # 修正: 南極から北極への座標系に統一
        lat = -90.0 + (row + 0.5) * (180.0 / 4320)
        cols_per_row[row] = max(1, int(8640 * abs(math.cos(math.radians(lat))) + 0.5))
    
    # 各rowの開始bin番号を累積計算
    row_starts = np.zeros(4321, dtype=int)
    row_starts[0] = 1
    row_starts[1:] = np.cumsum(cols_per_row) + 1
    
    _lookup_tables = {
        'cols_per_row': cols_per_row,
        'row_starts': row_starts
    }
    
    print("初期化完了")
    return _lookup_tables

def bin_to_coords(bin_nums):
    """
    高速化されたbin_numから緯度・経度への変換
    """
    tables = init_lookup_tables()
    row_starts = tables['row_starts']
    cols_per_row = tables['cols_per_row']
    
    bin_nums = np.asarray(bin_nums)
    
    # vectorized row検索
    rows = np.searchsorted(row_starts[1:], bin_nums, side='right')
    
    # 緯度計算（vectorized）
    # MODIS Level-3では南極から北極へ行番号が増加
    lats = -90.0 + (rows + 0.5) * (180.0 / 4320)
    
    # 経度計算（vectorized）
    row_start_bins = row_starts[rows]
    cols_in_rows = cols_per_row[rows]
    cols = bin_nums - row_start_bins
    lons = -180.0 + (cols + 0.5) * (360.0 / cols_in_rows)
    
    return lats, lons

def main():
        
    data_dir = "C:\\Users\\sakum\\Desktop\\abe_paper\\data"

    # *test.txtパターンに一致するファイルパスを再帰的に検索
    pattern = os.path.join(data_dir, "**", "*.nc")
    # glob.globを使って再帰的に検索(recursive=True)
    matching_files = glob.glob(pattern, recursive=True)

    for path in matching_files:

        save_dir = f"C:\\Users\\sakum\\Desktop\\abe_paper\\txt\\{path.split('_')[-1][:4]}"
        savepath = f"{save_dir}\\{path.split('\\')[-1].replace('.nc','.txt')}"
        
        txt_df = to_txt(path)
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        txt_df.to_csv(savepath, sep='\t', index=False)
        print(f"end: {path}")

if __name__ == "__main__":
    
    main()
    test = "C:\\Users\\sakum\\Desktop\\abe_paper\\data\\AQUA_MODIS.20110501_20110531.L4b.MO.GSM.x.nc"
    
    #df = to_txt(test)
    #df.to_csv("C:\\Users\\sakum\\Desktop\\abe_paper\\test.txt", sep='\t', index=False)