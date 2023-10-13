import os
import sklearn # type: ignore
import numpy as np
import pandas as pd # type: ignore
from matplotlib import pyplot as plt # type: ignore
import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
import random
from typing import List, Tuple, Dict, Callable, Union, Optional

def MixtureGaussian(ncomp: int,
                    ndims: int,
                    seed: int = 0) -> tfp.distributions.Mixture:
    """
    Correlated mixture of Gaussians used in https://arxiv.org/abs/2302.12024 
    with ncomp = 3 and ndims varying from 4 to 1000
    
    Args:
        ncomp: int, number of components
        ndims: int, number of dimensions
        seed: int, random seed

    Returns:
        targ_dist: tfp.distributions.Mixture, mixture of Gaussians
    """
    targ_dist: tfp.distributions.Mixture = MixMultiNormal1(ncomp, ndims, seed = seed)
    return targ_dist

def MixNormal1(n_components: int = 3,
               n_dimensions: int = 4,
               seed: int = 0) -> tfp.distributions.Mixture:
    """
    Defines a mixture of 'n_components' Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to that of 'loc' and 'scale'). This means that each component in each
    dimension can be assigned a different probability.

    The resulting multivariate distribution has small correlation.

    Note: The functions 'MixNormal1' and 'MixNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixNormal2' and 'MixNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed
        
    Returns:
        mix_gauss: tfp.distributions.Mixture, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample([n_dimensions,n_components])
    components: List[tfp.distributions.Normal] = []
    for i in range(n_components):
        components.append(tfp.distributions.Normal(loc = loc[i],
                                     scale = scale[i]))
    mix_gauss: tfp.distributions.Mixture = tfp.distributions.Mixture(
        cat = tfp.distributions.Categorical(probs=probs),
        components = components,
        validate_args = True)
    return mix_gauss
    
def MixNormal2(n_components: int = 3,
               n_dimensions: int = 4,
               seed: int = 0) -> tfp.distributions.Mixture:
    """
    Defines a mixture of 'n_components' Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each component in all
    dimension is assigned a single probability.

    The resulting multivariate distribution has small correlation.

    Note: The functions 'MixNormal1' and 'MixNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixNormal2' and 'MixNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed

    Returns:    
        mix_gauss: tfp.distributions.MixtureSameFamily, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample(n_components)
    mix_gauss: tfp.distributions.MixtureSameFamily = tfp.distributions.MixtureSameFamily(
        mixture_distribution = tfp.distributions.Categorical(probs = probs),
        components_distribution = tfp.distributions.Normal(loc = loc,
                                             scale = scale),
        validate_args = True)
    return mix_gauss

def MixNormal1_indep(n_components: int = 3,
                     n_dimensions: int = 4,
                     seed: int = 0) -> tfp.distributions.Independent:
    """
    Defines a mixture of 'n_components' Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to that of 'loc' and 'scale'). This means that each component in each
    dimension can be assigned a different probability.

    The resulting multivariate distribution has small correlation.

    Note: The functions 'MixNormal1' and 'MixNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixNormal2' and 'MixNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed

    Returns:
        mix_gauss: tfp.distributions.Independent, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample([n_dimensions,n_components])
    components: List[tfp.distributions.Normal] = []
    for i in range(n_components):
        components.append(tfp.distributions.Normal(loc = loc[i], 
                                     scale = scale[i]))
    mix_gauss: tfp.distributions.Independent = tfp.distributions.Independent(
        distribution = tfp.distributions.Mixture(cat = tfp.distributions.Categorical(probs = probs),
                                   components = components,
                                   validate_args = True),
        reinterpreted_batch_ndims = 0)
    return mix_gauss
    
def MixNormal2_indep(n_components: int = 3,
                     n_dimensions: int = 4,  
                     seed: int = 0) -> tfp.distributions.Independent:
    """
    Defines a mixture of 'n_components' Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each component in all
    dimension is assigned a single probability.

    The resulting multivariate distribution has small correlation.

    Note: The functions 'MixNormal1' and 'MixNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixNormal2' and 'MixNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed
        
    Returns:
        mix_gauss: tfp.distributions.Independent, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample(n_components)
    mix_gauss: tfp.distributions.Independent = tfp.distributions.Independent(
        distribution = tfp.distributions.MixtureSameFamily(mixture_distribution = tfp.distributions.Categorical(probs = probs),
                                             components_distribution = tfp.distributions.Normal(loc = loc,
                                                                                  scale = scale),
                                             validate_args = True),
        reinterpreted_batch_ndims = 0)
    return mix_gauss

