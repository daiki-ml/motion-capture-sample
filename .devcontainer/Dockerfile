FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /workspace

# システムパッケージの更新とOpenCVに必要な依存関係をインストール
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 非rootユーザーを作成（先に作成）
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Python依存関係をコピーしてインストール
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# MediaPipeのモデルを事前にダウンロード（root権限で実行）
RUN python -c "\
import mediapipe as mp; \
pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5); \
print('MediaPipe model downloaded successfully'); \
pose.close()" && \
    chmod -R 777 /usr/local/lib/python3.11/site-packages/mediapipe/modules

USER $USERNAME
