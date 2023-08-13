import glob
import os
from argparse import ArgumentParser

from loguru import logger

from autotrain.cli import BaseAutoTrainCommand


try:
    from autotrain.trainers.dreambooth import train as train_dreambooth
    from autotrain.trainers.dreambooth.params import DreamBoothTrainingParams
    from autotrain.trainers.dreambooth.utils import VALID_IMAGE_EXTENSIONS, XL_MODELS
except ImportError:
    logger.warning(
        "❌ Some DreamBooth components are missing! Please run `autotrain setup` to install it. Ignore this warning if you are not using DreamBooth or running `autotrain setup` already."
    )


def count_images(directory):
    files_grabbed = []
    for files in VALID_IMAGE_EXTENSIONS:
        files_grabbed.extend(glob.glob(os.path.join(directory, "*" + files)))
    return len(files_grabbed)


def run_dreambooth_command_factory(args):
    return RunAutoTrainDreamboothCommand(args)


class RunAutoTrainDreamboothCommand(BaseAutoTrainCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        arg_list = [
            {
                "arg": "--model",
                "help": "Model to use for training",
                "required": True,
                "type": str,
            },
            {
                "arg": "--revision",
                "help": "Model revision to use for training",
                "required": False,
                "type": str,
            },
            {
                "arg": "--tokenizer",
                "help": "Tokenizer to use for training",
                "required": False,
                "type": str,
            },
            {
                "arg": "--vae",
                "help": "VAE to use for training (pretrained_vae_model_name_or_path)",
                "required": False,
                "type": str,
            },
            {
                "arg": "--image-path",
                "help": "Path to the images",
                "required": True,
                "type": str,
            },
            {
                "arg": "--class-image-path",
                "help": "Path to the class images",
                "required": False,
                "type": str,
            },
            {
                "arg": "--prompt",
                "help": "Instance prompt",
                "required": True,
                "type": str,
            },
            {
                "arg": "--class-prompt",
                "help": "Class prompt",
                "required": False,
                "type": str,
            },
            {
                "arg": "--num-class-images",
                "help": "Number of class images",
                "required": False,
                "default": 100,
                "type": int,
            },
            {
                "arg": "--class-labels-conditioning",
                "help": "Class labels conditioning",
                "required": False,
                "type": str,
            },
            {
                "arg": "--prior-preservation",
                "help": "With prior preservation",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--prior-loss-weight",
                "help": "Prior loss weight",
                "required": False,
                "default": 1.0,
                "type": float,
            },
            {
                "arg": "--output",
                "help": "Output directory",
                "required": True,
                "type": str,
            },
            {
                "arg": "--seed",
                "help": "Seed",
                "required": False,
                "default": 42,
                "type": int,
            },
            {
                "arg": "--resolution",
                "help": "Resolution",
                "required": True,
                "type": int,
            },
            {
                "arg": "--center-crop",
                "help": "Center crop",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--train-text-encoder",
                "help": "Train text encoder",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--batch-size",
                "help": "Train batch size",
                "required": False,
                "default": 4,
                "type": int,
            },
            {
                "arg": "--sample-batch-size",
                "help": "Sample batch size",
                "required": False,
                "default": 4,
                "type": int,
            },
            {
                "arg": "--epochs",
                "help": "Number of training epochs",
                "required": False,
                "default": 1,
                "type": int,
            },
            {
                "arg": "--num-steps",
                "help": "Max train steps",
                "required": False,
                "type": int,
            },
            {
                "arg": "--checkpointing-steps",
                "help": "Checkpointing steps",
                "required": False,
                "default": 100000,
                "type": int,
            },
            {
                "arg": "--resume-from-checkpoint",
                "help": "Resume from checkpoint",
                "required": False,
                "type": str,
            },
            {
                "arg": "--gradient-accumulation",
                "help": "Gradient accumulation steps",
                "required": False,
                "default": 1,
                "type": int,
            },
            {
                "arg": "--gradient-checkpointing",
                "help": "Gradient checkpointing",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--lr",
                "help": "Learning rate",
                "required": False,
                "default": 5e-4,
                "type": float,
            },
            {
                "arg": "--scale-lr",
                "help": "Scale learning rate",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--scheduler",
                "help": "Learning rate scheduler",
                "required": False,
                "default": "constant",
            },
            {
                "arg": "--warmup-steps",
                "help": "Learning rate warmup steps",
                "required": False,
                "default": 0,
                "type": int,
            },
            {
                "arg": "--num-cycles",
                "help": "Learning rate num cycles",
                "required": False,
                "default": 1,
                "type": int,
            },
            {
                "arg": "--lr-power",
                "help": "Learning rate power",
                "required": False,
                "default": 1.0,
                "type": float,
            },
            {
                "arg": "--dataloader-num-workers",
                "help": "Dataloader num workers",
                "required": False,
                "default": 0,
                "type": int,
            },
            {
                "arg": "--use-8bit-adam",
                "help": "Use 8bit adam",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--adam-beta1",
                "help": "Adam beta 1",
                "required": False,
                "default": 0.9,
                "type": float,
            },
            {
                "arg": "--adam-beta2",
                "help": "Adam beta 2",
                "required": False,
                "default": 0.999,
                "type": float,
            },
            {
                "arg": "--adam-weight-decay",
                "help": "Adam weight decay",
                "required": False,
                "default": 1e-2,
                "type": float,
            },
            {
                "arg": "--adam-epsilon",
                "help": "Adam epsilon",
                "required": False,
                "default": 1e-8,
                "type": float,
            },
            {
                "arg": "--max-grad-norm",
                "help": "Max grad norm",
                "required": False,
                "default": 1.0,
                "type": float,
            },
            {
                "arg": "--allow-tf32",
                "help": "Allow TF32",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--prior-generation-precision",
                "help": "Prior generation precision",
                "required": False,
                "type": str,
            },
            {
                "arg": "--local-rank",
                "help": "Local rank",
                "required": False,
                "default": -1,
                "type": int,
            },
            {
                "arg": "--xformers",
                "help": "Enable xformers memory efficient attention",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--pre-compute-text-embeddings",
                "help": "Pre compute text embeddings",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--tokenizer-max-length",
                "help": "Tokenizer max length",
                "required": False,
                "type": int,
            },
            {
                "arg": "--text-encoder-use-attention-mask",
                "help": "Text encoder use attention mask",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--rank",
                "help": "Rank",
                "required": False,
                "default": 4,
                "type": int,
            },
            {
                "arg": "--xl",
                "help": "XL",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--fp16",
                "help": "FP16",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--bf16",
                "help": "BF16",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--hub-token",
                "help": "Hub token",
                "required": False,
                "type": str,
            },
            {
                "arg": "--hub-model-id",
                "help": "Hub model id",
                "required": False,
                "type": str,
            },
            {
                "arg": "--push-to-hub",
                "help": "Push to hub",
                "required": False,
                "action": "store_true",
            },
            {
                "arg": "--validation-prompt",
                "help": "Validation prompt",
                "required": False,
                "type": str,
            },
            {
                "arg": "--num-validation-images",
                "help": "Number of validation images",
                "required": False,
                "default": 4,
                "type": int,
            },
            {
                "arg": "--validation-epochs",
                "help": "Validation epochs",
                "required": False,
                "default": 50,
                "type": int,
            },
            {
                "arg": "--checkpoints-total-limit",
                "help": "Checkpoints total limit",
                "required": False,
                "type": int,
            },
            {
                "arg": "--validation-images",
                "help": "Validation images",
                "required": False,
                "type": str,
            },
            {
                "arg": "--logging",
                "help": "Logging using tensorboard",
                "required": False,
                "action": "store_true",
            },
        ]

        run_dreambooth_parser = parser.add_parser("dreambooth", description="✨ Run AutoTrain DreamBooth Training")
        for arg in arg_list:
            if "action" in arg:
                run_dreambooth_parser.add_argument(
                    arg["arg"],
                    help=arg["help"],
                    required=arg.get("required", False),
                    action=arg.get("action"),
                    default=arg.get("default"),
                )
            else:
                run_dreambooth_parser.add_argument(
                    arg["arg"],
                    help=arg["help"],
                    required=arg.get("required", False),
                    type=arg.get("type"),
                    default=arg.get("default"),
                )
        run_dreambooth_parser.set_defaults(func=run_dreambooth_command_factory)

    def __init__(self, args):
        self.args = args
        logger.info(self.args)

        store_true_arg_names = [
            "center_crop",
            "train_text_encoder",
            "gradient_checkpointing",
            "scale_lr",
            "use_8bit_adam",
            "allow_tf32",
            "xformers",
            "pre_compute_text_embeddings",
            "text_encoder_use_attention_mask",
            "xl",
            "fp16",
            "bf16",
            "push_to_hub",
            "logging",
            "prior_preservation",
        ]

        for arg_name in store_true_arg_names:
            if getattr(self.args, arg_name) is None:
                setattr(self.args, arg_name, False)

        if self.args.fp16 and self.args.bf16:
            raise ValueError("❌ Please choose either FP16 or BF16")

        # check if self.args.image_path is a directory with images
        if not os.path.isdir(self.args.image_path):
            raise ValueError("❌ Please specify a valid image directory")

        # count the number of images in the directory. valid images are .jpg, .jpeg, .png
        num_images = count_images(self.args.image_path)
        if num_images == 0:
            raise ValueError("❌ Please specify a valid image directory")

        if self.args.push_to_hub:
            if self.args.hub_model_id is None:
                raise ValueError("❌ Please specify a hub model id")

        if self.args.model in XL_MODELS:
            self.args.xl = True

    def run(self):
        logger.info("Running DreamBooth Training")
        params = DreamBoothTrainingParams(**vars(self.args))
        train_dreambooth(params)