def MixMultiNormal1(n_components: int = 3,
                    n_dimensions: int = 4,
                    seed: int = 0) -> tfp.distributions.Mixture:
    """
    Defines a mixture of 'n_components' Multivariate Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each Multivariate distribution 
    is assigned a single probability.

    The resulting multivariate distribution has large (random) correlation.

    Note: The functions 'MixMultiNormal1' and 'MixMultiNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixMultiNormal2' and 'MixMultiNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed
        
    Returns:
        mix_gauss: tfp.distributions.Mixture, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample(n_components)
    components: List[tfp.distributions.MultivariateNormalDiag] = []
    for i in range(n_components):
        components.append(tfp.distributions.MultivariateNormalDiag(loc = loc[i],
                                                     scale_diag = scale[i]))
    mix_gauss: tfp.distributions.Mixture = tfp.distributions.Mixture(
        cat = tfp.distributions.Categorical(probs = probs),
        components = components,
        validate_args = True)
    return mix_gauss
    
def MixMultiNormal2(n_components: int = 3,
                    n_dimensions: int = 4,
                    seed: int = 0) -> tfp.distributions.MixtureSameFamily:
    """
    Defines a mixture of 'n_components' Multivariate Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each Multivariate distribution 
    is assigned a single probability.

    The resulting multivariate distribution has large (random) correlation.

    Note: The functions 'MixMultiNormal1' and 'MixMultiNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixMultiNormal2' and 'MixMultiNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed

    Returns:
        mix_gauss: tfp.distributions.MixtureSameFamily, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs = np.random.sample(n_components)
    mix_gauss: tfp.distributions.MixtureSameFamily = tfp.distributions.MixtureSameFamily(
        mixture_distribution = tfp.distributions.Categorical(probs = probs),
        components_distribution = tfp.distributions.MultivariateNormalDiag(loc = loc,
                                                             scale_diag = scale),
        validate_args=True)
    return mix_gauss

