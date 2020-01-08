import pandas as pd
import numpy as np
import math
from tqdm import tqdm

def BulkCorrection(ts, w, tstd):
    """
    Takes a Pandas series and returns a timeseries without anomaly
    (using the average +/- tstd * standard deviation). The algorithm
    is based on evaluating if the `qty` value is outside the moving
    average value +/- a few standard deviations.
    
    `w` defines the width of the rolling window
    `tstd` defines the number of standard deviations around the average
    """

    df_ts = ts.to_frame(name='qty')
    df_ts['mean'] = df_ts['qty'].rolling(window=w, center=True).mean()
    df_ts['std'] = df_ts['qty'].rolling(window=w, center=True).std()
    df_ts['corr_qty'] = np.where((df_ts['mean'] - tstd*df_ts['std'] > df_ts['qty']) \
                               | (df_ts['qty'] > df_ts['mean'] + tstd*df_ts['std']),df_ts['mean'],df_ts['qty'])
    
    shift = math.floor(w/2)
    return df_ts.iloc[shift:-shift]
    
def maxslopeDetection(ts):
    """
    Function to detect raw maximum and minimum slope in a timeseries ts
    """
    assert type(ts) != str

    n = len(ts)
    sl = ts[1:].values - ts[:-1].values
    
    return max(sl)

def seasonality(ts,slen,prop=0.75):
    df = pd.DataFrame(ts[-slen:])
    s = df.iloc[:,0].sum()
    if s == 0:
        return 0
    else:
        for i in range(slen):
            df[i]=np.roll(df.iloc[:,0],i).cumsum()/s
        return min((slen-(df>0.75).sum())[1:])+1
    
def dataPrep(df_data):
    """
    Formatting dataframe to handle features building, getting the raw data
    to standard timeseries.
    
    Input :
    * df_data : pandas dataframe resulting from make_dataset.makeDataset()
    
    Output :
    * df_data_wk_c : pandas dataframe timeseries (articles in column)
    """
    
    # Converting the `date` field to datetime format for DF handling
    df_data['date'] = pd.to_datetime(df_data['date'])
    # Putting the articles as columns
    df_data = df_data.pivot(index='date', columns='article', values='qty')
    # Setting up date frequency
    df_data = df_data.asfreq('W')
    # Filling up NA values as 0
    df_data = df_data.fillna(0)
    # Resampling dataset to weekly and aggregating with summation
    df_data_wk = df_data[df_data.columns].resample('W').sum()
    
    ############################################################################
    ###### Getting rid of anomaly values (based on the BulkOrders logic) #######
    ############################################################################
    # Final dataset for algorithm input will be based on a copy of original dataset
    df_data_wk_c = df_data_wk.copy()
    # Applying the BulkOrders-like algorithm to the dataset
    w = 5 # rolling window used in the algorithm
    tstd = 3  # number of standard deviations lag from average to detect anomaly
    for i in tqdm(df_data_wk_c.columns):
        df_data_wk_c[i] = BulkCorrection(df_data_wk[i], w ,tstd)
    # The consequence of using the moving average method is losing a few values
    # right of left of the dataset. These values must be getting rid of before 
    # feeding the algorithm.
    shift = math.floor(w/2)
    df_data_wk_c = df_data_wk_c.iloc[shift:-shift]
    
    return df_data_wk_c