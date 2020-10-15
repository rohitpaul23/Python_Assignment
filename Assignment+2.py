

# # Assignment 2 - Pandas Introduction

# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')


# ### Question 0 (Example)
# 
# What is the first country in df?
#

def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
#

def answer_one():
    return df['Gold'].idxmax()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 

def answer_two():
    diff = 0
    rindex = ''
    for index, value in df.iterrows():
        cdiff = value['Gold'] - value['Gold.1']
        if cdiff > diff:
            diff = cdiff
            rindex = index
    return rindex    


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 

def answer_three():
    diff = 0
    rindex = ''
    for index, value in df.iterrows():
        if value['Gold'] > 0 and value['Gold.1'] > 0:
            cdiff = (value['Gold'] - value['Gold.1'])/value['Gold.2']
            if cdiff > diff:
                diff = cdiff
                rindex = index
    return rindex


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 

def answer_four():
    points_list = []
    for index, rows in df.iterrows():
        pts = rows['Gold.2'] * 3 + rows['Silver.2'] * 2 + rows['Bronze.2']
        points_list.append(pts)
    Points = pd.Series(points_list, index = df.index)
    return Points


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 

census_df = pd.read_csv('census.csv')
census_df.head()


def answer_five():
    dff = census_df.set_index(['STNAME', 'CTYNAME'])
    return dff['COUNTY'].count(level = 'STNAME').idxmax()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 

def answer_six():
    cout_pop = {} 
    dff = census_df.set_index(['STNAME', 'CTYNAME'])
    dff = dff[dff['SUMLEV'] == 50]
    for index in census_df['STNAME'].unique():
        cout_pop[index] = dff['CENSUS2010POP'].loc[index].nlargest(3).sum()
    s = pd.Series(cout_pop)
    return (list(s.nlargest(3).index))
answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 

def answer_seven():
    dff = census_df.set_index('CTYNAME')
    col_to_keep = ['POPESTIMATE2010',
                  'POPESTIMATE2011',
                  'POPESTIMATE2012',
                  'POPESTIMATE2013',
                  'POPESTIMATE2014',
                  'POPESTIMATE2015']
    dff = dff[dff['SUMLEV'] == 50]
    dff = dff[col_to_keep]
    cdf = dff.max(axis = 1) - dff.min(axis = 1)
    return cdf.idxmax()
answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 

def answer_eight(): 
    cdf = census_df[(census_df['REGION'] == 1) | (census_df['REGION'] == 2)]
    cdf = cdf[cdf['POPESTIMATE2015'] > cdf['POPESTIMATE2014']]
    cdf = cdf[['STNAME','CTYNAME']]
    data = []
    indixes = []
    for index,row in cdf.iterrows():
        data_item = []
        if row['CTYNAME'][:10] == 'Washington':
            data_item.append(row['STNAME'])
            data_item.append(row['CTYNAME'])
            data.append(data_item)
            indixes.append(index)
        #cdf = cdf[cdf['CTYNAME'][:10] == 'Washington']
    cdf = pd.DataFrame(data, index = indixes, columns = ['STNAME', 'CTYNAME'])
    return cdf   





