"""
3D可視化スクリプト

抽出した3D座標データから3Dアニメーションを生成します。
Plotlyを使用してインタラクティブなHTMLファイルを出力します。
"""

import argparse
import json
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Tuple


class Visualizer3D:
    """3D座標データの可視化クラス"""

    # MediaPipe Poseのランドマーク接続定義
    POSE_CONNECTIONS = [
        # 胴体
        (11, 12),  # 左肩 - 右肩
        (11, 23),  # 左肩 - 左腰
        (12, 24),  # 右肩 - 右腰
        (23, 24),  # 左腰 - 右腰
        # 左腕
        (11, 13),  # 左肩 - 左肘
        (13, 15),  # 左肘 - 左手首
        # 右腕
        (12, 14),  # 右肩 - 右肘
        (14, 16),  # 右肘 - 右手首
        # 左脚
        (23, 25),  # 左腰 - 左膝
        (25, 27),  # 左膝 - 左足首
        (27, 29),  # 左足首 - 左足先
        (27, 31),  # 左足首 - 左かかと
        # 右脚
        (24, 26),  # 右腰 - 右膝
        (26, 28),  # 右膝 - 右足首
        (28, 30),  # 右足首 - 右足先
        (28, 32),  # 右足首 - 右かかと
        # 頭部
        (0, 1),  # 鼻 - 左目内側
        (0, 4),  # 鼻 - 右目内側
        (1, 2),  # 左目内側 - 左目
        (2, 3),  # 左目 - 左目外側
        (4, 5),  # 右目内側 - 右目
        (5, 6),  # 右目 - 右目外側
        (9, 10),  # 口左 - 口右
    ]

    def __init__(self):
        """初期化"""
        pass

    def load_data(self, json_path: str) -> dict:
        """
        JSONファイルから座標データを読み込み

        Args:
            json_path: JSONファイルのパス

        Returns:
            座標データを含む辞書
        """
        json_path = Path(json_path)
        if not json_path.exists():
            raise FileNotFoundError(f"JSONファイルが見つかりません: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"データ読み込み完了:")
        print(f"  - 動画名: {data['metadata']['video_name']}")
        print(f"  - フレーム数: {len(data['frames'])}")

        return data

    def create_3d_animation(
        self,
        data: dict,
        output_path: str = None,
        show_connections: bool = True,
        frame_skip: int = 1,
    ) -> str:
        """
        3Dアニメーションを生成

        Args:
            data: 座標データを含む辞書
            output_path: 出力HTMLファイルのパス
            show_connections: 骨格の接続線を表示するか
            frame_skip: フレームをスキップする数（1=全フレーム、2=1フレームおき）

        Returns:
            出力ファイルのパス
        """
        if output_path is None:
            output_path = (
                Path("output")
                / f"{Path(data['metadata']['video_name']).stem}_3d_animation.html"
            )
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        frames = data["frames"][::frame_skip]
        fps = data["metadata"]["fps"] / frame_skip

        # アニメーションフレームを作成
        plotly_frames = []
        slider_steps = []

        for frame_idx, frame in enumerate(frames):
            if not frame["landmarks_3d"]:
                continue

            # 3D座標を抽出
            landmarks = np.array(
                [[lm["x"], lm["y"], lm["z"]] for lm in frame["landmarks_3d"]]
            )

            # 関節点のプロット
            scatter_data = go.Scatter3d(
                x=landmarks[:, 0],
                y=landmarks[:, 1],
                z=landmarks[:, 2],
                mode="markers",
                marker=dict(size=10, color="red", opacity=0.8),
                name="関節点",
            )

            frame_data = [scatter_data]

            # 骨格の接続線を追加
            if show_connections:
                for connection in self.POSE_CONNECTIONS:
                    start_idx, end_idx = connection
                    if start_idx < len(landmarks) and end_idx < len(landmarks):
                        line_data = go.Scatter3d(
                            x=[landmarks[start_idx, 0], landmarks[end_idx, 0]],
                            y=[landmarks[start_idx, 1], landmarks[end_idx, 1]],
                            z=[landmarks[start_idx, 2], landmarks[end_idx, 2]],
                            mode="lines",
                            line=dict(color="blue", width=10),
                            showlegend=False,
                        )
                        frame_data.append(line_data)

            plotly_frames.append(go.Frame(data=frame_data, name=str(frame_idx)))

            slider_steps.append(
                {
                    "args": [
                        [str(frame_idx)],
                        {
                            "frame": {"duration": 1000 / fps, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    "label": f"{frame['timestamp']:.2f}s",
                    "method": "animate",
                }
            )

        # 初期フレームのデータ
        if frames and frames[0]["landmarks_3d"]:
            initial_landmarks = np.array(
                [[lm["x"], lm["y"], lm["z"]] for lm in frames[0]["landmarks_3d"]]
            )

            initial_scatter = go.Scatter3d(
                x=initial_landmarks[:, 0],
                y=initial_landmarks[:, 1],
                z=initial_landmarks[:, 2],
                mode="markers",
                marker=dict(size=10, color="red", opacity=0.8),
                name="関節点",
            )

            initial_data = [initial_scatter]

            if show_connections:
                for connection in self.POSE_CONNECTIONS:
                    start_idx, end_idx = connection
                    if start_idx < len(initial_landmarks) and end_idx < len(
                        initial_landmarks
                    ):
                        line_data = go.Scatter3d(
                            x=[
                                initial_landmarks[start_idx, 0],
                                initial_landmarks[end_idx, 0],
                            ],
                            y=[
                                initial_landmarks[start_idx, 1],
                                initial_landmarks[end_idx, 1],
                            ],
                            z=[
                                initial_landmarks[start_idx, 2],
                                initial_landmarks[end_idx, 2],
                            ],
                            mode="lines",
                            line=dict(color="blue", width=10),
                            showlegend=False,
                        )
                        initial_data.append(line_data)
        else:
            initial_data = []

        # レイアウト設定
        layout = go.Layout(
            title=f"3Dモーションキャプチャ - {data['metadata']['video_name']}",
            scene=dict(
                xaxis=dict(title="X", range=[-1, 1]),
                yaxis=dict(title="Y", range=[-1, 1]),
                zaxis=dict(title="Z", range=[-1, 1]),
                aspectmode="cube",
            ),
            updatemenus=[
                {
                    "type": "buttons",
                    "showactive": False,
                    "buttons": [
                        {
                            "label": "再生",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 1000 / fps, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                        {
                            "label": "一時停止",
                            "method": "animate",
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                    ],
                    "x": 0.1,
                    "y": 0,
                    "xanchor": "left",
                    "yanchor": "bottom",
                }
            ],
            sliders=[
                {
                    "active": 0,
                    "steps": slider_steps,
                    "x": 0.1,
                    "len": 0.9,
                    "xanchor": "left",
                    "y": 0,
                    "yanchor": "top",
                    "pad": {"b": 10, "t": 50},
                }
            ],
        )

        # Figureを作成
        fig = go.Figure(data=initial_data, layout=layout, frames=plotly_frames)

        # HTMLファイルに保存
        fig.write_html(str(output_path))

        print(f"\n3Dアニメーション生成完了!")
        print(f"  - 出力ファイル: {output_path}")
        print(f"  - ブラウザで開いて確認してください")

        return str(output_path)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="3D座標データから3Dアニメーションを生成"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="入力JSONファイルのパス（motion_capture.pyの出力）",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="出力HTMLファイルのパス（デフォルト: output/<動画名>_3d_animation.html）",
    )
    parser.add_argument(
        "--no-connections", action="store_true", help="骨格の接続線を表示しない"
    )
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=1,
        help="フレームスキップ数（大きいほど軽量、デフォルト: 1）",
    )

    args = parser.parse_args()

    # 可視化実行
    visualizer = Visualizer3D()
    data = visualizer.load_data(args.input)
    visualizer.create_3d_animation(
        data=data,
        output_path=args.output,
        show_connections=not args.no_connections,
        frame_skip=args.frame_skip,
    )


if __name__ == "__main__":
    main()
