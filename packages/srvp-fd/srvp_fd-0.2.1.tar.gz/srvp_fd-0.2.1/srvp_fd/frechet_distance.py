"""Fréchet distance calculation module for various video datasets.

This module provides functions to calculate the Fréchet distance between two sets of
video frames using the encoder from the SRVP model to extract features.
"""

import json
import os
import warnings
from typing import Literal, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from huggingface_hub import hf_hub_download
from scipy import linalg

# Import the SRVP model components
from .srvp_model import DCGAN64Encoder, StochasticLatentResidualVideoPredictor

# Define dataset options as Literal type
DatasetType = Literal["mmnist_stochastic", "mmnist_deterministic", "bair", "kth", "human"]

# Map dataset names to their paths in the repository
DATASET_PATHS = {
    "mmnist_stochastic": "mmnist/stochastic",
    "mmnist_deterministic": "mmnist/deterministic",
    "bair": "bair",
    "kth": "kth",
    "human": "human",
}


def _calculate_frechet_distance(
    mu1: np.ndarray, sigma1: np.ndarray, mu2: np.ndarray, sigma2: np.ndarray
) -> float:
    """Calculate Fréchet Distance between two multivariate Gaussians.

    Args:
        mu1: Mean of the first Gaussian distribution
        sigma1: Covariance matrix of the first Gaussian distribution
        mu2: Mean of the second Gaussian distribution
        sigma2: Covariance matrix of the second Gaussian distribution

    Returns:
        Fréchet distance between the two distributions
    """
    # Calculate squared difference between means
    diff = mu1 - mu2

    # Product of covariances
    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    if not np.isfinite(covmean).all():
        offset = np.eye(sigma1.shape[0]) * 1e-6
        covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

    # Check and correct imaginary numbers from sqrt
    if np.iscomplexobj(covmean):
        covmean = covmean.real

    # Calculate Fréchet distance
    tr_covmean = np.trace(covmean)
    return float(diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean)


def _fix_state_dict_keys(state_dict):
    """Fix the keys in the state dict to match the model's expected keys.

    Args:
        state_dict: The state dict loaded from the model file.

    Returns:
        The fixed state dict.
    """
    # Extract only the encoder part of the state dict
    encoder_state_dict = {}
    for key, value in state_dict.items():
        if key.startswith("encoder."):
            encoder_state_dict[key] = value

    # Create a new state dict with only the encoder keys
    new_state_dict = {}
    for key, value in encoder_state_dict.items():
        new_state_dict[key] = value

    return new_state_dict


