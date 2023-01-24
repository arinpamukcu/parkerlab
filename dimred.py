# Created by Arin Pamukcu, PhD on January 2023 in Chicago, IL

from mars import *
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.stats import zscore
from sklearn.decomposition import FastICA
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# PCA (principal component analysis)
# ICA (independent component analysis)
# NMF (non-negative matrix factorization)

def pca_calcium(data, components):

    # standardize data
    std_peaks = zscore(data, axis=1)  # Q
    std_peaks = np.nan_to_num(std_peaks)

    # get PCA
    data_pca = PCA(n_components=components).fit(std_peaks)  # T
    data_pcaX = PCA(n_components=components).fit_transform(std_peaks)  # R

    # find variance explained by each component
    pca_weights = data_pca.components_.T  # eigenvector
    pca_expl_var = data_pca.explained_variance_ratio_  # eigenvalue

    # reconstruct data
    pca_computed_data = pca_weights @ data_pcaX.T

    # find the mean square error and r2 squared of calcium smooth vs computed matrix
    pca_mse = mean_squared_error(data, pca_computed_data)
    pca_r2 = r2_score(data, pca_computed_data)

    pca_residuals = np.mean(np.square(data - pca_computed_data))
    pca_total = np.mean(np.square(data))
    pca_r2_manual = 1 - pca_residuals / pca_total

    return data_pcaX, pca_expl_var, pca_weights, pca_computed_data


def pca_plots(data, components):

    data_pcaX, pca_expl_var, pca_weights, pca_computed_data = pca_calcium(data, components)

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
    plt.imshow(pca_computed_data[1, :].T)
    ax.set(title='reconstructed neuron 1', xlabel='time', ylabel='signal')
    plt.xlim(0, 5000)

    # compare original data to reconstructed data (population)
    plt.figure(figsize=(12, 6))

    plt.subplot(211)
    plt.imshow(data[:, ::10], aspect='auto')
    plt.colorbar()

    plt.subplot(212)
    plt.imshow(pca_computed_data[:, ::10], aspect='auto')
    plt.colorbar()

    plt.show()

    return


def pca_sort(data, components):
    data_pcaX, pca_expl_var, pca_weights, pca_computed_matrix = pca_calcium(data, components)

    # concatenate PC data on dataT
    df_data = pd.DataFrame(data)

    # oncatenate PC data on dataT
    df_data['PCA1'] = pca_weights[:, 0]  # chose which PC you want to sort with
    df_data['PCA2'] = pca_weights[:, 1]
    df_data['PCA3'] = pca_weights[:, 2]
    # df_data.head()

    # sort data wrt PCs
    df_sorted_pca1 = df_data.sort_values(by='PCA1', ascending=False)
    df_sorted_pca2 = df_data.sort_values(by='PCA2', ascending=False)
    df_sorted_pca3 = df_data.sort_values(by='PCA3', ascending=False)

    sorted_pca1 = df_sorted_pca1.iloc[:, :-4].to_numpy()
    sorted_pca2 = df_sorted_pca2.iloc[:, :-4].to_numpy()
    sorted_pca3 = df_sorted_pca3.iloc[:, :-4].to_numpy()
    # df_sorted_pca1.head()

    plt.figure(figsize=(20, 9))

    ax = plt.subplot(3, 1, 1)
    plt.imshow(sorted_pca1[:, :], aspect='auto')
    # plt.xlabel('time (s)')
    plt.ylabel('sorted wrt PC 1')
    plt.colorbar()

    ax = plt.subplot(3, 1, 2)
    plt.imshow(sorted_pca2[:, :], aspect='auto')
    # plt.xlabel('time (s)')
    plt.ylabel('sorted wrt PC 2')
    plt.colorbar()

    ax = plt.subplot(3, 1, 3)
    plt.imshow(sorted_pca3[:, :], aspect='auto')
    plt.xlabel('time (s)')
    plt.ylabel('sorted wrt PC 3')
    plt.colorbar()

    # plot first 15 neurons
    plt.figure(figsize=(20, 10))

    ax = plt.subplot(10, 1, 1)
    plt.plot(data_pcaX[:, 0])
    plt.xlabel('time (s)')
    plt.ylabel('PC')
    plt.xlim(0, 4500)
    plt.axis('off')
    plt.legend()

    for n in range(0, 9):
        ax = plt.subplot(15, 1, n + 2)
        plt.plot(sorted_pca1[n, :])
        plt.xlim((0, 4500))
        # plt.ylim((-2,6))
        plt.axis('off')


