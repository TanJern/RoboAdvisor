import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import pickle



#Reading CSV
dataset= pd.read_csv("C:/Users/c2070756/autoassessmenttool/assessment/etfdb.csv")


#Replacing alphabet ratings
alpha_not_accepted=['Liquidity_Rating','Expenses_Rating','Volatility_Rating','Dividend_Rating']
for column in alpha_not_accepted:
    dataset[column]= dataset[column].replace('A+',0)
    dataset[column]= dataset[column].replace('A',1)
    dataset[column]= dataset[column].replace('A-',1)
    dataset[column]= dataset[column].replace('B+',2)
    dataset[column]= dataset[column].replace('B',2)
    dataset[column]= dataset[column].replace('B-',3)
    dataset[column]= dataset[column].replace('C+',3)
    dataset[column]= dataset[column].replace('C',3)
    dataset[column]= dataset[column].replace('C-',3)
    dataset[column]=dataset[column].replace(np.NaN,2)


#code below are adapted from this page:
#https://gist.github.com/Tahsin-Mayeesha/81dcdafc61b774768b64ba5201e31e0a#file-recommending-anime-with-k-nearest-neighbor-ipynb
asset_features = pd.concat([dataset["Liquidity_Rating"],dataset["Expenses_Rating"],dataset["Volatility_Rating"],dataset["Dividend_Rating"]],axis=1)

#Scaling
scaler = MinMaxScaler()
asset_features=scaler.fit_transform(asset_features)

#Fiting in KNN model
nbrs = NearestNeighbors(n_neighbors=30, algorithm='ball_tree').fit(asset_features)
distances, indices = nbrs.kneighbors(asset_features)

print(indices)

pickle.dump(indices,open("model.pkl","wb"))

