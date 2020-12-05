import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr

sns.set()

emissions_data = pd.read_csv("C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\GDC "
                             "projects\\Greenhouse Gases\\emission_data\\co2-mm-mlo_csv.csv")

temp_data = pd.read_csv("C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\GDC "
                        "projects\\Greenhouse Gases\\global-temp_zip\\data\\monthly_csv.csv")


# A function that creates a new column for year from the date column.
def get_year(df, date_col):
    df[date_col] = pd.to_datetime(df[date_col], format='%Y-%m-%d')
    df['Year'] = pd.DatetimeIndex(df[date_col]).year
    return df


# Getting a separate year column for both data sets.
emissions_data = get_year(emissions_data, 'Date')
temp_data = get_year(temp_data, 'Date')

# """ Question to answer: has the temperature risen according to both sources (GCAG) and (GISTEMP)? """
# gcag_1 = temp_data[temp_data['Source'] == 'gcag']
# gistemp_1 = temp_data[temp_data['Source'] == 'gistemp']
#
# plt.plot(gcag_1['Year'], gcag_1['Mean'])
# plt.plot(gistemp_1['Year'], gistemp_1['Mean'])
# plt.show()

# Getting the data for temperature from 1958 onwards only and invalid average emissions data.
temp_data = temp_data[temp_data['Year'] >= 1958]
emissions_data = emissions_data[emissions_data['Average'] != -99.99]
# Only keeping the required columns for the emissions data.
emissions_data = emissions_data[['Date', 'Average', 'Year']]

# Separating out the two different sources for temperature measures.
gcag = temp_data.loc[temp_data['Source'] == 'GCAG'].copy(deep=True)
gistemp = temp_data.loc[temp_data['Source'] == 'GISTEMP'].copy(deep=True)
gcag['gcag_mean'] = gcag['Mean']
gistemp['gistemp_mean'] = gistemp['Mean']
gcag = gcag.drop(labels=['Mean'], axis=1)
gistemp = gistemp.drop(labels=['Mean'], axis=1)

# Group by the year and take the average measures for temp and emissions for that year.
emissions_year = emissions_data.groupby(by='Year').mean()
gcag_year = gcag.groupby(by='Year').mean()
gistemp_year = gistemp.groupby(by='Year').mean()
# merging the three datasets by year.
output_data = pd.merge(emissions_year, gcag_year, how="inner", on='Year')
output_data = pd.merge(output_data, gistemp_year, how="inner", on='Year')

fig2, (ax1, ax2) = plt.subplots(2, 1)
ax1.scatter(output_data['Average'], output_data['gcag_mean'], color='blue')
ax1.set_xlabel('CO2 emissions (mole fraction)')
ax1.set_ylabel('Temperature change (Celsius)') # against base 20th century average
ax1.set_title("GCAG Data on Average Temperature change vs Average CO2 Emissions from 1958-2016")
# generating equation for best fit (straight line).
m, b = np.polyfit(output_data['Average'],output_data['gcag_mean'], 1)
ax1.plot(output_data['Average'], m*output_data['Average'] + b)

# fig3, (ax2) = plt.subplots(1, 1)
ax2.scatter(output_data['Average'], output_data['gistemp_mean'], color='purple')
ax2.set_xlabel('CO2 emissions (mole fraction)')
ax2.set_ylabel('Temperature change (Celsius)') #against base period average 1951-1980
ax2.set_title("GISTEMP Data on Average Temperature change vs Average CO2 Emissions from 1958-2016")
m2, b2 = np.polyfit(output_data['Average'], output_data['gistemp_mean'], 1)
ax2.plot(output_data['Average'], m2*output_data['Average'] + b2)


# fig2, (ax1) = plt.subplots(1, 1)
# ax1.scatter(output_data['Average'], output_data['gcag_mean'], color='blue')
# ax1.set_xlabel('CO2 emissions (mole fraction)')
# ax1.set_ylabel('Change in temperature (degrees Celsius) against 20th century average')
# ax1.set_title("GCAG Data on Average Temperature change vs Average CO2 Emissions from 1958-2016")
# # generating equation for best fit (straight line).
# m, b = np.polyfit(output_data['Average'],output_data['gcag_mean'], 1)
# ax1.plot(output_data['Average'], m*output_data['Average'] + b)

years = [y for y in output_data.index]
for i, year in enumerate(years):
    if i % 8 == 0:
        ax1.text(output_data['Average'].iloc[i], output_data['gcag_mean'].iloc[i], str(year),
                 horizontalalignment='right')
        ax2.text(output_data['Average'].iloc[i], output_data['gistemp_mean'].iloc[i], str(year),
                 horizontalalignment='right')
print(pearsonr(output_data['Average'], output_data['gcag_mean']))
plt.tight_layout()
plt.show()




