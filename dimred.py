# Created by Arin Pamukcu, PhD on January 2023 in Chicago, IL

from mars import *
from scipy.stats import zscore
from sklearn.decomposition import FastICA
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# PCA on calcium event times
def pca(data, components):

    # standardize data
    std_peaks = zscore(data, axis=1)  # Q
    std_peaks = np.nan_to_num(std_peaks)

    # get PCA
    data_pca = PCA(n_components=components).fit(std_peaks)  # T
    data_pcaX = PCA(n_components=components).fit_transform(std_peaks)  # R

    # find variance explaiend by each component
    pca_components =
    pca_peaks_evr = data_pca.explained_variance_ratio_  # variance explained for R
    print(data_pca.explained_variance_ratio_)

    # plot PCs
    plt.figure(figsize=(4, 6))

    plt.plot(data_pcaX[:, 0], label='PC 1')
    plt.plot(data_pcaX[:, 1], label='PC 2')
    plt.plot(data_pcaX[:, 2], label='PC 3')
    plt.xlabel('time')
    plt.ylabel('PCs')


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


    # plot reconstruction
    plt.figure(figsize=(4, 6))

    plt.subplot(131)
    plt.plot((data_pcaX[:, 0]) @ data)
    plt.xlabel('time')
    plt.ylabel('reconstruction')


    # plot variance explained
    plt.figure(figsize=(4, 6))

    plt.subplot(131)
    plt.plot(pca_peaks_evr.cumsum())
    plt.xlabel('no of PCs')
    plt.ylabel('cumulative explained variance')


    # plot 3D plot for first three PCs
    plt.figure(figsize=(5, 9))



    return

# ICA o MARS fts


# NMM

