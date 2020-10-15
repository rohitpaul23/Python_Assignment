

# # Assignment 3 - More Pandas

# ### Question 1 
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 


def answer_one():
    import pandas as pd
    energy = pd.read_excel('Energy Indicators.xls',
                           na_values='...',
                           keep_default_na=True,
                           usecols=[2,3,4,5],
                           skiprows=17,
                           skipfooter=38,
                           names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace(r" *\(.*\)", "")
    energy.replace(to_replace=["Republic of Korea",
                               "United States of America",
                               "United Kingdom of Great Britain and Northern Ireland", 
                               "China, Hong Kong Special Administrative Region"],
                   value=["South Korea", "United States", "United Kingdom", "Hong Kong"],
                   inplace=True )
    GDP = pd.read_csv('world_bank.csv',
                      header=1,
                      skiprows=3)
    GDP.replace(to_replace=["Korea, Rep.",
                            "Iran, Islamic Rep.",
                            "Hong Kong SAR, China"],
                   value=["South Korea", "Iran", "Hong Kong"],
                   inplace=True )
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    keep_col = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', '2006', '2007', '2008', '2009',
               '2010', '2011', '2012', '2013', '2014', '2015']
    GDP = GDP[keep_col]
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    ScimEn = ScimEn[ScimEn['Rank'] < 16]
    mer1 = pd.merge(ScimEn, GDP, how='inner', left_on='Country', right_on='Country')
    mer2 = pd.merge(mer1, energy, how='inner', left_on='Country', right_on='Country')
    mer2 = mer2.set_index('Country')
    col_needed =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                   'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                   '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    mer2 = mer2[col_needed]
    return mer2
answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')



def answer_two():
    import pandas as pd
    energy = pd.read_excel('Energy Indicators.xls',
                           na_values='...',
                           keep_default_na=True,
                           usecols=[2,3,4,5],
                           skiprows=17,
                           skipfooter=38,
                           names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace(r" *\(.*\)", "")
    energy.replace(to_replace=["Republic of Korea",
                               "United States of America",
                               "United Kingdom of Great Britain and Northern Ireland", 
                               "China, Hong Kong Special Administrative Region"],
                   value=["South Korea", "United States", "United Kingdom", "Hong Kong"],
                   inplace=True )
    GDP = pd.read_csv('world_bank.csv',
                      header=1,
                      skiprows=3)
    GDP.replace(to_replace=["Korea, Rep.",
                            "Iran, Islamic Rep.",
                            "Hong Kong SAR, China"],
                   value=["South Korea", "Iran", "Hong Kong"],
                   inplace=True )
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    keep_col = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', '2006', '2007', '2008', '2009',
               '2010', '2011', '2012', '2013', '2014', '2015']
    GDP = GDP[keep_col]
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    ScimEn = ScimEn[ScimEn['Rank'] < 16]
    innermer1 = pd.merge(ScimEn, GDP, how='inner', left_on='Country', right_on='Country')
    innermer2 = pd.merge(innermer1, energy, how='inner', left_on='Country', right_on='Country')
    innermer2 = innermer2.set_index('Country')
    outermer1 = pd.merge(ScimEn, GDP, how='outer', left_on='Country', right_on='Country')
    outermer2 = pd.merge(outermer1, energy, how='outer', left_on='Country', right_on='Country')
    outermer2 = outermer2.set_index('Country')
    return outermer2.shape[0]-innermer2.shape[0]
#answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 

def answer_three():
    import numpy as np
    Top15 = answer_one()
    rows = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    avgGDP = Top15.apply(lambda x: np.nanmean(x[rows]), axis=1)
    return avgGDP
#answer_three()


# ### Question 4 
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 

def answer_four():
    import numpy as np
    Top15 = answer_one()
    avg15 = answer_three()
    sort15 = np.sort(avg15)[::-1]
    sort5 = avg15[avg15 == sort15[5]]
    data = Top15.loc[str(sort5.index[0])]
    return data['2015']-data['2006']
#answer_four()


# ### Question 5 
# What is the mean `Energy Supply per Capita`?
# 

def answer_five():
    import numpy as np
    Top15 = answer_one()
    
    return np.mean(Top15['Energy Supply per Capita'])
#answer_five()


# ### Question 6 
# What country has the maximum % Renewable and what is the percentage?
# 

def answer_six():
    import numpy as np
    Top15 = answer_one()
    ren = Top15[Top15['% Renewable']==np.max(Top15['% Renewable'])]
    return ren.index[0], np.max(Top15['% Renewable'])
#answer_six()


# ### Question 7 
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 

def answer_seven():
    import numpy as np
    Top15 = answer_one()
    totalcit = np.sum(Top15['Self-citations'])
    maxcit = Top15.apply(lambda x: x['Self-citations']/x['Citations'], axis=1)
    citsort = maxcit.sort_values(ascending=False)
    #totalcit = Top15.apply(lambda x: np.sum(x[rows]), axis=0)
    return citsort.index[0], citsort[0]
answer_seven()


# ### Question 8 
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 

def answer_eight():
    import numpy as np
    Top15 = answer_one()
    pop = Top15.apply(lambda x: x['Energy Supply']/x['Energy Supply per Capita'], axis=1)
    popsort = pop.sort_values(ascending=False)
    return popsort.index[2]
#answer_eight()


# ### Question 9 
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 

def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    cor = Top15.corr(method ='pearson')
    return cor['Energy Supply per Capita']['Citable docs per Capita']
#answer_nine()


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*


def answer_ten():
    Top15 = answer_one()
    med = Top15['% Renewable'].median() 
    HighRenew = Top15.apply(lambda x: 1 if x['% Renewable']>=med else 0, axis=1)
    return HighRenew
#answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*


import numpy as np
def answer_eleven():
    ContinentDict  = ['Asia', 
                      'North America', 
                      'Asia', 
                      'Europe', 
                      'Europe', 
                      'North America', 
                      'Europe', 
                      'Asia',
                      'Europe', 
                      'Asia', 
                      'Europe', 
                      'Europe', 
                      'Asia',
                      'Australia', 
                      'South America']
    
    Top15 = answer_one()
    Top15.insert(1, 'Continent', ContinentDict)
    pop = Top15.apply(lambda x: x['Energy Supply']/x['Energy Supply per Capita'], axis=1)
    Top15['Population'] = pop
    new = (Top15.set_index('Continent').groupby(level=0)['Population']
    .agg({'size': np.size, 'sum': np.sum, 'mean': np.mean, 'std': np.std}))
    return new
#answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 

def answer_twelve():
    Top15 = answer_one()
    return "ANSWER"


# ### Question 13 
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 

def answer_thirteen():
    Top15 = answer_one()
    return "ANSWER"


# Use the built in function `plot_optional()` to see an example visualization.


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")



#plot_optional() 