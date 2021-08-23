import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

def vectorization(df, columns):
    column_name = columns[0]
    
    # Checking if the column name has been removed already
    if column_name not in ['Drinking', 'Smoking', 'Gender']:
        return df
    
    if column_name in ['Drinking','Smoking', 'Gender']:
        df[column_name.lower()] = pd.Categorical(df[column_name])
        df[column_name.lower()] = df[column_name.lower()].cat.codes
        
        df = df.drop(column_name, 1)
        
        return vectorization(df, df.columns)
    
    else:
        new_df=df.drop(column_name, axis = 1).join(df[column_name].str.join('|').str.get_dummies(),lsuffix='_left', rsuffix='_right')
        return vectorization(new_df, new_df.columns)

def PredCluster(user_data):
    new_cluster= vectorization(user_data, user_data.columns)
    new_cluster.columns=new_cluster.columns.str.lower()
    new_cluster= pd.DataFrame(scaler.fit_transform(new_cluster), index=new_cluster.index, columns=new_cluster.columns)

    model = joblib.load(r"API_mini_model.joblib")

    cluster_label = model.predict(new_cluster)
    df = pd.DataFrame(cluster_label,
            columns=['cluster'])

    df['ID'] = pd.Series(user_data['Gender'])
    
    return df