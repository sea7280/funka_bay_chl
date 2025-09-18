
噴火湾の海面クロロフィルデータ解析

データダウンロードサイト
https://oceancolor.gsfc.nasa.gov/

ダウンロードプロダクト
special, modis, chlorophyll, monthly, 4km

ディレクトリ構成
data: プロダクトデータ（.nc）
map: 東日本を中心とした広範囲マッピングファイル
map_zoom: 噴火湾周辺のマッピングファイル
src: ソースコード
txt: プロダクトデータからクロロフィル、座標データをテキスト化

ソースコード構成

プロダクトデータのテキスト化, 以後の処理はこのテキストから
\src\modis_to_txt.py

東日本を中心に広範囲マッピング
\src\modis_mapping.py

噴火湾のマッピング
\src\modis_mapping_zoom.py

噴火湾, 2月3月の平均値を算出, 年変動をプロットする
\src\modis_mean_plot.py