def _get_model_and_config(
    model_path: Optional[str] = None,
    dataset: Optional[DatasetType] = None,
) -> Tuple[StochasticLatentResidualVideoPredictor, dict]:
    """Load the SRVP model and its configuration.

    Args:
        model_path: Path to the model file. If None, the model will be downloaded from HuggingFace.
        dataset: The dataset to use. Required if model_path is None.
            Options: "mmnist_stochastic", "mmnist_deterministic", "bair", "kth", "human"

    Returns:
        A tuple containing the model and its configuration.

    Raises:
        ValueError: If dataset is None when model_path is None.
        FileNotFoundError: If the model or config file cannot be found.
    """
    if model_path is None:
        if dataset is None:
            raise ValueError(
                "dataset parameter is required when model_path is not provided. "
                "Choose from: mmnist_stochastic, mmnist_deterministic, bair, kth, human"
            )

        # Get the dataset path
        dataset_path = DATASET_PATHS[dataset]

        # Download the model and config from HuggingFace Hub
        try:
            # Create cache directory if it doesn't exist
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "srvp-fd")
            os.makedirs(cache_dir, exist_ok=True)

            # Download the config first
            config_path = hf_hub_download(
                repo_id="nkiyohara/srvp-pretrained-model-mirror",
                filename=f"{dataset_path}/config.json",
                cache_dir=cache_dir,
                force_download=False,
            )
            print(f"Successfully downloaded config from {config_path}")

            # Load config
            with open(config_path) as f:
                config = json.load(f)

            # Check if skipco is True and issue a warning
            if config.get("skipco", False):
                warnings.warn(
                    f"The model for dataset '{dataset}' uses skip connections (skipco=True). "
                    "This may affect the quality of the Fréchet distance calculation, "
                    "as skip connections can bypass the encoder's feature extraction. "
                    "Consider using a model without skip connections for more accurate results.",
                    UserWarning,
                    stacklevel=2,
                )

            # Create a standalone encoder based on config
            encoder = DCGAN64Encoder(
                nc=config["nc"],  # Number of channels from config
                nh=128,  # Feature dimension
                nf=config["nf"],  # Base filters from config
            )

            # Create a dummy model to hold the encoder
            model = StochasticLatentResidualVideoPredictor(
                nx=config["nx"],
                nc=config["nc"],
                nf=config["nf"],
                nhx=config["nhx"],
                ny=config["ny"],
                nz=config["nz"],
                skipco=config["skipco"],
                nt_inf=config["nt_inf"],
                nh_inf=config["nh_inf"],
                nlayers_inf=config["nlayers_inf"],
                nh_res=config["nh_res"],
                nlayers_res=config["nlayers_res"],
                archi=config["archi"],
            )

            # Replace the encoder with our standalone one
            model.encoder = encoder

            return model, config

        except Exception as e:
            print(f"Failed to download or load model: {e}")
            raise FileNotFoundError(
                f"Could not download or load the model for dataset '{dataset}' from HuggingFace. "
                "Please check your internet connection or provide a local model_path."
            ) from e
    else:
        # If model_path is provided, look for config in the same directory
        model_dir = os.path.dirname(model_path)
        config_path = os.path.join(model_dir, "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found at {config_path}. "
                f"Please ensure config.json is in the same directory as the model."
            )

        # Load config
        with open(config_path) as f:
            config = json.load(f)

        # Check if skipco is True and issue a warning
        if config.get("skipco", False):
            warnings.warn(
                "The provided model uses skip connections (skipco=True). "
                "This may affect the quality of the Fréchet distance calculation, "
                "as skip connections can bypass the encoder's feature extraction. "
                "Consider using a model without skip connections for more accurate results.",
                UserWarning,
                stacklevel=2,
            )

        # Create a standalone encoder based on config
        encoder = DCGAN64Encoder(
            nc=config["nc"],  # Number of channels from config
            nh=128,  # Feature dimension
            nf=config["nf"],  # Base filters from config
        )

        # Create a dummy model to hold the encoder
        model = StochasticLatentResidualVideoPredictor(
            nx=config["nx"],
            nc=config["nc"],
            nf=config["nf"],
            nhx=config["nhx"],
            ny=config["ny"],
            nz=config["nz"],
            skipco=config["skipco"],
            nt_inf=config["nt_inf"],
            nh_inf=config["nh_inf"],
            nlayers_inf=config["nlayers_inf"],
            nh_res=config["nh_res"],
            nlayers_res=config["nlayers_res"],
            archi=config["archi"],
        )

        # Replace the encoder with our standalone one
        model.encoder = encoder

        return model, config


