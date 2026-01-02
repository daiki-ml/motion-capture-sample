# モーションキャプチャデモシステム
スマホ1台で撮影した動画から、AIを使って3D座標を抽出し、ブラウザで3Dアニメーションとして可視化できます。

## 特徴

- **簡単セットアップ**: Docker環境で依存関係を自動解決
- **高精度**: GoogleのMediaPipeを使用した3D姿勢推定
- **オフライン動作**: インターネット接続不要（講演会場でも安心）
- **インタラクティブ可視化**: ブラウザで再生・回転・拡大が可能な3Dアニメーション

## 技術スタック

- **MediaPipe**: Google製の3D姿勢推定ライブラリ
- **OpenCV**: 動画処理
- **Plotly**: インタラクティブな3D可視化
- **Docker**: 開発環境の統一

## プロジェクト構成

```
kitasato/
├── .devcontainer/          # VSCode開発コンテナ設定
│   ├── Dockerfile
│   └── devcontainer.json
├── src/                    # Pythonソースコード
│   ├── motion_capture.py   # 動画から3D座標を抽出
│   ├── visualizer.py       # 3Dアニメーション生成
│   └── utils.py            # ユーティリティ関数
├── input/                  # 入力動画を配置
├── output/                 # 解析結果を出力
├── requirements.txt        # Python依存関係
├── docker-compose.yml      # Docker Compose設定
└── README.md              # このファイル
```

## セットアップ

### 方法1: VSCodeのdevcontainerを使用（推奨）

1. VSCodeをインストール
2. VSCode拡張機能「Dev Containers」をインストール
3. このプロジェクトをVSCodeで開く
4. コマンドパレット（Cmd+Shift+P / Ctrl+Shift+P）で「Dev Containers: Reopen in Container」を選択
5. コンテナが自動でビルドされ、開発環境が整います

### 方法2: Docker Composeを使用

```bash
# コンテナのビルドと起動
docker-compose up -d

# コンテナに入る
docker-compose exec motion-capture bash
```

## 使い方

### 1. 動画の準備

スマホで撮影した動画を `input/` フォルダに配置します。

**撮影のコツ:**
- 全身が映るように撮影
- カメラは固定
- 明るい場所で撮影
- 被写体とカメラの距離は2-5m程度
- 動画の長さは10-30秒（デモ用）

例:
```bash
# 動画を配置
cp ~/Videos/walking.mp4 input/
```

### 2. 3D座標の抽出

```bash
# 基本的な使い方
python src/motion_capture.py -i input/walking.mp4

# オプション指定
python src/motion_capture.py \
  -i input/walking.mp4 \
  -o output/my_result.json \
  --no-visualize  # 可視化動画を生成しない場合
```

**出力ファイル:**
- `output/walking_3d_coords.json`: 3D座標データ（JSON形式）
- `output/walking_visualized.mp4`: スケルトンを重ねた動画（--no-visualizeを指定しない場合）

### 3. 3Dアニメーションの生成

```bash
# 基本的な使い方
python src/visualizer.py -i output/walking_3d_coords.json

# オプション指定
python src/visualizer.py \
  -i output/walking_3d_coords.json \
  -o output/my_animation.html \
  --frame-skip 2  # フレームを間引く（軽量化）
```

**出力ファイル:**
- `output/walking_3d_animation.html`: ブラウザで開けるインタラクティブな3Dアニメーション

### 4. 結果の確認

生成されたHTMLファイルをブラウザで開きます:

```bash
# macOSの場合
open output/walking_3d_animation.html

# Linuxの場合
xdg-open output/walking_3d_animation.html
```

ブラウザ上で以下の操作が可能です:
- **再生/一時停止**: 画面下のボタン
- **シークバー**: 任意の時点に移動
- **視点回転**: マウスドラッグ
- **拡大縮小**: マウスホイール

## 検出される関節点

MediaPipeは33個の関節点を検出します:

- **顔**: 鼻、目、耳、口
- **上半身**: 肩、肘、手首、手指（親指、人差し指、小指）
- **下半身**: 腰、膝、足首、かかと、足指

## トラブルシューティング

### 動画が読み込めない

```bash
# サポートされている動画形式: mp4, avi, mov など
# 変換が必要な場合はffmpegを使用
ffmpeg -i input.mov -c:v libx264 output.mp4
```

### 関節が検出されない

- 全身が映っているか確認
- 明るさが十分か確認
- カメラとの距離を調整（2-5m推奨）
- 複雑な背景を避ける

### HTMLファイルが重い

`--frame-skip` オプションでフレームを間引く:

```bash
python src/visualizer.py -i output/data.json --frame-skip 3
```

## デモでの使い方（講演向け）

### 事前準備

1. 複数の動画を用意（歩行、スポーツ動作など）
2. 事前に解析を完了させておく
3. HTMLファイルをブラウザで開いておく

### 講演の流れ

1. **導入**: Sportipでの経験を紹介
2. **デモ1**: 事前に用意したHTMLで3Dアニメーションを再生
3. **説明**: スマホ1台での撮影 → AI解析 → 3D座標抽出の流れ
4. **応用**: 理学療法への活用可能性
   - 歩行分析
   - リハビリ動作の評価
   - 運動療法の効果測定

### Tips

- 動画は10-30秒程度の短いものを複数用意
- 異なる動作（歩行、ジャンプ、投球など）を見せる
- 3D可視化を回転させて立体的に見せる
- 処理済みの結果を用意しておき、時間短縮

## ライセンス

このプロジェクトは教育・デモ目的で作成されています。

使用しているライブラリのライセンス:
- MediaPipe: Apache License 2.0
- OpenCV: Apache License 2.0
- Plotly: MIT License

## 参考資料

- [MediaPipe公式ドキュメント](https://ai.google.dev/edge/mediapipe/solutions/guide)
- [MediaPipe Pythonサンプル](https://github.com/Kazuhito00/mediapipe-python-sample)