def MixMultiNormal1_indep(n_components: int = 3,
                          n_dimensions: int = 4,
                          seed: int = 0) -> tfp.distributions.Independent:
    """
    Defines a mixture of 'n_components' Multivariate Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each Multivariate distribution 
    is assigned a single probability.

    The resulting multivariate distribution has large (random) correlation.

    Note: The functions 'MixMultiNormal1' and 'MixMultiNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixMultiNormal2' and 'MixMultiNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed

    Returns:
        mix_gauss: tfp.distributions.Independent, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample(n_components)
    components: List[tfp.distributions.MultivariateNormalDiag]
    for i in range(n_components):
        components.append(tfp.distributions.MultivariateNormalDiag(loc = loc[i],
                                                     scale_diag = scale[i]))
    mix_gauss: tfp.distributions.Independent = tfp.distributions.Independent(
        distribution = tfp.distributions.Mixture(cat = tfp.distributions.Categorical(probs = probs),
                                   components = components,
                                   validate_args = True),
        reinterpreted_batch_ndims = 0)
    return mix_gauss
    
def MixMultiNormal2_indep(n_components: int = 3,
                          n_dimensions: int = 4,
                          seed: int = 0) -> tfp.distributions.Independent:
    """
    Defines a mixture of 'n_components' Multivariate Normal distributions in 'n_dimensions' dimensions 
    with means and stddevs given by the tensors 'loc' and 'scale' with shapes 
    '(n_components,n_dimensions)'.
    The components are mixed according to the categorical distribution with probabilities
    'probs' (with shape equal to 'n_components'). This means that each Multivariate distribution 
    is assigned a single probability.

    The resulting multivariate distribution has large (random) correlation.

    Note: The functions 'MixMultiNormal1' and 'MixMultiNormal1_indep'
    generate identical samples, different from the samples generated by
    'MixMultiNormal2' and 'MixMultiNormal2_indep' (also identical).
    
    Args:
        n_components: int, number of components
        n_dimensions: int, number of dimensions
        seed: int, random seed

    Returns:
        mix_gauss: tfp.distributions.Independent, mixture of Gaussians
    """
    reset_random_seeds(seed)
    loc: np.ndarray = np.random.sample([n_components, n_dimensions]) * 10
    scale: np.ndarray = np.random.sample([n_components,n_dimensions])
    probs: np.ndarray = np.random.sample(n_components)

    mix_gauss: tfp.distributions.Independent = tfp.distributions.Independent(
        distribution = tfp.distributions.MixtureSameFamily(mixture_distribution = tfp.distributions.Categorical(probs = probs),
                                             components_distribution = tfp.distributions.MultivariateNormalDiag(loc = loc,
                                                                                                  scale_diag = scale),
                                             validate_args = True),
        reinterpreted_batch_ndims = 0)
    return mix_gauss

def describe_distributions(distributions: List[tfp.distributions.Distribution]) -> None:
    """
    Describes a 'tfp.distributions' object.
    
    Args:
        distributions: list of 'tfp.distributions' objects, distributions to describe

    Returns:
        None (prints the description)
    """
    print('\n'.join([str(d) for d in distributions]))

def rot_matrix(data: np.ndarray) -> np.ndarray:
    """
    Calculates the matrix that rotates the covariance matrix of 'data' to the diagonal basis.

    Args:
        data: np.ndarray, data to rotate

    Returns:
        rotation: np.ndarray, rotation matrix
    """
    cov_matrix: np.ndarray = np.cov(data, rowvar=False)
    w: np.ndarray
    V: np.ndarray
    w, V = np.linalg.eig(cov_matrix)
    return V

def transform_data(data: np.ndarray,
                   rotation: np.ndarray) -> np.ndarray:
    """
    Transforms the data according to the rotation matrix 'rotation'.
    
    Args:
        data: np.ndarray, data to transform
        rotation: np.ndarray, rotation matrix

    Returns:
        data_new: np.ndarray, transformed data
    """
    if len(rotation.shape) != 2:
        raise Exception('Rottion matrix must be a 2D matrix.')
    elif rotation.shape[0] != rotation.shape[1]:
        raise Exception('Rotation matrix must be square.')
    data_new: np.ndarray = np.dot(data,rotation)
    return data_new

def inverse_transform_data(data: np.ndarray,
                           rotation: np.ndarray) -> np.ndarray:
    """
    Transforms the data according to the inverse of the rotation matrix 'rotation'.
    
    Args:
        data: np.ndarray, data to transform
        rotation: np.ndarray, rotation matrix
        
    Returns:
        data_new: np.ndarray, transformed data
    """
    if len(rotation.shape) != 2:
        raise Exception('Rottion matrix must be a 2D matrix.')
    elif rotation.shape[0] != rotation.shape[1]:
        raise Exception('Rotation matrix must be square.')
    data_new: np.ndarray = np.dot(data,np.transpose(rotation))
    return data_new

def reset_random_seeds(seed: int = 0) -> None:
    """
    Resets the random seeds of the packages 'tensorflow', 'numpy' and 'random'.
    
    Args:
        seed: int, random seed
        
    Returns:
        None
    """
    os.environ['PYTHONHASHSEED'] = str(seed)
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

def RandCorr(matrixSize: int,
             seed: int) -> np.ndarray:
    """
    Generates a random correlation matrix of size 'matrixSize' x 'matrixSize'.

    Args:
        matrixSize: int, size of the matrix
        seed: int, random seed
        
    Returns:
        Vnorm: np.ndarray, normalized random correlation matrix
    """
    np.random.seed(0)
    V: np.ndarray = sklearn.datasets.make_spd_matrix(matrixSize,
                                                     random_state = seed)
    D: np.ndarray = np.sqrt(np.diag(np.diag(V)))
    Dinv: np.ndarray = np.linalg.inv(D)
    Vnorm: np.ndarray = np.matmul(np.matmul(Dinv,V),Dinv)
    return Vnorm

def is_pos_def(x: np.ndarray) -> bool:
    """ 
    Checks if the matrix 'x' is positive definite.
    
    Args:
        x: np.ndarray, matrix to check

    Returns:
        bool, True if 'x' is positive definite, False otherwise
    """
    if len(x.shape) != 2:
        raise Exception('Input to is_pos_def must be a 2-dimensional array.')
    elif x.shape[0] != x.shape[1]:
        raise Exception('Input to is_pos_def must be a square matrix.')
    return bool(np.all(np.linalg.eigvals(x) > 0))

def RandCov(std: np.ndarray,
            seed: int) -> np.ndarray:
    """
    Generates a random covariance matrix of size 'matrixSize' x 'matrixSize'.

    Args:
        std: np.ndarray, standard deviations of the random variables
        seed: int, random seed
        
    Returns:
        V: np.ndarray, random covariance matrix
    """
    matrixSize: int = len(std)
    corr: np.ndarray = RandCorr(matrixSize,seed)
    D: np.ndarray = np.diag(std)
    V: np.ndarray = np.matmul(np.matmul(D,corr),D)
    return V

def plot_corr_matrix(X: np.ndarray) -> None:
    """
    Plots the correlation matrix of the data 'X'.
    
    Args:
        X: np.ndarray, data to plot the correlation matrix of

    Returns:
        None (plots the correlation matrix)
    """
    df: pd.DataFrame = pd.DataFrame(X)
    f: plt.Figure = plt.figure(figsize=(18, 18))
    plt.matshow(df.corr(), fignum=f.number)
    cb = plt.colorbar()
    plt.grid(False)
    plt.show()
    plt.close()