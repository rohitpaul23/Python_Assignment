


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}



def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    import re
    df = pd.read_csv('university_towns.txt', sep='\n', header=None, squeeze=True)
    country = ''
    new_df = pd.DataFrame(columns=["State", "RegionName"])
    #print(new_df)
    for row in df:
        if re.search('.*\[edit\]', row):
            state = row[:-6]
        else:    
            row = re.sub(' \(.*','',row)
            row = re.sub('\[.*\]','',row)
            new_df = new_df.append({'State': state, 'RegionName': row}, ignore_index=True)
            #print(country, row)
    #print(new_df)        
    return new_df
#get_list_of_university_towns()



def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', skiprows=8, header=None)
    df = df[[4,5,6]]
    result = df.isin(['2000q1'])
    rows = result[4][result[4] == True].index
    #print(rows[0])
    i = rows[0]
    while i < df.size/3 - 3:
        if df.iloc[i-1][6] > df.iloc[i][6]:
            
            if df.iloc[i][6] > df.iloc[i+1][6]:
                j = i+1
                while True:
                    if df.iloc[j][6] > df.iloc[j+1][6]:
                        j = j + 1
                    else:
                        break
                if df.iloc[j][6] < df.iloc[j+1][6]:
                    if df.iloc[j+1][6] < df.iloc[j+2][6]:
                        #print(df.iloc[i][4])
                        #i = j+3
                        return df.iloc[i][4]
        
        i = i + 1
#get_recession_start()



def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', skiprows=8, header=None)
    df = df[[4,5,6]]
    result = df.isin(['2000q1'])
    rows = result[4][result[4] == True].index
    #print(rows[0])
    i = rows[0]
    while i < df.size/3 - 3:
        if df.iloc[i-1][6] > df.iloc[i][6]:
            
            if df.iloc[i][6] > df.iloc[i+1][6]:
                j = i+1
                while True:
                    if df.iloc[j][6] > df.iloc[j+1][6]:
                        j = j + 1
                    else:
                        break
                if df.iloc[j][6] < df.iloc[j+1][6]:
                    if df.iloc[j+1][6] < df.iloc[j+2][6]:
                        #print(df.iloc[i][4])
                        #i = j+3
                        return df.iloc[j+2][4]
        
        i = i + 1
#get_recession_start()



def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', skiprows=8, header=None)
    df = df[[4,5,6]]
    result = df.isin(['2000q1'])
    rows = result[4][result[4] == True].index
    #print(rows[0])
    i = rows[0]
    while i < df.size/3 - 3:
        if df.iloc[i-1][6] > df.iloc[i][6]:
            
            if df.iloc[i][6] > df.iloc[i+1][6]:
                j = i+1
                while True:
                    if df.iloc[j][6] > df.iloc[j+1][6]:
                        j = j + 1
                    else:
                        break
                if df.iloc[j][6] < df.iloc[j+1][6]:
                    if df.iloc[j+1][6] < df.iloc[j+2][6]:
                        #print(df.iloc[i][4])
                        #i = j+3
                        return df.iloc[j][4]
        
        i = i + 1
#get_recession_start()



def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df = df.set_index(["State","RegionName"])
    df = df.drop(['RegionID', 'Metro', 'CountyName', 'SizeRank'], axis=1)
    row = ['1996-04', '1996-05']
    #moddf = df.apply(lambda x: np.mean(x[row]), axis=1)
    for col in df.columns:
        if pd.Timestamp(col) < pd.Timestamp('2000-01'):
            df = df.drop(col, axis=1)
    
    for col in df.columns:
        if pd.Timestamp(col).month < 4:
            newcol = str(pd.Timestamp(col).year)+'q1'
            df.rename(columns={col:newcol}, inplace=True)
        elif  3 < pd.Timestamp(col).month < 7:
            newcol = str(pd.Timestamp(col).year)+'q2'
            df.rename(columns={col:newcol}, inplace=True)
        elif  6 < pd.Timestamp(col).month < 10:
            newcol = str(pd.Timestamp(col).year)+'q3'
            df.rename(columns={col:newcol}, inplace=True)
        else:
            newcol = str(pd.Timestamp(col).year)+'q4'
            df.rename(columns={col:newcol}, inplace=True)
    df = df.groupby(by=df.columns, axis=1).mean()    
    df = df.reset_index()
    df['State'] = df['State'].map(states)
    
    df = df.set_index(["State","RegionName"])
    return df
#convert_housing_data_to_quarters().iloc[:10,[0,1,-2,-1]]



def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    from scipy import stats
    
    uni_town = get_list_of_university_towns()
    rec_start = get_recession_start()
    rec_bottom = get_recession_bottom()
    df = convert_housing_data_to_quarters()
    
    if rec_start[-2:] == 'q1':
        bef_rec_start = str(int(rec_start[:-2])-1) + 'q4'
    elif rec_start[-2:] == 'q2':
        bef_rec_start = rec_start[:-2] + 'q1'
    elif rec_start[-2:] == 'q3':
        bef_rec_start = rec_start[:-2] + 'q2'
    elif rec_start[-2:] == 'q4':
        bef_rec_start = rec_start[:-2] + 'q3'    
    
    df['house_ratio'] = df[bef_rec_start].div(df[rec_bottom])
    
    #uni_town_list = uni_town.to_records(index=False).tolist()
    #group1 = df.loc[uni_town_list]
    #group2 = df.loc[~df.index.isin(uni_town_list)]
    
    new_df = pd.merge(df.reset_index(),
                     uni_town,
                     on=uni_town.columns.tolist(),
                     indicator='_flag', how='outer')
    group1 = new_df[new_df['_flag']=='both']
    group2 = new_df[new_df['_flag']!='both']
    
    group1_mean =group1['house_ratio'].mean()
    group2_mean =group2['house_ratio'].mean()
    
    #stat = stats.ttest_ind(group1.dropna()['house_ratio'], group2.dropna()['house_ratio'])
    #stat = stats.ttest_ind(group1['house_ratio'], group2['house_ratio'])
    stat = stats.ttest_ind(group1['house_ratio'], group2['house_ratio'], nan_policy='omit')
    p = stat[1]
    
    if p < 0.01:
        different = True
    else:
        different = False
    better = ''
    if group1_mean > group2_mean:
        better = "non-university town"
    else:
        better = "university town"
        #different, p, better
    return different, p, better
run_ttest()