def _get_encoder(
    device: Union[str, torch.device] = None,
    model_path: Optional[str] = None,
    dataset: Optional[DatasetType] = None,
) -> nn.Module:
    """Create and return the encoder part of the SRVP model.

    Args:
        device: Device to use for computation.
        model_path: Path to the model file. If provided, will load the encoder from this file.
        dataset: The dataset to use for feature extraction. Required if model_path is None.
            Options: "mmnist_stochastic", "mmnist_deterministic", "bair", "kth", "human"

    Returns:
        The encoder module.

    Raises:
        ValueError: If dataset is None when model_path is None.
    """
    if model_path is not None or dataset is not None:
        try:
            # Try to load the full model first
            model, config = _get_model_and_config(model_path, dataset)
            return model.encoder.to(device)
        except Exception as e:
            print(f"Failed to load full model: {e}")
            print("Creating a standalone encoder instead...")

            # If loading the full model fails, create a standalone encoder
            if dataset is not None or model_path is not None:
                # Get config if possible
                try:
                    if dataset is not None:
                        dataset_path = DATASET_PATHS[dataset]
                        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "srvp-fd")
                        os.makedirs(cache_dir, exist_ok=True)
                        config_path = hf_hub_download(
                            repo_id="nkiyohara/srvp-pretrained-model-mirror",
                            filename=f"{dataset_path}/config.json",
                            cache_dir=cache_dir,
                            force_download=False,
                        )
                    else:
                        model_dir = os.path.dirname(model_path)
                        config_path = os.path.join(model_dir, "config.json")

                    with open(config_path) as f:
                        config = json.load(f)

                    # Create encoder based on config
                    nc = config.get("nc", 1)  # Default to 1 (grayscale)
                    nf = config.get("nf", 32)  # Default to 32 base filters
                except Exception as e:
                    print(f"Failed to load config: {e}")
                    print("Using default encoder parameters...")
                    nc = 1  # Default to grayscale
                    nf = 32  # Default base filters
            else:
                nc = 1  # Default to grayscale
                nf = 32  # Default base filters

            # Create a standalone encoder
            encoder = DCGAN64Encoder(
                nc=nc,  # Number of channels
                nh=128,  # Feature dimension
                nf=nf,  # Base filters
            )

            if device is not None:
                encoder = encoder.to(device)

            return encoder

    # Create a default encoder for MMNIST (grayscale)
    # This is kept for backward compatibility
    warnings.warn(
        "No model_path or dataset specified. Creating a default encoder for Moving MNIST. "
        "For better results, specify a dataset or model_path.",
        UserWarning,
        stacklevel=2,
    )

    encoder = DCGAN64Encoder(
        nc=1,  # Moving MNIST is grayscale
        nh=128,  # Match the feature dimension of the SRVP model
        nf=32,  # Match the base filters of the SRVP model
    )

    if device is not None:
        encoder = encoder.to(device)

    return encoder


def _validate_input_shapes(images1: torch.Tensor, images2: torch.Tensor) -> None:
    """Validate the shapes of the input tensors.

    Args:
        images1: First set of images.
        images2: Second set of images.

    Raises:
        ValueError: If the input shapes are invalid.
    """
    # Check dimensions
    if images1.dim() != 4 or images2.dim() != 4:
        raise ValueError(
            f"Input tensors must be 4D (batch, channels, height, width). "
            f"Got shapes {images1.shape} and {images2.shape}."
        )

    # Check channel dimensions match
    if images1.shape[1] != images2.shape[1]:
        raise ValueError(
            f"Channel dimensions must match. Got {images1.shape[1]} and {images2.shape[1]}."
        )

    # Check spatial dimensions match
    if images1.shape[2:] != images2.shape[2:]:
        raise ValueError(
            f"Spatial dimensions must match. Got {images1.shape[2:]} and {images2.shape[2:]}."
        )

    # Check that sample size is greater than 128 (feature dimension)
    if images1.shape[0] <= 128 or images2.shape[0] <= 128:
        raise ValueError(
            f"Sample size must be greater than 128 (feature dimension). "
            f"Got {images1.shape[0]} and {images2.shape[0]}."
        )


