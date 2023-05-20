
import streamlit as st
import pandas as pd
from datetime import datetime


# read the raw data from .csv file, and cache the raw data for improved performance
@st.cache_data
def rawSDGData() -> pd.DataFrame:
    return pd.read_csv('../../../../../dropped_articles.tsv',sep='\t')

# Melt the dataset according to the sdgs column
def melt_sdgs(dfs: pd.DataFrame) -> pd.DataFrame:    
    # dropping null values of sdgs because the threshold of all the seven SDG's columns are less than 0.95
    # dfs = dfs.dropna(axis=0, subset=['sdgs'])
    # st.write(dfs.head(50))

    # Explode the sdgs column
    dfs = dfs.explode('sdgs').reset_index(drop=True)

    # Split the sdgs values into separate columns
    fn = dfs['sdgs'].str.split(',', expand=True).add_prefix('sdgs')

    # Concatenate the sdgs columns (fn) to the original dfs DataFrame
    new_dfs = pd.concat([dfs,fn],axis=1).drop('sdgs', axis=1)
    dfs_columns = new_dfs.columns[0:10]
    # st.write(dfs_columns)
    # Melt the DataFrame to convert the SDG columns to a single column
    new_dfs = new_dfs.melt(id_vars=dfs_columns, value_vars=['sdgs0', 'sdgs1', 'sdgs2'], value_name='sdg')

    # Drop the variable column and rows with missing SDGs
    new_dfs.drop(['variable'], axis=1, inplace=True)
    new_dfs.dropna(subset=['sdg'], inplace=True)

    # convert the 'sdg' column to categorical type
    new_dfs['sdg'] = new_dfs['sdg'].astype('category')
    return new_dfs

# pre-process the dataset by removing NaN values and unused columns 
@st.cache_data
def processData() -> pd.DataFrame:
    df = rawSDGData()
    proc_data = df.drop(['issn', 'doi', 'topics', 'topic', 'topic_prob', 'targets', 'slug_handle', 'repo', 'repo_url'], axis=1)
    proc_data.dropna(subset=['title', 'sdgs'], axis=0, inplace=True)
    proc_data['type'] = proc_data['type'].replace(['journalarticles'], 'journalarticle')
    proc_data['date'] = pd.to_datetime(proc_data['date'])
    proc_data['year'] = proc_data['date'].dt.year
    proc_data = pd.concat((proc_data.iloc[:, 0:10], proc_data['year']), axis=1)
    # st.write(proc_data.head(50))
    # st.write(proc_data["year"].dtype)

    # *** CALL THE MELT_SDGS FUNCTION ***
    final_data = melt_sdgs(proc_data)
    return final_data
