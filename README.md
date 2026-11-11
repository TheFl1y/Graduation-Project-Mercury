# Mercury：YOLOv5 物件偵測實驗

這是以 [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) 為基礎的畢業專題程式庫。現有程式包含單類別 `ball` 資料轉換與訓練設定、模型稀疏化／剪枝腳本，以及在偵測程式中加入的距離估算與資料庫查詢原型。**YOLOv5 的基礎架構和大部分通用程式來自上游專案**；本頁聚焦此儲存庫的修改與實驗。

## 專案流程

| 階段 | 對應檔案 | 目前內容 |
| --- | --- | --- |
| 資料準備 | `prepare_data.py`, `data/voc_ball.yaml` | 將 VOC XML 的 `ball` 標註轉為 YOLO 格式，隨機分為訓練與驗證集 |
| 訓練 | `train.py`, `models/yolov5s_ball.yaml` | 以一類物件的設定訓練 YOLOv5 |
| 模型精簡 | `train_sparsity.py`, `prune.py`, `finetune_pruned.py` | 稀疏化、通道剪枝與剪枝後微調的實驗腳本 |
| 偵測原型 | `detect.py`, `detect_pruned.py` | 輸出偵測框與信心分數；`detect.py` 對部分物件類別提供示範距離估算 |
| 資料庫原型 | `detect.py` | 可選擇連接 MySQL，讀取 `license` 表中狀態為「駕駛中」的資料 |

`ball` 訓練和人／車距離估算是兩組程式實驗；目前儲存庫沒有證據顯示兩者已整合為完整系統。

## 資料與重現狀態

- **未提供**原始訓練影像、VOC XML 標註、自訓模型權重、資料庫結構或可核對的專題評估結果。因此不能僅憑此 repo 重現原專題的訓練結果，也不在這裡宣稱準確率或速度提升。
- 原始儲存庫曾追蹤 `yolov5_train.txt`、`yolov5_val.txt`，內容是舊環境的 `D:` 磁碟路徑；整理版將它們視為可重新產生的檔案。使用自己的資料時請執行 `prepare_data.py`。
- `tutorial.ipynb` 與 `data/images/` 的範例圖片沿用 YOLOv5 教學內容，不是 Mercury 的專題評估。
- `data/voc_ball.yaml` 已保留本專題的一類資料設定；缺少資料時會直接提示，不會自動下載無關的 PASCAL VOC 全資料集。

## 使用自己的球體資料

1. 依下列結構放入同名圖片與 VOC XML 標註，XML 的物件類別需為 `ball`：

   ```text
   VOCdevkit/VOC2007/
   ├── Annotations/img00001.xml
   └── JPEGImages/img00001.jpg
   ```

2. 在相容的 Python／PyTorch 環境安裝 `requirements.txt`，從 repo 根目錄執行：

   ```bash
   pip install -r requirements.txt
   python prepare_data.py
   ```

   腳本會建立 `VOCdevkit/images/{train,val}`、`VOCdevkit/labels/{train,val}`，並重新產生訓練與驗證清單。它以隨機方式約 80/20 分割資料，未固定亂數種子。

3. 以自己的資料訓練，例如：

   ```bash
   python train.py --data data/voc_ball.yaml --cfg models/yolov5s_ball.yaml --weights '' --epochs 100 --imgsz 640
   ```

   稀疏化和剪枝腳本需要相容的已訓練權重及各自的參數設定；此 repo 沒有附完整實驗紀錄，因此它們應視為可供檢視的原型程式，而非已驗證的一鍵流程。

## 偵測與距離估算

提供自己的 YOLOv5 相容權重與影像後，可執行：

```bash
python detect.py --weights path/to/model.pt --source path/to/image.jpg --device cpu
```

程式會印出**實際偵測框座標**與信心分數。當模型類別名稱為 `person`、`car`、`motorcycle` 或 `bicycle` 時，還會依預設物體寬度及固定焦距參數計算距離。這些參數未經相機校正，**數值僅是示範估算，不能用於安全警示或真實距離判定**。單類別 `ball` 模型目前沒有對應的寬度參數，因此只輸出偵測結果。

資料庫查詢預設關閉，偵測本身不需要 MySQL。若要檢視舊版資料庫原型，需自行建立 `mercury.license` 表，安裝 `mysql-connector-python`，並設定 `MERCURY_DB_ENABLED=1`、`MERCURY_DB_HOST`、`MERCURY_DB_USER`、`MERCURY_DB_PASSWORD`、`MERCURY_DB_NAME`。此查詢只讀取資料；原 repo 沒有提供建表檔，請勿使用真實個資進行測試。語音函式若要啟用，另需 `gTTS` 與 `pygame`。

## 授權與來源

本儲存庫保留上游 YOLOv5 的 [GPL-3.0 授權](LICENSE)。通用模型、訓練與推論框架的來源請見 [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)；本 repo 的 `prepare_data.py`、球體設定、剪枝流程與 Mercury 偵測擴充應與上游程式碼區分閱讀。