class FrechetDistanceCalculator:
    """A class for calculating Fréchet distance between sets of images.

    This class loads the SRVP encoder model once during initialization and
    can be reused for multiple Fréchet distance calculations, avoiding
    repeated model loading.

    Attributes:
        encoder: The encoder model used for feature extraction.
        device: The device used for computation.
    """

    def __init__(
        self,
        dataset: DatasetType = "mmnist_stochastic",
        model_path: Optional[str] = None,
        device: Union[str, torch.device] = None,
    ):
        """Initialize the Fréchet distance calculator.

        Args:
            dataset: The dataset to use for feature extraction. Required if model_path is None.
                Options: "mmnist_stochastic", "mmnist_deterministic", "bair", "kth", "human"
            model_path: Path to the model file. If provided, will use this model instead of
                downloading.
            device: Device to use for computation. If None, will use CUDA if available,
                otherwise CPU.
        """
        # Get the device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device

        # Get the encoder
        self.encoder = _get_encoder(self.device, model_path, dataset)
        self.encoder.eval()  # Set to evaluation mode

    def __call__(
        self,
        images1: torch.Tensor,
        images2: torch.Tensor,
    ) -> float:
        """Calculate the Fréchet distance between two sets of images.

        Args:
            images1: First set of images. Shape: [batch_size, channels, height, width]
            images2: Second set of images. Shape: [batch_size, channels, height, width]

        Returns:
            The Fréchet distance between the two sets of images.

        Raises:
            ValueError: If the input shapes are invalid.
        """
        # Validate input shapes
        _validate_input_shapes(images1, images2)

        # Extract features
        with torch.no_grad():
            features1 = self.encoder(images1.to(self.device))
            features2 = self.encoder(images2.to(self.device))

        # Convert to numpy arrays
        features1 = features1.cpu().numpy()
        features2 = features2.cpu().numpy()

        # Calculate mean and covariance
        mu1 = np.mean(features1, axis=0)
        sigma1 = np.cov(features1, rowvar=False)
        mu2 = np.mean(features2, axis=0)
        sigma2 = np.cov(features2, rowvar=False)

        # Calculate Fréchet distance
        return _calculate_frechet_distance(mu1, sigma1, mu2, sigma2)

    def extract_features(self, images: torch.Tensor) -> np.ndarray:
        """Extract features from a set of images.

        This method can be used to extract features from images for later use,
        which can be useful when you want to compare multiple sets of images
        against a reference set.

        Args:
            images: Set of images. Shape: [batch_size, channels, height, width]

        Returns:
            Numpy array of features with shape [batch_size, feature_dim]
        """
        # Validate input shape
        if not isinstance(images, torch.Tensor):
            raise ValueError("Images must be a torch.Tensor")
        if len(images.shape) != 4:
            raise ValueError(f"Images must have 4 dimensions, got {len(images.shape)}")

        # Extract features
        with torch.no_grad():
            features = self.encoder(images.to(self.device))

        # Convert to numpy array
        return features.cpu().numpy()

    def calculate_frechet_distance_from_features(
        self, features1: np.ndarray, features2: np.ndarray
    ) -> float:
        """Calculate Fréchet distance from pre-extracted features.

        Args:
            features1: First set of features. Shape: [batch_size, feature_dim]
            features2: Second set of features. Shape: [batch_size, feature_dim]

        Returns:
            The Fréchet distance between the two sets of features.
        """
        # Calculate mean and covariance
        mu1 = np.mean(features1, axis=0)
        sigma1 = np.cov(features1, rowvar=False)
        mu2 = np.mean(features2, axis=0)
        sigma2 = np.cov(features2, rowvar=False)

        # Calculate Fréchet distance
        return _calculate_frechet_distance(mu1, sigma1, mu2, sigma2)


def frechet_distance(
    images1: torch.Tensor,
    images2: torch.Tensor,
    dataset: DatasetType = "mmnist_stochastic",
    model_path: Optional[str] = None,
    device: Union[str, torch.device] = None,
) -> float:
    """Calculate the Fréchet distance between two sets of images.

    Args:
        images1: First set of images. Shape: [batch_size, channels, height, width]
        images2: Second set of images. Shape: [batch_size, channels, height, width]
        dataset: The dataset to use for feature extraction. Required if model_path is None.
            Options: "mmnist_stochastic", "mmnist_deterministic", "bair", "kth", "human"
        model_path: Path to the model file. If provided, will use this model instead of downloading.
        device: Device to use for computation. If None, will use CUDA if available, otherwise CPU.

    Returns:
        The Fréchet distance between the two sets of images.

    Raises:
        ValueError: If the input shapes are invalid.
    """
    # Validate input shapes
    _validate_input_shapes(images1, images2)

    # Get the device
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Get the encoder
    encoder = _get_encoder(device, model_path, dataset)
    encoder.eval()  # Set to evaluation mode

    # Extract features
    with torch.no_grad():
        features1 = encoder(images1.to(device))
        features2 = encoder(images2.to(device))

    # Convert to numpy arrays
    features1 = features1.cpu().numpy()
    features2 = features2.cpu().numpy()

    # Calculate mean and covariance
    mu1 = np.mean(features1, axis=0)
    sigma1 = np.cov(features1, rowvar=False)
    mu2 = np.mean(features2, axis=0)
    sigma2 = np.cov(features2, rowvar=False)

    # Calculate Fréchet distance
    return _calculate_frechet_distance(mu1, sigma1, mu2, sigma2)
