# 3Dモーションキャプチャ - 初心者向けガイド

## これは何？

スマホで撮影した動画から、**人の動きを3Dで見られるアニメーション**を作るツールです。

- プログラミングの知識は不要です
- スマホ1台で撮影した動画があればOK
- 結果はブラウザで見られます（回転・拡大が自由にできます）

**例：** 歩いている動画 → AIが自動で骨格を検出 → 3Dアニメーションに変換

---

## 必要なもの

### 1. パソコン
- Windows、Mac、Linuxどれでも可
- メモリ: 8GB以上推奨

### 2. ソフトウェア（全て無料）
以下を順番にインストールしてください：

#### ① Visual Studio Code（VSCode）
- コードを実行するためのエディタです
- ダウンロード: https://code.visualstudio.com/
- 青い「Download」ボタンをクリック
- ダウンロードしたファイルを開いてインストール
- インストール後、VSCodeを起動して確認してください

#### ② Docker Desktop
- プログラムを動かすための環境を自動で作ってくれるツールです
- ダウンロード: https://www.docker.com/products/docker-desktop
- 「Download for Mac」または「Download for Windows」をクリック
- ダウンロードしたファイルを開いてインストール
- **重要**: インストール後、Docker Desktopを起動してください
  - 起動していないとエラーになります
  - タスクバー（Windows）またはメニューバー（Mac）にDockerのアイコンが表示されればOK

### 3. 動画
- スマホで撮影した動画（mp4形式推奨）
- 撮影のコツは後述

---

## インストール手順

### ステップ1: プロジェクトをダウンロード

1. **GitHubからZIPファイルをダウンロード**
   - ブラウザでこのページを開く: https://github.com/daiki-ml/motion-capture-sample
   - 緑色の「Code」ボタンをクリック
   - 「Download ZIP」をクリック
   - ZIPファイルがダウンロードされます

2. **ZIPファイルを解凍**
   - ダウンロードしたZIPファイル（`motion-capture-sample-main.zip`）をダブルクリック
   - または右クリック → 「すべて展開」（Windows）/ 「開く」（Mac）
   - 解凍されたフォルダ（`motion-capture-sample-main`）が作成されます

3. **分かりやすい場所に移動**（任意）
   - デスクトップや書類フォルダなど、見つけやすい場所に移動してください

### ステップ2: VSCodeで開く

1. **VSCodeを起動**

2. **「フォルダーを開く」をクリック**
   - メニューバー: ファイル → フォルダーを開く（Open Folder）
   - 先ほど解凍した `motion-capture-sample-main` フォルダを選択
   - 「選択」または「開く」をクリック

3. **Dev Containers拡張機能をインストール**
   - 左側のアイコンから「拡張機能」（四角が4つ重なったアイコン）をクリック
   - 検索バーに「Dev Containers」と入力
   - 「Dev Containers」（Microsoft製）を見つけて「インストール」をクリック
   - インストール完了を待つ

### ステップ3: コンテナで開く

1. **VSCodeの左下の緑色のアイコンをクリック**
   - 画面左下に「><」のようなアイコンがあります
   - クリックするとメニューが表示されます

2. **「コンテナーで再度開く」を選択**
   - メニューから「Reopen in Container」（コンテナーで再度開く）を選択
   - **初回は5-10分かかります**（自動で環境を構築しています）
   - 右下に進捗バーが表示されます
   - 「Starting Dev Container...」と表示されます

3. **完了を待つ**
   - 完了すると、左下に「Dev Container: モーションキャプチャデモ環境」と表示されます
   - これで準備完了です！

**トラブルシューティング:**
- 「Docker is not running」と表示される場合
  → Docker Desktopを起動してください
- 時間がかかりすぎる場合
  → インターネット接続を確認してください

---

## 使い方

### ステップ1: 動画を準備する

