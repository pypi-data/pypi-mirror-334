import collections
from typing import List, Literal, OrderedDict

import torch

from .common import lazy_normalize


DistanceOptions = Literal["cosine", "euclidean"]
AffinityOptions = Literal["cosine", "rbf", "laplacian"]

# noinspection PyTypeChecker
DISTANCE_TO_AFFINITY: OrderedDict[DistanceOptions, List[AffinityOptions]] = collections.OrderedDict([
    ("cosine", ["cosine"]),
    ("euclidean", ["rbf", "laplacian"]),
])
# noinspection PyTypeChecker
AFFINITY_TO_DISTANCE: OrderedDict[AffinityOptions, DistanceOptions] = collections.OrderedDict(sum([
    [(affinity_type, distance_type) for affinity_type in affinity_types]
    for distance_type, affinity_types in DISTANCE_TO_AFFINITY.items()
], start=[]))



def to_euclidean(x: torch.Tensor, distance_type: DistanceOptions) -> torch.Tensor:
    if distance_type == "cosine":
        return lazy_normalize(x, p=2, dim=-1)
    elif distance_type == "euclidean":
        return x
    else:
        raise ValueError(f"to_euclidean not implemented for distance_type {distance_type}.")


def distance_from_features(
    features: torch.Tensor,
    features_B: torch.Tensor,
    distance_type: DistanceOptions,
):
    """Compute distance matrix from input features.
    Args:
        features (torch.Tensor): input features, shape (n_samples, n_features)
        features_B (torch.Tensor, optional): optional, if not None, compute affinity between two features
        distance_type (str): distance metric, 'cosine' (default) or 'euclidean', 'rbf'.
    Returns:
        (torch.Tensor): affinity matrix, shape (n_samples, n_samples)
    """
    # compute distance matrix from input features
    shape: torch.Size = features.shape[:-2]
    features = features.view((-1, *features.shape[-2:]))
    features_B = features_B.view((-1, *features_B.shape[-2:]))

    match distance_type:
        case "cosine":
            features = lazy_normalize(features, dim=-1)
            features_B = lazy_normalize(features_B, dim=-1)
            D = 1 - features @ features_B.mT
        case "euclidean":
            D = torch.cdist(features, features_B, p=2)
        case _:
            raise ValueError("Distance should be 'cosine' or 'euclidean'")
    return D.view((*shape, *D.shape[-2:]))


def affinity_from_features(
    features: torch.Tensor,
    features_B: torch.Tensor = None,
    affinity_focal_gamma: float = 1.0,
    affinity_type: AffinityOptions = "cosine",
):
    """Compute affinity matrix from input features.

    Args:
        features (torch.Tensor): input features, shape (n_samples, n_features)
        features_B (torch.Tensor, optional): optional, if not None, compute affinity between two features
        affinity_focal_gamma (float): affinity matrix parameter, lower t reduce the edge weights
            on weak connections, default 1.0
        affinity_type (str): distance metric, 'cosine' (default) or 'euclidean'.
    Returns:
        (torch.Tensor): affinity matrix, shape (n_samples, n_samples)
    """
    # compute affinity matrix from input features

    # if feature_B is not provided, compute affinity matrix on features x features
    # if feature_B is provided, compute affinity matrix on features x feature_B
    features_B = features if features_B is None else features_B

    # compute distance matrix from input features
    D = distance_from_features(features, features_B, AFFINITY_TO_DISTANCE[affinity_type])

    # lower affinity_focal_gamma reduce the weak edge weights
    match affinity_type:
        case "cosine" | "laplacian":
            A = torch.exp(-D / affinity_focal_gamma)                                        # [... x n x n]
        case "rbf":
            # Outlier-robust scale invariance using quantiles to estimate standard deviation
            c = 2.0
            p = torch.erf(torch.tensor((-c, c), device=features.device) * (2 ** -0.5))
            stds = torch.nanquantile(features, q=(p + 1) / 2, dim=-2)                       # [2 x ... x d]
            stds = (stds[1] - stds[0]) / (2 * c)                                            # [... x d]
            D = 0.5 * (D / torch.norm(stds, dim=-1)[..., None, None]) ** 2
            A = torch.exp(-D / affinity_focal_gamma)
        case _:
            raise ValueError("Affinity should be 'cosine', 'rbf', or 'laplacian'")

    return A
