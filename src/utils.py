"""
ユーティリティ関数

データ処理や共通機能を提供します。
"""

import numpy as np
from typing import List, Dict, Tuple
from scipy import interpolate
from scipy.ndimage import gaussian_filter1d


def smooth_landmarks(landmarks_sequence: np.ndarray, sigma: float = 2.0) -> np.ndarray:
    """
    ランドマーク座標系列をスムージング

    Args:
        landmarks_sequence: (frames, landmarks, 3) の形状の配列
        sigma: ガウシアンフィルタのシグマ値

    Returns:
        スムージングされた座標配列
    """
    smoothed = np.copy(landmarks_sequence)

    for landmark_idx in range(landmarks_sequence.shape[1]):
        for coord_idx in range(3):  # x, y, z
            smoothed[:, landmark_idx, coord_idx] = gaussian_filter1d(
                landmarks_sequence[:, landmark_idx, coord_idx],
                sigma=sigma
            )

    return smoothed


def interpolate_missing_frames(landmarks_sequence: np.ndarray,
                               valid_frames: List[int]) -> np.ndarray:
    """
    欠損フレームを線形補間

    Args:
        landmarks_sequence: (frames, landmarks, 3) の形状の配列
        valid_frames: 有効なフレームのインデックスリスト

    Returns:
        補間された座標配列
    """
    if len(valid_frames) < 2:
        return landmarks_sequence

    interpolated = np.copy(landmarks_sequence)
    total_frames = landmarks_sequence.shape[0]
    num_landmarks = landmarks_sequence.shape[1]

    for landmark_idx in range(num_landmarks):
        for coord_idx in range(3):  # x, y, z
            # 有効なフレームの値を取得
            valid_values = landmarks_sequence[valid_frames, landmark_idx, coord_idx]

            # 補間関数を作成
            f = interpolate.interp1d(
                valid_frames,
                valid_values,
                kind='linear',
                fill_value='extrapolate'
            )

            # 全フレームに対して補間
            all_frames = np.arange(total_frames)
            interpolated[:, landmark_idx, coord_idx] = f(all_frames)

    return interpolated


def normalize_coordinates(landmarks: np.ndarray,
                         center: bool = True,
                         scale: bool = True) -> Tuple[np.ndarray, Dict]:
    """
    座標を正規化

    Args:
        landmarks: (landmarks, 3) の形状の配列
        center: 重心を原点に移動するか
        scale: スケールを正規化するか

    Returns:
        正規化された座標と正規化パラメータ
    """
    normalized = np.copy(landmarks)
    params = {}

    if center:
        # 重心を計算
        centroid = np.mean(landmarks, axis=0)
        normalized -= centroid
        params['centroid'] = centroid

    if scale:
        # スケールを計算（原点からの最大距離）
        max_distance = np.max(np.linalg.norm(normalized, axis=1))
        if max_distance > 0:
            normalized /= max_distance
            params['scale'] = max_distance
        else:
            params['scale'] = 1.0

    return normalized, params


def calculate_joint_angles(landmarks: np.ndarray,
                          joint_triplets: List[Tuple[int, int, int]]) -> List[float]:
    """
    関節角度を計算

    Args:
        landmarks: (landmarks, 3) の形状の配列
        joint_triplets: 関節を定義する3点のインデックスのリスト
                       [(point1, joint, point2), ...]

    Returns:
        各関節の角度（度数法）のリスト
    """
    angles = []

    for p1_idx, joint_idx, p2_idx in joint_triplets:
        # ベクトルを計算
        v1 = landmarks[p1_idx] - landmarks[joint_idx]
        v2 = landmarks[p2_idx] - landmarks[joint_idx]

        # 内積を使って角度を計算
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        # 数値誤差対策
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)

        angles.append(angle_deg)

    return angles


def calculate_velocity(landmarks_sequence: np.ndarray, fps: float) -> np.ndarray:
    """
    各ランドマークの速度を計算

    Args:
        landmarks_sequence: (frames, landmarks, 3) の形状の配列
        fps: フレームレート

    Returns:
        速度配列 (frames-1, landmarks, 3)
    """
    # フレーム間の差分を計算
    diff = np.diff(landmarks_sequence, axis=0)

    # 時間で割って速度に変換
    dt = 1.0 / fps
    velocity = diff / dt

    return velocity


def filter_low_confidence_landmarks(landmarks: List[Dict],
                                   confidence_threshold: float = 0.5) -> List[Dict]:
    """
    信頼度の低いランドマークをフィルタリング

    Args:
        landmarks: ランドマークのリスト（各要素はx, y, z, visibilityを含む辞書）
        confidence_threshold: 信頼度の閾値

    Returns:
        フィルタリングされたランドマークのリスト
    """
    filtered = []

    for landmark in landmarks:
        if landmark.get('visibility', 0) >= confidence_threshold:
            filtered.append(landmark)
        else:
            # 信頼度が低い場合はNoneまたはゼロ値を設定
            filtered.append({
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'visibility': 0.0
            })

    return filtered


def get_landmark_names() -> List[str]:
    """
    MediaPipe Poseのランドマーク名リストを取得

    Returns:
        ランドマーク名のリスト（33個）
    """
    return [
        "nose",                    # 0
        "left_eye_inner",          # 1
        "left_eye",                # 2
        "left_eye_outer",          # 3
        "right_eye_inner",         # 4
        "right_eye",               # 5
        "right_eye_outer",         # 6
        "left_ear",                # 7
        "right_ear",               # 8
        "mouth_left",              # 9
        "mouth_right",             # 10
        "left_shoulder",           # 11
        "right_shoulder",          # 12
        "left_elbow",              # 13
        "right_elbow",             # 14
        "left_wrist",              # 15
        "right_wrist",             # 16
        "left_pinky",              # 17
        "right_pinky",             # 18
        "left_index",              # 19
        "right_index",             # 20
        "left_thumb",              # 21
        "right_thumb",             # 22
        "left_hip",                # 23
        "right_hip",               # 24
        "left_knee",               # 25
        "right_knee",              # 26
        "left_ankle",              # 27
        "right_ankle",             # 28
        "left_heel",               # 29
        "right_heel",              # 30
        "left_foot_index",         # 31
        "right_foot_index",        # 32
    ]


def get_major_joint_angles() -> List[Tuple[int, int, int, str]]:
    """
    主要な関節角度の定義を取得

    Returns:
        (point1_idx, joint_idx, point2_idx, joint_name) のリスト
    """
    return [
        # 左腕
        (11, 13, 15, "left_elbow"),      # 左肩-左肘-左手首
        # 右腕
        (12, 14, 16, "right_elbow"),     # 右肩-右肘-右手首
        # 左脚
        (23, 25, 27, "left_knee"),       # 左腰-左膝-左足首
        # 右脚
        (24, 26, 28, "right_knee"),      # 右腰-右膝-右足首
        # 体幹
        (11, 23, 25, "left_hip"),        # 左肩-左腰-左膝
        (12, 24, 26, "right_hip"),       # 右肩-右腰-右膝
    ]