def pca_varexpl(data):

    time = len(data)

    data_train = data[:, int(time * 0.2):]
    data_test = data[:, :int(time * 0.2)]

    pca_var_mse = []
    pca_var_r2 = []

    for n in range(1, 51):
        # fit pca with component no = n
        pca = PCA(n)
        pca_train = pca.fit(data_train.T)
        pca_test = pca.transform(data_test.T)

        # compute predicted matrix calculated from pca with the assigned component number
        pca_train_weights = pca_train.components_
        pca_train_weights = pca_train_weights.T
        pca_computed_data = pca_train_weights @ pca_test.T

        # find the mean square error and r squared between original and computed matrices
        pca_mse = mean_squared_error(data_test, pca_computed_data)
        pca_r2 = r2_score(data_test, pca_computed_data)
        print("R^2 for PCA", str(n), ":", str(pca_r2))

        # append the mean square error and r squared for each ic in a separate matrix
        pca_var_mse.append(pca_mse)
        pca_var_r2.append(pca_r2)

    # print(pca_var)

    # plot change in R squared
    plt.subplot(1, 3, 3)
    pca_var_r2 = np.array(pca_var_r2)
    plt.plot((pca_var_r2[1:] - pca_var_r2[:-1]))
    plt.xlabel('PC')
    plt.ylabel('Change in R squared');

    return


def ica_calcium(data, component):

    # smooth, then whiten data
    time = len(data)
    data = gaussian_filter1d(data, sigma=20)  # smooth
    data = (data - np.nanmean(data)) / np.nanstd(data)  # whiten

    ica = FastICA(n_components=component)
    data_ica = ica.fit(data.T)
    data_icaX = ica.transform(data.T)

    # plot ICAs
    plt.figure(figsize=(20, 7.5))

    plt.subplot(3, 1, 1)
    plt.plot(data_icaX[:, 0])
    plt.xlim(0, time)

    # reconstruct data
    ica_weights = data @ np.linalg.pinv(data_icaX.T)
    ica_computed_data = ica_weights @ data_icaX.T

    # find the mean square error and r2 squared of calcium smooth vs computed matrix
    ica_mse = mean_squared_error(data, ica_computed_data)
    ica_r2 = r2_score(data, ica_computed_data)

    ica_residuals = np.mean(np.square(data - ica_computed_data))
    ica_total = np.mean(np.square(data))
    ica_r2_manual = 1 - ica_residuals / ica_total

    # compare Ca signal from original and computed matrices
    plt.figure(figsize=(20, 7.5))

    ax = plt.subplot(2, 1, 1)
    plt.plot(data[1, :].T)
    ax.set(title='original neuron 1', xlabel='time (s)', ylabel='Ca signal')
    plt.xlim(0, time)

    ax = plt.subplot(2, 1, 2)
    plt.plot(ica_computed_data[1, :].T)
    ax.set(title='computed neuron 1', xlabel='time (s)', ylabel='Ca signal')
    plt.xlim(0, time)

    plt.figure(figsize=(20, 6))

    ax = plt.subplot(1, 5, 1)
    plt.hist(data_icaX[:, 1])
    plt.gca().set(title='Frequency Histogram', xlabel='IC1 for time', ylabel='Frequency');

    return data_icaX, ica_weights, ica_computed_data


def ica_sort(data, component):

    data_icaX, ica_weights, ica_computed_data = ica_calcium(data, component)

    # concatenate NMF weights on data
    df_data = pd.DataFrame(data)
    df_data['IC1'] = ica_weights[:, 0]  # chose which ICA component you want to sort with
    df_data.head()

    # sort data by ICA
    df_data_ica_sorted = df_data.sort_values(by='IC1', ascending=False)
    # print(df_sorted_ica)
    data_ica_sorted = df_data_ica_sorted.iloc[:, :-3].to_numpy()

    # plot data sorted by ICA-1 for first and last 50 neurons
    data_ica_sorted_firstlast = np.concatenate((data_ica_sorted[:50, :], data_ica_sorted[-50:, :]))

    # plt.figure(figsize = (20,4))
    plt.imshow(data_ica_sorted_firstlast, aspect='auto')
    plt.xlabel('time (s)')
    plt.ylabel('50/50 neurons sorted by IC1')
    plt.colorbar()

    return


def ica_varexpl(data):

    time = len(data)
    data = gaussian_filter1d(data, sigma=20)  # smooth
    data = (data - np.nanmean(data)) / np.nanstd(data)  # whiten

    # fit the data using training set, find MSEs using test set
    data_train = data[:, int(time * 0.2):]
    data_test = data[:, :int(time * 0.2)]

    ica_var_mse = []
    ica_var_r2 = []

    for n in range(1, 51):
        # fit ica with component no = n
        ica = FastICA(n)
        ica_train = ica.fit_transform(data_train.T)
        ica_test = ica.transform(data_test.T)

        # compute predicted matrix calculated from icas with the assigned component number
        ica_weights = data_train @ np.linalg.pinv(ica_train.T)
        ica_computed_matrix = ica_weights @ ica_test.T

        # find the mean square error and r squared between original and computed matrices
        mse = mean_squared_error(data_test, ica_computed_matrix)
        r2 = r2_score(data_test, ica_computed_matrix)
        print("R^2 for IC", str(n), ":", str(r2))

        # append the mean square error and r squared for each ic in a separate matrix
        ica_var_mse.append(mse)
        ica_var_r2.append(r2)

    # plot MSE and R squared
    ax = plt.subplot(1, 3, 1)
    plt.plot(ica_var_mse)
    ax.set(xlabel='ICs', ylabel='MSE')

    # plot R squared
    ax = plt.subplot(1, 3, 2)
    plt.plot(ica_var_r2)
    ax.set(xlabel='ICs', ylabel='R squared')

    # plot change in R squared
    plt.subplot(1, 3, 3)
    ica_var_r2 = np.array(ica_var_r2)
    plt.plot((ica_var_r2[1:] - ica_var_r2[:-1]))
    plt.xlabel('ICs')
    plt.ylabel('Change in R squared')

    return


