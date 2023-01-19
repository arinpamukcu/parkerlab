# Created by Arin Pamukcu, PhD on January 2023 in Chicago, IL

from mars import *
from scipy.stats import zscore
from sklearn.decomposition import FastICA
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# PCA (principal component analysis)

def pca_calcium(data, components):

    # standardize data
    std_peaks = zscore(data, axis=1)  # Q
    std_peaks = np.nan_to_num(std_peaks)

    # get PCA
    data_pca = PCA(n_components=components).fit(std_peaks)  # T
    data_pcaX = PCA(n_components=components).fit_transform(std_peaks)  # R

    # find variance explaiend by each component
    pca_components = data_pca.components_.T  # eigenvector
    pca_expl_var = data_pca.explained_variance_ratio_  # eigenvalue

    # reconstruct data
    pca_computed_matrix = pca_components @ data_pcaX.T

    # find the mean square error and r2 squared of calcium smooth vs computed matrix
    pca_mse = mean_squared_error(data, pca_computed_matrix)
    pca_r2 = r2_score(data, pca_computed_matrix)

    pca_residuals = np.mean(np.square(data - pca_computed_matrix))
    pca_total = np.mean(np.square(data))
    pca_r2_manual = 1 - pca_residuals / pca_total


    # plot PCs
    plt.figure(figsize=(4, 6))

    plt.plot(data_pcaX[:, 0], label='PC 1')
    plt.plot(data_pcaX[:, 1], label='PC 2')
    plt.plot(data_pcaX[:, 2], label='PC 3')
    plt.xlabel('time')
    plt.ylabel('PCs')
    plt.legend()


    # plot PC vs PC
    plt.figure(figsize=(4, 6))

    plt.subplot(131)
    plt.scatter(data_pcaX[:, 0], data_pcaX[:, 1], s=3)
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')

    plt.subplot(132)
    plt.hexbin(data_pcaX[:, 0], data_pcaX[:, 2], gridsize=40, bins='log', mincnt=1)
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')

    plt.subplot(132)
    plt.hexbin(data_pcaX[:, 1], data_pcaX[:, 2], gridsize=40, bins='log', mincnt=1)
    plt.xlabel('PC 2')
    plt.ylabel('PC 3')
    plt.legend()


    # plot variance explained
    plt.figure(figsize=(4, 6))

    plt.subplot(131)
    plt.plot(pca_expl_var.cumsum())
    plt.xlabel('no of PCs')
    plt.ylabel('cumulative explained variance')
    plt.legend()


    # plot 3D phase plot for first three PCs
    fig = plt.figure(figsize=(6, 6))

    ax = fig.add_subplot(131, projection='3d')
    ax.scatter(data_pcaX[:, 0], data_pcaX[:, 1], data_pcaX[:, 2], s=0.5, c=data_pcaX[:, 0], cmap='magma')
    ax.set(xlabel='PC 1', ylabel='PC 2', zlabel='PC 3')


    # compare original data to reconstructed data (individual)
    plt.figure(figsize=(12, 6))

    ax = plt.subplot(211)
    plt.plot(data[1, :].T)
    ax.set(title='original neuron 1', xlabel='time', ylabel='signal')
    plt.xlim(0, 5000)

    ax = plt.subplot(212)
    plt.imshow(pca_computed_matrix[1, :].T)
    ax.set(title='reconstructed neuron 1', xlabel='time', ylabel='signal')
    plt.xlim(0, 5000)


    # compare original data to reconstructed data (population)
    plt.figure(figsize=(12, 6))

    plt.subplot(211)
    plt.imshow(data[:, ::10], aspect='auto')
    plt.colorbar()

    plt.subplot(212)
    plt.imshow(pca_computed_matrix[:, ::10], aspect='auto')
    plt.colorbar()

    plt.show()

    return

# ICA (independent component analysis)


# NMF (non-negative matrix factorization)

