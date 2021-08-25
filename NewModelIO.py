import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

def vectorization(df, columns):

    column_name = columns[0]

    if column_name not in ['Drinking', 'Smoking', 'Gender']:
        return df
    
    if column_name in ['Drinking','Smoking', 'Gender']:
        df[column_name.lower()] = pd.Categorical(df[column_name])
        df[column_name.lower()] = df[column_name.lower()].cat.codes
        
        df = df.drop(column_name, 1)
        
        return vectorization(df, df.columns)
    
    else:
        print('entering else')
        new_df=df.drop(column_name, axis = 1).join(df[column_name].str.join('|').str.get_dummies(),lsuffix='_left', rsuffix='_right')
        return vectorization(new_df, new_df.columns)


# user_data = DataFrame of all users who qualify for the search parameters and now can undergo clustering and ranking based on the main usr we are preparing the list for
# user_data1 = it is the df of main (anchor user) user who we are preparing the list for
# user_data1 must belong inside user_data

#currently  usering first name as UID as it a string format to test parameters, cannot test large scale(more than 8-9 users) because first name is not unique identifier
# dont mind the coimmented code, that will play into effect once a  proper UID and anchoring measure is set

def PredCluster(user_data, user_data1):
    #reference anchor for vectorization to take standard hold
    #not really sure why this doesnt work on single input df

#     data = [{"Drinking":"Drinking Frequently", "Smoking":"Smoking" , "Gender":"male"}]
#     dft = pd.DataFrame(data)
#     user_data = dft.append(user_data)
#     print(user_data)

    new_cluster= vectorization(user_data, user_data.columns)
    new_cluster.columns=new_cluster.columns.str.lower()
    new_cluster= pd.DataFrame(scaler.fit_transform(new_cluster), index=new_cluster.index, columns=new_cluster.columns)

    model = joblib.load(r"API_mini_model.joblib")

    cluster_label = model.predict(new_cluster)
    
    new_cluster['Cluster'] = cluster_label
    
    # new_cluster = new_cluster[new_cluster['Cluster']==designated_cluster[0]].drop('Cluster', 1)
    # des_cluster = des_cluster.append(vect_profile, sort=False)
    
    new_list = new_cluster.T.corr()
    # user_data1 has not been decieded how to be procured
    user_n = user_data1.index[0]
    
    likely_users = new_list[[user_n]].sort_values(by=[user_n],axis=0, ascending=False)[1:4]
    
#     df = pd.DataFrame(cluster_label, 
#             columns=['cluster'])
    
#     df = df.drop(1)
#     df.set_index("First", inplace = True)

#     df['ID'] = pd.Series(user_data.index)
#     df = df.set_index('ID', inplace = True)
#     df = df.drop(['ID'], axis = 1)
    
    return likely_users