1. **スマホで動画を撮影**（または既存の動画を用意）

   **撮影のコツ:**
   - 全身が映るように撮影（頭から足先まで）
   - カメラは固定（手持ちでもOKですが、なるべく動かさない）
   - 明るい場所で撮影
   - 被写体とカメラの距離は2-5m程度
   - 動画の長さは10-30秒がおすすめ（長いと処理に時間がかかります）
   - 背景はシンプルな方が良い
   - 横向き撮影推奨

2. **動画をパソコンに転送**
   - AirDrop（Mac+iPhone）
   - USBケーブル
   - Googleドライブ・iCloudなど
   - お好きな方法で転送してください

3. **動画ファイル名を英語にする**
   - ファイル名を英数字のみにしてください
   - 例: `歩行.mp4` → `walking.mp4`
   - 日本語や特殊文字があるとエラーになることがあります

4. **動画を `input` フォルダに入れる**
   - VSCodeの左側のファイルツリーから `input` フォルダを開く
   - 動画ファイルをドラッグ&ドロップ
   - または、右クリック → 「Reveal in Finder/File Explorer」で開いて、直接ファイルをコピー

### ステップ2: ターミナルを開く

VSCode上部のメニューから:
- **ターミナル → 新しいターミナル** をクリック
- 画面下部にターミナル（黒い画面）が表示されます

### ステップ3: 3D座標を抽出する

ターミナルに以下のコマンドを**コピー&ペースト**して、Enterキーを押します:

```bash
python src/motion_capture.py -i input/walking.mp4
```

**ファイル名の変更:**
- `walking.mp4` の部分を、自分の動画ファイル名に変更してください
- 例: 自分の動画が `running.mp4` なら
  ```bash
  python src/motion_capture.py -i input/running.mp4
  ```

**処理中の表示:**
- 「Processing frame XX/YY...」と表示されます
- 動画の長さによって数分かかることがあります
- **完了するまで待ってください**

**処理完了:**
- 「3D座標の抽出が完了しました」と表示されます
- `output` フォルダに以下のファイルが作成されます:
  - `walking_3d_coords.json`: 3D座標データ
  - `walking_visualized.mp4`: 骨格を重ねた動画

### ステップ4: 3Dアニメーションを生成する

ターミナルに以下のコマンドを**コピー&ペースト**:

```bash
python src/visualizer.py -i output/walking_3d_coords.json
```

**ファイル名の変更:**
- `walking` の部分を、自分の動画ファイル名に変更してください
- 例: `running.mp4` を使った場合
  ```bash
  python src/visualizer.py -i output/running_3d_coords.json
  ```

**処理中:**
- 数秒〜1分程度で完了します

**処理完了:**
- 「3Dアニメーション生成完了!」と表示されます
- `output/walking_3d_animation.html` が作成されます

### ステップ5: 結果を見る

1. **VSCodeの左側のファイルツリーから `output` フォルダを開く**

2. **`walking_3d_animation.html` を右クリック**

3. **「Reveal in Finder」（Mac）または「Reveal in File Explorer」（Windows）を選択**
   - ファイルの場所が開きます

4. **HTMLファイルをダブルクリック**
   - ブラウザが開いて3Dアニメーションが表示されます

5. **操作方法:**
   - **再生/一時停止**: 画面下の「再生」ボタン
   - **シークバー**: 下のバーをドラッグして好きな時点に移動
   - **視点回転**: マウスでドラッグ（左ボタン）
   - **拡大縮小**: マウスホイールでスクロール
   - **視点移動**: 右ボタンでドラッグ

**別の動画を試す場合:**
- ステップ1から繰り返してください
- `input` フォルダに新しい動画を入れて、同じコマンドを実行

---

## よくある質問

### Q1: 「Docker is not running」と表示される

**A:** Docker Desktopを起動してください。

