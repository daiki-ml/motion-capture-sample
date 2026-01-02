"""
モーションキャプチャメインスクリプト

MediaPipeを使用して動画から3D姿勢推定を行い、
関節の3D座標を抽出してJSONファイルに保存します。
"""

import argparse
import cv2
import json
import mediapipe as mp
import numpy as np
from pathlib import Path
from tqdm import tqdm


class MotionCapture:
    """MediaPipeを使った3Dモーションキャプチャクラス"""

    def __init__(self):
        """初期化"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Poseモデルの設定
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,  # 0, 1, 2 (2が最も精度高い)
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_video(self, video_path: str, output_path: str = None,
                     visualize: bool = True) -> dict:
        """
        動画を処理して3D座標を抽出

        Args:
            video_path: 入力動画のパス
            output_path: 出力JSONファイルのパス（Noneの場合は自動生成）
            visualize: 可視化結果の動画を保存するか

        Returns:
            抽出した座標データを含む辞書
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

        # 出力パスの設定
        if output_path is None:
            output_path = Path("output") / f"{video_path.stem}_3d_coords.json"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 動画の読み込み
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"動画情報:")
        print(f"  - FPS: {fps}")
        print(f"  - フレーム数: {frame_count}")
        print(f"  - 解像度: {width}x{height}")

        # 可視化用の動画ライター
        video_writer = None
        if visualize:
            output_video_path = output_path.parent / f"{video_path.stem}_visualized.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                str(output_video_path), fourcc, fps, (width, height)
            )

        # 座標データを格納
        results_data = {
            "metadata": {
                "video_name": video_path.name,
                "fps": fps,
                "frame_count": frame_count,
                "resolution": {"width": width, "height": height}
            },
            "frames": []
        }

        # フレームごとに処理
        frame_idx = 0
        with tqdm(total=frame_count, desc="解析中") as pbar:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                # BGRからRGBに変換
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 姿勢推定
                results = self.pose.process(frame_rgb)

                frame_data = {
                    "frame_index": frame_idx,
                    "timestamp": frame_idx / fps,
                    "landmarks_2d": [],
                    "landmarks_3d": []
                }

                # ランドマークが検出された場合
                if results.pose_landmarks:
                    # 2D座標（画像上の座標）
                    for landmark in results.pose_landmarks.landmark:
                        frame_data["landmarks_2d"].append({
                            "x": landmark.x,
                            "y": landmark.y,
                            "z": landmark.z,  # 深度情報
                            "visibility": landmark.visibility
                        })

                    # 3D座標（ワールド座標系）
                    if results.pose_world_landmarks:
                        for landmark in results.pose_world_landmarks.landmark:
                            frame_data["landmarks_3d"].append({
                                "x": landmark.x,
                                "y": landmark.y,
                                "z": landmark.z,
                                "visibility": landmark.visibility
                            })

                    # 可視化
                    if visualize and video_writer:
                        # スケルトンを描画
                        self.mp_drawing.draw_landmarks(
                            frame,
                            results.pose_landmarks,
                            self.mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                        )
                        video_writer.write(frame)

                results_data["frames"].append(frame_data)
                frame_idx += 1
                pbar.update(1)

        # リソースの解放
        cap.release()
        if video_writer:
            video_writer.release()

        # JSONに保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        print(f"\n解析完了!")
        print(f"  - 座標データ: {output_path}")
        if visualize:
            print(f"  - 可視化動画: {output_video_path}")

        return results_data

    def __del__(self):
        """デストラクタ"""
        if hasattr(self, 'pose'):
            self.pose.close()


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='動画から3Dモーションキャプチャを実行'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='入力動画のパス'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='出力JSONファイルのパス（デフォルト: output/<動画名>_3d_coords.json）'
    )
    parser.add_argument(
        '--no-visualize',
        action='store_true',
        help='可視化動画を生成しない'
    )

    args = parser.parse_args()

    # モーションキャプチャ実行
    mc = MotionCapture()
    mc.process_video(
        video_path=args.input,
        output_path=args.output,
        visualize=not args.no_visualize
    )


if __name__ == "__main__":
    main()
