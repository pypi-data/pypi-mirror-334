import logging
from typing import List

import numpy as np
import torch
from omegaconf import DictConfig

from .common import Camera, Face, FacePartsName
from .head_pose_estimation import HeadPoseNormalizer, LandmarkEstimator
from .models import create_model
from .transforms import create_transform
from .utils import get_3d_face_model

logger = logging.getLogger(__name__)


class GazeEstimator:
    EYE_KEYS = [FacePartsName.REYE, FacePartsName.LEYE]

    def __init__(self, config: DictConfig):
        print("GazeEstimator 21")
        self._config = config
        print("GazeEstimator 23")
        self._face_model3d = get_3d_face_model(config)
        print("GazeEstimator 25")
        self.camera = Camera(config.gaze_estimator.camera_params)
        print("GazeEstimator 27")
        self._normalized_camera = Camera(
            config.gaze_estimator.normalized_camera_params)
        print("GazeEstimator 30")
        self._landmark_estimator = LandmarkEstimator(config)
        print("GazeEstimator 32")
        self._head_pose_normalizer = HeadPoseNormalizer(
            self.camera, self._normalized_camera,
            self._config.gaze_estimator.normalized_camera_distance)
        print("GazeEstimator 36")
        self._gaze_estimation_model = self._load_model()
        print("GazeEstimator 38")
        self._transform = create_transform(config)

    def _load_model(self) -> torch.nn.Module:
        print("_load_model 42")
        model = create_model(self._config)
        print("_load_model 44")
        checkpoint = torch.load(self._config.gaze_estimator.checkpoint,
                                map_location='cpu')
        print("_load_model 47")
        model.load_state_dict(checkpoint['model'])
        print("_load_model 49")
        model.to(torch.device(self._config.device))
        print("_load_model 51")
        model.eval()
        return model

    def detect_faces(self, image: np.ndarray) -> List[Face]:
        return self._landmark_estimator.detect_faces(image)

    def estimate_gaze(self, image: np.ndarray, face: Face) -> None:
        print("estimate_gaze before _face_model3d")
        self._face_model3d.estimate_head_pose(face, self.camera)
        self._face_model3d.compute_3d_pose(face)
        self._face_model3d.compute_face_eye_centers(face, self._config.mode)
        print("estimate_gaze after _face_model3d")

        if self._config.mode == 'MPIIGaze':
            for key in self.EYE_KEYS:
                eye = getattr(face, key.name.lower())
                self._head_pose_normalizer.normalize(image, eye)
            self._run_mpiigaze_model(face)
        elif self._config.mode == 'MPIIFaceGaze':
            self._head_pose_normalizer.normalize(image, face)
            self._run_mpiifacegaze_model(face)
        elif self._config.mode == 'ETH-XGaze':
            print("_config ETH-XGaze")
            self._head_pose_normalizer.normalize(image, face)
            print("_config ETH-XGaze normalize end")
            self._run_ethxgaze_model(face)
            print("_config ETH-XGaze _run_ethxgaze_model end")
            print("_config ETH-XGaze end")
        else:
            raise ValueError

    @torch.no_grad()
    def _run_mpiigaze_model(self, face: Face) -> None:
        images = []
        head_poses = []
        for key in self.EYE_KEYS:
            eye = getattr(face, key.name.lower())
            image = eye.normalized_image
            normalized_head_pose = eye.normalized_head_rot2d
            if key == FacePartsName.REYE:
                image = image[:, ::-1].copy()
                normalized_head_pose *= np.array([1, -1])
            image = self._transform(image)
            images.append(image)
            head_poses.append(normalized_head_pose)
        images = torch.stack(images)
        head_poses = np.array(head_poses).astype(np.float32)
        head_poses = torch.from_numpy(head_poses)

        device = torch.device(self._config.device)
        images = images.to(device)
        head_poses = head_poses.to(device)
        predictions = self._gaze_estimation_model(images, head_poses)
        predictions = predictions.cpu().numpy()

        for i, key in enumerate(self.EYE_KEYS):
            eye = getattr(face, key.name.lower())
            eye.normalized_gaze_angles = predictions[i]
            if key == FacePartsName.REYE:
                eye.normalized_gaze_angles *= np.array([1, -1])
            eye.angle_to_vector()
            eye.denormalize_gaze_vector()

    @torch.no_grad()
    def _run_mpiifacegaze_model(self, face: Face) -> None:
        image = self._transform(face.normalized_image).unsqueeze(0)

        device = torch.device(self._config.device)
        image = image.to(device)
        prediction = self._gaze_estimation_model(image)
        prediction = prediction.cpu().numpy()

        face.normalized_gaze_angles = prediction[0]
        face.angle_to_vector()
        face.denormalize_gaze_vector()

    @torch.no_grad()
    def _run_ethxgaze_model(self, face: Face) -> None:
        image = self._transform(face.normalized_image).unsqueeze(0)

        device = torch.device(self._config.device)
        image = image.to(device)
        prediction = self._gaze_estimation_model(image)
        prediction = prediction.cpu().numpy()

        face.normalized_gaze_angles = prediction[0]
        face.angle_to_vector()
        face.denormalize_gaze_vector()