def nmf_calcium(data, component):

    # nmf = NMF(n_components=component, init='random', random_state=0)
    # V = nmf.fit(calcium_smooth)
    # W = nmf.fit_transform(calcium_smooth)
    # H = nmf.components_

    data_nmf = NMF(n_components=component).fit(data.T)
    data_nmfX = NMF(n_components=component).fit_transform(data.T)
    nmf_weights = data_nmf.components_

    # # find variance explaiend by each component
    # data_nmf_evr = data_nmf.explained_variance_ratio_
    # print(data_nmf_evr)

    # reconstruct data
    nmf_computed_data = nmf_weights @ data_nmfX.T

    # find the mean square error and r2 squared of calcium smooth vs computed matrix
    nmf_mse = mean_squared_error(data, nmf_computed_data)
    nmf_r2 = r2_score(data, nmf_computed_data)

    nmf_residuals = np.mean(np.square(data - nmf_computed_data))
    nmf_total = np.mean(np.square(data))
    nmf_r2_manual = 1 - nmf_residuals / nmf_total

    # compare data from original and computed matrices
    ax = plt.subplot(1, 2, 1)
    plt.plot(data[1, :].T)
    ax.set(title='original neuron 1', xlabel='time', ylabel='Ca signal')
    plt.xlim(0, 5000)

    ax = plt.subplot(1, 2, 2)
    plt.plot(nmf_computed_data[1, :].T)
    ax.set(title='computed neuron 1', xlabel='time', ylabel='Ca signal')
    plt.xlim(0, 5000)

    return data_nmfX, nmf_weights, nmf_computed_data


def nmf_sort(data, component):

    data_nmfX, nmf_weights, nmf_computed_data = nmf_calcium(data, component)

    # concatenate NMF data on dataT
    df_nmf = pd.DataFrame(data)
    df_nmf['NMF1'] = nmf_weights[0, :]  # chose which NMF component you want to sort with
    # df_nmf['NMF2'] = nmf_weights[1, :]
    # df_nmf['NMF3'] = nmf_weights[2, :]
    # df_nmf.head()

    # sort data wrt NMF
    df_sorted_nmf1 = df_nmf.sort_values(by='NMF1', ascending=False)
    # df_sorted_nmf2 = df_nmf.sort_values(by='NMF2', ascending=False)
    # df_sorted_nmf3 = df_nmf.sort_values(by='NMF3', ascending=False)
    # print(df_sorted_cnmf1)
    sorted_nmf1 = df_sorted_nmf1.iloc[:, :-4].to_numpy()
    # sorted_nmf2 = df_sorted_nmf2.iloc[:, :-4].to_numpy()
    # sorted_nmf3 = df_sorted_nmf3.iloc[:, :-4].to_numpy()

    return


def nmf_varexpl(data):

    time = len(data)
    data = gaussian_filter1d(data, sigma=20)  # smooth
    data = (data - np.nanmean(data)) / np.nanstd(data)  # whiten

    data_train = data[:, int(time * 0.2):]
    data_test = data[:, :int(time * 0.2)]

    # fit the data using training set, find MSEs using test set

    nmf_var_mse = []
    nmf_var_r2 = []

    for n in range(1, 51):
        # fit nmf with component no = n
        nmf = NMF(n)
        nmf_train = nmf.fit(data_train.T)
        nmf_test = nmf.transform(data_test.T)

        # compute predicted matrix calculated from nmf with the assigned component number
        nmf_train_weights = nmf_train.components_
        nmf_train_weights = nmf_train_weights.T
        nmf_computed_data = nmf_train_weights @ nmf_test.T

        # find the mean square error and r squared between original and computed matrices
        nmf_mse = mean_squared_error(data_test, nmf_computed_data)
        nmf_r2 = r2_score(data_test, nmf_computed_data)
        print("R^2 for NMF", str(n), ":", str(nmf_r2))

        # append the mean square error and r squared for each ic in a separate matrix
        nmf_var_mse.append(nmf_mse)
        nmf_var_r2.append(nmf_r2)

    # # plot MSE and R squared
    # ax = plt.subplot(1,3,1)
    # plt.plot(nmf_var_mse)
    # ax.set(xlabel = 'NMF', ylabel = 'MSE');

    # # plot R squared
    # ax = plt.subplot(1,3,2)
    # plt.plot(nmf_var_r2)
    # ax.set(xlabel = 'NMF', ylabel = 'R squared');

    # plot change in R squared
    ax = plt.subplot(1, 3, 3)
    nmf_var_r2 = np.array(nmf_var_r2)
    plt.plot((nmf_var_r2[1:] - nmf_var_r2[:-1]))
    plt.xlabel('NMF')
    plt.ylabel('Change in R squared');

    return