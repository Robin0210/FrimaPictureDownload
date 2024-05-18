import urllib.request
import urllib.error
import time
import sys
import os
import datetime as dt
import json


#####################################################################################################
# 変数
#####################################################################################################

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
url_base = 'https://static.mercdn.net/item/detail/orig/photos/'
suffix_jpg = '.jpg'
read_file_name = "ItemIdList.txt"
option_name_sale = "販売"
option_name_purchase = "購入"

#####################################################################################################
# 関数
#####################################################################################################

# 設定ファイル読込み処理
def loadConfig():
    with open('config.json') as f:
        config = json.load(f)
    return config

# パラメータチェック処理
# 0:販売、1:購入
def chkParam(option):
    if option == "0":
        return True
    if option == "1":
        return True
    return False

# ダウンロードフォルダ作成処理
def createDownloadPath(option):

    # プログラム実行日（yyyyMMdd）を取得
    dt_now = dt.datetime.now().strftime('%Y%m%d')

    dir_name = ""
    if option == "0":
        dir_name = option_name_sale + "_" + dt_now
    elif option == "1":
        dir_name = option_name_purchase + "_" + dt_now
    download_path = os.path.join(download_base, dir_name)

    # ダウンロードファイルの格納先の存在確認
    if not os.path.exists(download_path):
        # フォルダを作成
        os.makedirs(download_path)
        print("[INFO] ダウンロードファイルの格納先フォルダを作成しました。")

    return download_path

# リスト読み込み処理
def readList():
    with open(read_file_name) as read_list:
        list = read_list.read().splitlines()
        return list

# 画像ファイルダウンロード処理
def downloadFile(url, download_path):
    request = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(request) as web_file, open(download_path, 'wb') as local_file:
        local_file.write(web_file.read())

#####################################################################################################
# メイン処理
#####################################################################################################

print("[INFO] プログラムを開始します。")

# コマンドライン引数を取得する
args = sys.argv
option = args[1]

# 引数チェックを行い、エラーならプログラムを終了する
if chkParam(option) == False:
    print("[ERROR] パラメータは「0」（販売）か「1」（購入）を選択してください。")
    sys.exit(1)

# 設定ファイルを読み込む
config = loadConfig()
download_base = config['download_base']
sleep_time_sec = config['sleep_time_sec']
roop_cnt = config['roop_cnt']

# ダウンロードファイルの格納先を作成する
download_path = createDownloadPath(option)

# 商品IDリストを読み込み
lists = readList()

try:
    # 読み込んだリスト1件毎に以下の処理を実行
    for index, item_list in enumerate(lists):
        print("[INFO] " + str(index + 1) + "件目のデータをダウンロードします。")
        # 商品写真1枚毎に以下の処理を実行
        for i in range(1, roop_cnt + 1):
            # ファイル名、URL、ダウンロード先を作成
            file_name = item_list + "_" + str(i) + suffix_jpg
            url = url_base + file_name
            download_target = download_path + "/" + file_name

            try:
                # 指定されたURLの商品写真をダウンロード先へ格納
                downloadFile(url, download_target)
                # サーバー負荷を軽減のため任意秒待機
                time.sleep(sleep_time_sec)
            except urllib.error.HTTPError as he:
                # ファイルが見つからない場合403エラーとなる為、次の処理を行う
                if he.code == 403:
                    print("[INFO] 作成完了。次のデータへ進みます。")
                    break
                else:
                    raise
    print("[INFO] プログラムを終了します。")
    sys.exit(0)
except urllib.error.HTTPError as he:
    print("[ERROR] HTTPError発生 内容：", hx)
    sys.exit(1)
except Exception as ex:
    print("[ERROR] Exception発生 内容：", ex)
    sys.exit(1)