**手順:**
1. Windowsの場合: スタートメニューから「Docker Desktop」を検索して起動
2. Macの場合: Launchpadから「Docker」を起動
3. 起動が完了するまで待つ（初回は数分かかることがあります）
4. タスクバー（Windows）またはメニューバー（Mac）にDockerのアイコンが表示されればOK
5. VSCodeに戻って、もう一度コマンドを実行

### Q2: 「No such file or directory」と表示される

**A:** ファイル名が間違っている可能性があります。

**確認方法:**
1. VSCodeの左側で `input` フォルダを開く
2. 動画ファイルの名前を確認
3. コマンドのファイル名部分を、正確に入力

**よくある間違い:**
- 大文字・小文字が違う（`Walking.mp4` と `walking.mp4` は別物）
- 拡張子が違う（`.mp4` と `.MP4` など）
- スペースが入っている（`my video.mp4` → `my_video.mp4` に変更してください）

### Q3: 動画が読み込めない

**A:** 以下を確認してください:

1. **ファイル名に日本語や特殊文字が含まれていませんか？**
   - 英数字のファイル名にリネームしてください
   - 例: `歩行テスト.mp4` → `walking_test.mp4`

2. **動画形式は対応していますか？**
   - 対応形式: mp4, avi, mov
   - iPhoneの.MOV形式もOKです
   - 他の形式の場合、オンラインコンバーターでmp4に変換してください

3. **ファイルサイズが大きすぎませんか？**
   - 100MB以下を推奨
   - 大きい場合は、動画編集ソフトで圧縮してください

### Q4: 関節が検出されない・おかしい

**A:** 以下を試してください:

**撮影に問題がある場合:**
- ✅ 全身が映っているか確認（特に足先と頭）
- ✅ 明るさが十分か確認（逆光は避ける）
- ✅ カメラとの距離を調整（2-5m推奨）
- ✅ 複雑な背景を避ける（壁の前など）
- ✅ 複数人が映っている場合、1人だけにする
- ✅ 服装は体のラインが分かりやすいもの

**それでも解決しない場合:**
- 別の動画で試してみてください
- サンプル動画で動作確認してください

### Q5: HTMLファイルが重くて動かない

**A:** フレームを間引いて軽量化できます:

```bash
python src/visualizer.py -i output/walking_3d_coords.json --frame-skip 2
```

**オプションの説明:**
- `--frame-skip 2`: 1フレームおきに処理（半分のサイズ）
- `--frame-skip 3`: 2フレームおきに処理（1/3のサイズ）
- 数字を大きくするほど軽くなりますが、滑らかさは落ちます

### Q6: コマンドをコピペしたらエラーになる

**A:** 以下を確認してください:

1. **ターミナルがVSCode内のものか確認**
   - VSCode内のターミナル（下部の黒い画面）を使ってください
   - パソコンのターミナルアプリでは動きません

2. **コンテナ内で実行しているか確認**
   - 左下に「Dev Container: モーションキャプチャデモ環境」と表示されているか確認
   - 表示されていない場合、ステップ3をやり直してください

3. **コマンドが正しくコピーできているか確認**
   - スペースや改行が余分に入っていないか確認
   - 全角文字が混ざっていないか確認

### Q7: 「Permission denied」と表示される

**A:** Dockerにファイルへのアクセス権限を与える必要があります。

**Mac/Windowsの場合:**
1. Docker Desktopを開く
2. Settings（設定）→ Resources → File Sharing
3. プロジェクトフォルダがあるディレクトリを追加
4. 「Apply & Restart」をクリック

### Q8: もっと詳しく知りたい・カスタマイズしたい

**A:** 以下のドキュメントを参照してください:

**コマンドオプション:**
```bash
# ヘルプを表示
python src/motion_capture.py --help
python src/visualizer.py --help
```

**コードを見る:**
- `src/motion_capture.py`: モーションキャプチャの処理
- `src/visualizer.py`: 3D可視化の処理
- コメントで説明を書いています

---

## コマンド一覧

