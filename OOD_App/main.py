from omegaconf import OmegaConf
from tqdm import tqdm
import numpy as np
from .utils.utils import build_cfg_path, form_list_from_user_input, sanity_check
import os

def main(args_cli):
    # config
    args_yml = OmegaConf.load(build_cfg_path(args_cli.feature_type))
    args = OmegaConf.merge(args_yml, args_cli)  # the latter arguments are prioritized
    # OmegaConf.set_readonly(args, True)
    sanity_check(args)

    # verbosing with the print -- haha (TODO: logging)
    print(OmegaConf.to_yaml(args))
    if args.on_extraction in ['save_numpy', 'save_pickle']:
        print(f'Saving features to {args.output_path}')
    print('Device:', args.device)

    # import are done here to avoid import errors (we have two conda environements)
    if args.feature_type == 'i3d':
        from .all_models.i3d.extract_i3d import ExtractI3D as Extractor
    elif args.feature_type == 'r21d':
        from .all_models.r21d.extract_r21d import ExtractR21D as Extractor
    elif args.feature_type == 's3d':
        from .all_models.s3d.extract_s3d import ExtractS3D as Extractor
    elif args.feature_type == 'vggish':
        from .all_models.vggish.extract_vggish import ExtractVGGish as Extractor
    elif args.feature_type == 'resnet':
        from .all_models.resnet.extract_resnet import ExtractResNet as Extractor
    elif args.feature_type == 'raft':
        from .all_models.raft.extract_raft import ExtractRAFT as Extractor
    elif args.feature_type == 'pwc':
        from .all_models.pwc.extract_pwc import ExtractPWC as Extractor
    elif args.feature_type == 'clip':
        from .all_models.clip.extract_clip import ExtractCLIP as Extractor
    else:
        raise NotImplementedError(f'Extractor {args.feature_type} is not implemented.')

    extractor = Extractor(args)

    # unifies whatever a user specified as paths into a list of paths
    video_paths = form_list_from_user_input(args.video_paths, args.file_with_video_paths, to_shuffle=True)

    #video_paths=np.load('testing_paths.npy')
    
    for video_path in video_paths:
        result=extractor._extract(video_path)  # note the `_` in the method name
        return result
    # yep, it is this simple!



