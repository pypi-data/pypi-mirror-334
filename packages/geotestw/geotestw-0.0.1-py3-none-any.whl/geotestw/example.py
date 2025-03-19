import wenhuitest
from geoevo import GeoEvoOptimizer
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import random
from sklearn.model_selection import train_test_split
import warnings
import time
warnings.filterwarnings("ignore")

def objfunc(zone_data, zone_val, param):
    feature_name = ['landusenum', 'Main_soil', 'Slope', 'gS', 'mS', 'fS', 'gU', 'mU', 'fU', 'Sand', 'Silt',
                    'Clay', 'pH_H2O', 'EC_H2O', 'TC', 'TOC', 'TN', 'FSS', 'Water_cont', 'Stone_dens', 'BD_bulk',
                    'Rock_fragm']
    var_name = ['CS_0_30']
    model = RandomForestRegressor(n_estimators=int(np.ceil(param[0])), max_features=int(np.ceil(param[1])), oob_score=False)
    model.fit(zone_data[feature_name], zone_data[var_name])
    p = model.predict(zone_val[feature_name])
    r2 = r2_score(zone_val[var_name], p)
    return r2

if __name__ == '__main__': 
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    start_time = time.time()
    ## load data
    train_df = pd.read_csv('/Users/wenhuizhang/1-research/code/AutoML/pypi/geoevo/src/wenhuitest/train_soc.csv')
    train_df, val_df = train_test_split(train_df, test_size=0.3, random_state=seed)
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    train_df.rename(columns={'County': 'zone'}, inplace = True)
    val_df.rename(columns={'County': 'zone'}, inplace = True)
    test_df = pd.read_csv('/Users/wenhuizhang/1-research/code/AutoML/pypi/geoevo/src/wenhuitest/test_soc.csv')
    train_x = train_df[['landusenum', 'Main_soil', 'Slope', 'gS', 'mS', 'fS', 'gU', 'mU', 'fU', 'Sand','Silt',
                        'Clay', 'pH_H2O', 'EC_H2O', 'TC', 'TOC', 'TN', 'FSS', 'Water_cont', 'Stone_dens', 'BD_bulk',
                        'Rock_fragm']]
    test_x = test_df[['landusenum', 'Main_soil', 'Slope', 'gS', 'mS', 'fS', 'gU', 'mU', 'fU', 'Sand','Silt',
                    'Clay', 'pH_H2O', 'EC_H2O', 'TC', 'TOC', 'TN', 'FSS', 'Water_cont', 'Stone_dens', 'BD_bulk',
                    'Rock_fragm']]
    val_x = val_df[['landusenum', 'Main_soil', 'Slope', 'gS', 'mS', 'fS', 'gU', 'mU', 'fU', 'Sand','Silt',
                    'Clay', 'pH_H2O', 'EC_H2O', 'TC', 'TOC', 'TN', 'FSS', 'Water_cont', 'Stone_dens', 'BD_bulk',
                    'Rock_fragm']]
    factor_name = ['Main_soil', 'Slope']
    train_x['Main_soil'] = pd.factorize(train_x['Main_soil'])[0]
    train_x['Slope'] = pd.factorize(train_x['Slope'])[0]
    test_x['Main_soil'] = pd.factorize(test_x['Main_soil'])[0]
    test_x['Slope'] = pd.factorize(test_x['Slope'])[0]
    train_df['Slope'] = pd.factorize(train_df['Slope'])[0]
    train_df['Main_soil'] = pd.factorize(train_df['Main_soil'])[0]
    val_df['Main_soil'] = pd.factorize(val_df['Main_soil'])[0]
    val_df['Slope'] = pd.factorize(val_df['Slope'])[0]
    train_y = train_df['CS_0_30']
    test_y = test_df['CS_0_30']
    feature_name = ['landusenum', 'Main_soil', 'Slope', 'gS', 'mS', 'fS', 'gU', 'mU', 'fU', 'Sand', 'Silt',
                    'Clay', 'pH_H2O', 'EC_H2O', 'TC', 'TOC', 'TN', 'FSS', 'Water_cont', 'Stone_dens', 'BD_bulk',
                    'Rock_fragm']
    var_name = ['CS_0_30']
    train_x.fillna(train_x.mean(), inplace=True)
    train_x[factor_name] = train_x[factor_name].apply(lambda x:np.round(x).astype(int))
    zoneslist = train_df['zone'].unique()
    adjmat = pd.read_csv('/Users/wenhuizhang/1-research/code/AutoML/pypi/geoevo/src/wenhuitest/adj_soc.csv', index_col=0)
    ## start optimization
    print('begin init')
    ## problem definition
    bounds = [(100,500),
            (1,train_x.shape[1])]
    dim = len(bounds)

    ## DE parameters
    mut = 0.8
    crossp = 1/dim
    popsize = 5
    its = 2

    optimizer = GeoEvoOptimizer(popsize, its, dim, objfunc, 1, zoneslist, adjmat, True)
    best_param, best_obj = optimizer.optimize(bounds, train_df, val_df)
    print(f'The best hyperparameter is\n {best_param}\n with objective value\n {best_obj}')

    

