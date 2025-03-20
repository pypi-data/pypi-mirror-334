import argparse
import logging
import pathlib
import warnings
import time

import torch
from omegaconf import DictConfig, OmegaConf
import importlib.metadata
from importlib.resources import files

from .demo import Demo
from .utils import (check_path_all, download_dlib_pretrained_model,
                    download_ethxgaze_model,
                    download_mpiigaze_model, expanduser_all,
                    generate_dummy_camera_params)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(prog='ehdg_gaze',
                                     description='Eye Health Diagnostic Group Gaze Detector.')
    ehdg_gaze_version = importlib.metadata.version('ehdg_gaze')
    parser.add_argument('--version', action='version', version=ehdg_gaze_version),
    parser.add_argument(
        '--config',
        type=str,
        help='Config file. When using a config file, all the other '
             'commandline arguments are ignored. '
             'See https://github.com/hysts/pytorch_mpiigaze_demo/ptgaze/data/configs/eth-xgaze.yaml'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['mpiigaze', 'mpiifacegaze', 'eth-xgaze'],
        help='With \'mpiigaze\', MPIIGaze model will be used. '
             'With \'mpiifacegaze\', MPIIFaceGaze model will be used. '
             'With \'eth-xgaze\', ETH-XGaze model will be used.')
    parser.add_argument(
        '--face-detector',
        type=str,
        default='mediapipe',
        choices=[
            'dlib', 'face_alignment_dlib', 'face_alignment_sfd', 'mediapipe'
        ],
        help='The method used to detect faces and find face landmarks '
             '(default: \'mediapipe\')')
    parser.add_argument('--device',
                        type=str,
                        choices=['cpu', 'cuda'],
                        help='Device used for model inference.')
    parser.add_argument('--image',
                        type=str,
                        help='Path to an input image file.')
    parser.add_argument('--video',
                        type=str,
                        help='Path to an input video file.')
    parser.add_argument(
        '--camera',
        type=str,
        help='Camera calibration file. '
             'See https://github.com/hysts/pytorch_mpiigaze_demo/ptgaze/data/calib/sample_params.yaml'
    )
    parser.add_argument(
        '--output-dir',
        '-o',
        type=str,
        help='If specified, the overlaid video will be saved to this directory.'
    )
    parser.add_argument('--ext',
                        '-e',
                        type=str,
                        choices=['avi', 'mp4'],
                        help='Output video file extension.')
    parser.add_argument(
        '--no-screen',
        action='store_true',
        help='If specified, the video is not displayed on screen, and saved '
             'to the output directory.')
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


def load_mode_config(args: argparse.Namespace, pkg_dir_in) -> DictConfig:
    package_root = pathlib.Path(__file__).parent.resolve()
    if args.mode == 'mpiigaze':
        path = package_root / 'data/configs/mpiigaze.yaml'
    elif args.mode == 'mpiifacegaze':
        path = package_root / 'data/configs/mpiifacegaze.yaml'
    elif args.mode == 'eth-xgaze':
        path = package_root / 'data/configs/eth-xgaze.yaml'
    else:
        raise ValueError
    config = OmegaConf.load(path)
    config.PACKAGE_ROOT = pkg_dir_in

    if args.face_detector:
        config.face_detector.mode = args.face_detector
    if args.device:
        config.device = args.device
    if config.device == 'cuda' and not torch.cuda.is_available():
        config.device = 'cpu'
        warnings.warn('Run on CPU because CUDA is not available.')
    if args.image and args.video:
        raise ValueError('Only one of --image or --video can be specified.')
    if args.image:
        config.demo.image_path = args.image
        config.demo.use_camera = False
    if args.video:
        config.demo.video_path = args.video
        config.demo.use_camera = False
    if args.camera:
        config.gaze_estimator.camera_params = args.camera
    elif args.image or args.video:
        config.gaze_estimator.use_dummy_camera_params = True
    if args.output_dir:
        config.demo.output_dir = args.output_dir
    if args.ext:
        config.demo.output_file_extension = args.ext
    if args.no_screen:
        config.demo.display_on_screen = False
        if not config.demo.output_dir:
            config.demo.output_dir = 'outputs'

    return config


def get_package_dir(module_name):
    config_dir = files(module_name)
    return str(config_dir)


def main(in_v, out_d):
    # parser = argparse.ArgumentParser(prog='ehdg_gaze',
    #                                  description='Eye Health Diagnostic Group Gaze Detector.')
    # ehdg_gaze_version = importlib.metadata.version('ehdg_gaze')
    # parser.add_argument('--version', action='version', version=ehdg_gaze_version),
    # parser.add_argument("-i", dest="input_video", required=True, type=str, help="input video.")
    # parser.add_argument("-o", dest="output_video", required=False, default=None, type=str, help="output video.")
    # parser.add_argument("-t", dest="model_type", required=False, default="eth-xgaze",
    #                     type=str, choices=['mpiigaze', 'eth-xgaze'],
    #                     help="model type (eth-xgaze or mpiigaze). Default is eth-xgaze.")
    # parser.add_argument("-c", dest="config_path", required=False, default=None, type=str,
    #                     help="config file path. It must be .config, .json or .yaml.")
    # parser.add_argument("-pu", dest="processing_unit", required=False, default="cpu",
    #                     type=str, choices=['cpu', 'gpu'],
    #                     help="processing unit (cpu or gpu). Default is cpu.")
    # parser.add_argument("--display", dest="display_bool", action='store_true',
    #                     help='If specified, the video will be displayed.')
    # parser.add_argument("--save_data", dest="write_csv", action='store_true',
    #                     help='If specified, the gaze data will be saved as csv.')

    # args = parser.parse_args()
    args = type('obj', (object,), {'video': in_v, "mode": "mpiigaze"})

    # args["video"] = in_v
    # args["output-dir"] = out_d
    # args["mode"] = "mpiigaze"
    # # args.config_path =
    # # args.processing_unit =
    # # args.display_bool =
    args.face_detector = False
    args.device = False
    args.image = False
    args.camera = False
    args.output_dir = out_d
    args.ext = "mp4"
    args.no_screen = False
    # pkg_dir = get_package_dir("ehdg_gaze")
    pkg_dir = r"C:\Users\zawli\Documents\GitHub\ehdg_gaze\src\ehdg_gaze"

    config = load_mode_config(args, pkg_dir)

    expanduser_all(config)
    print(config.gaze_estimator.use_dummy_camera_params)
    if config.gaze_estimator.use_dummy_camera_params:
        print("here")
        generate_dummy_camera_params(config)

    OmegaConf.set_readonly(config, True)
    logger.info(OmegaConf.to_yaml(config))

    # if config.face_detector.mode == 'dlib':
    #     download_dlib_pretrained_model()
    # if args.mode:
    #     if config.mode == 'MPIIGaze':
    #         print(config.mode)
    #         download_mpiigaze_model()
    #     elif config.mode == 'MPIIFaceGaze':
    #         print(config.mode)
    #         download_mpiifacegaze_model()
    #     elif config.mode == 'ETH-XGaze':
    #         print(config.mode)
    #         download_ethxgaze_model()

    check_path_all(config)
    print("end.")
    print(config.face_detector.mode)
    #
    start_time = time.time()
    demo = Demo(config)
    print("demo created")
    return
    demo.run()
    print(f"End time {time.time() - start_time}.")