### 基本コマンド

```bash
# 1. 3D座標を抽出
python src/motion_capture.py -i input/動画ファイル名.mp4

# 2. 3Dアニメーションを生成
python src/visualizer.py -i output/動画ファイル名_3d_coords.json
```

### よく使うオプション

#### 軽量化（ファイルサイズを小さくする）
```bash
python src/visualizer.py -i output/walking_3d_coords.json --frame-skip 2
```

#### 可視化動画を作らない（処理を速くする）
```bash
python src/motion_capture.py -i input/walking.mp4 --no-visualize
```

#### 出力先を変更
```bash
python src/motion_capture.py -i input/walking.mp4 -o output/my_result.json
python src/visualizer.py -i output/walking_3d_coords.json -o output/my_animation.html
```

#### 骨格の線を表示しない（点だけ）
```bash
python src/visualizer.py -i output/walking_3d_coords.json --no-connections
```

---

## 検出される関節点

MediaPipeは33個の関節点を検出します:

| 部位 | 関節点 |
|------|--------|
| **顔** | 鼻、左目（内側・中心・外側）、右目（内側・中心・外側）、口（左・右） |
| **上半身** | 左肩、右肩、左肘、右肘、左手首、右手首 |
| **手** | 左手（親指・人差し指・小指）、右手（親指・人差し指・小指） |
| **下半身** | 左腰、右腰、左膝、右膝、左足首、右足首 |
| **足** | 左足（かかと・つま先）、右足（かかと・つま先） |

これらの関節点の3D座標（X, Y, Z）を抽出して、3Dアニメーションを作成します。

---

## プロジェクトの仕組み

### フォルダ構成

```
motion-capture-sample-main/
├── input/              # ここに動画を入れる
│   └── .gitkeep
├── output/             # 処理結果が保存される
│   ├── XXX_3d_coords.json          # 3D座標データ
│   ├── XXX_visualized.mp4          # 骨格を重ねた動画
│   └── XXX_3d_animation.html       # 3Dアニメーション
├── src/                # プログラム本体
│   ├── motion_capture.py           # 座標抽出プログラム
│   ├── visualizer.py               # 可視化プログラム
│   └── utils.py                    # 補助機能
├── .devcontainer/      # Docker設定
├── requirements.txt    # 必要なライブラリ一覧
└── README.md          # このファイル
```

### 処理の流れ

1. **動画読み込み** → OpenCVで動画を1フレームずつ読み込む
2. **姿勢推定** → MediaPipeで各フレームから33個の関節点を検出
3. **3D座標抽出** → 検出した関節点の3D座標を保存
4. **可視化** → Plotlyで3Dアニメーションを生成
5. **結果出力** → HTMLファイルとして保存

### 使用技術

- **Python**: プログラミング言語
- **MediaPipe**: Google製のAI姿勢推定ライブラリ
- **OpenCV**: 動画処理ライブラリ
- **Plotly**: インタラクティブな3D可視化ライブラリ
- **Docker**: 環境構築の自動化
- **VSCode Dev Containers**: 開発環境の統一

---

## サンプル動画

練習用のサンプル動画は以下から入手できます:

1. **Pexels（無料動画素材サイト）**
   - https://www.pexels.com/search/videos/walking/
   - 「walking」「running」「exercise」などで検索
   - ダウンロードして `input` フォルダに入れてください

---

## 参考資料

### 公式ドキュメント
- [MediaPipe公式](https://ai.google.dev/edge/mediapipe/solutions/guide)
- [Plotly公式](https://plotly.com/python/)
- [VSCode公式](https://code.visualstudio.com/docs)
- [Docker公式](https://docs.docker.com/)

### チュートリアル
- [MediaPipe Pythonサンプル](https://github.com/Kazuhito00/mediapipe-python-sample)
- [Plotly入門](https://plotly.com/python/getting-started/)

---

**最終更新: 2026年1月**
