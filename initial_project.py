import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()

"""##### First question to answer is, has the average CO2 mole fraction gone up across the years? #####"""
# loading the data.
co2_ppm = pd.read_csv('C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\GDC projects\\Greenhouse Gases\\co2-mm-mlo_csv.csv')


# Let us break up the date by year to get averages across year.
co2_ppm['Date'] = pd.to_datetime(co2_ppm['Date'], format='%Y-%m-%d')
co2_ppm['year'] = pd.DatetimeIndex(co2_ppm['Date']).year

"""### Data Cleaning ###"""
# According to '\https://datahub.io/core/co2-ppm', the website where the data is gathered from, missing months are
# assigned the value -99.99. We need to make sure that these values do not skew our analysis.

co2_ppm = co2_ppm[co2_ppm['Average'] != -99.99]
print(co2_ppm)

# Now that we have the year separated out in a different column and gotten rid of ungathered data, we can group the data
# by the year taking the average, for each year. We are only interested in the 'Average' column which has the CO2 mole
# fraction average/month and the year column, since we want to see the trend of CO2 emissions across the years.

yearly_data = co2_ppm[['Average', 'year']].groupby(by=['year']).mean()
X = np.array(yearly_data.index)
Y = yearly_data['Average']

# Now we can visualise the data as a simple line graph.
plt.plot(X, Y)
plt.xlabel('Year')
plt.ylabel('Average CO2 mole fraction')
plt.show()


"""#### The second question we want to ask is what is the trend across year for carbon emission from fuel? ####"""

# We will take the data from 1950's onwards since this is when there is data per capita as well as for other fuels
# collected (likely because the other forms of fuel was not extracted until the mid 20th century).
fuel_data = pd.read_csv('C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\GDC projects\\Greenhouse '
                        'Gases\\co2-fossil-global_zip\\data\\global_csv.csv')

fuel_data = fuel_data[fuel_data['Year'] >= 1950]

# let us plot a stacked area chart to show which types of fuel has been contributing the most to CO2 emissions.
# First we only want to keep year and the different types of fuel for the plot.

X = fuel_data['Year']
Y = [fuel_data['Gas Fuel'], fuel_data['Liquid Fuel'], fuel_data['Solid Fuel'],
     fuel_data['Cement'], fuel_data['Gas Flaring']]
# use a known color palette)
pal = sns.color_palette("Set1")
plt.stackplot(X, Y, labels=['Gas Fuel', 'Liquid Fuel', 'Solid Fuel', 'Cement', 'Gas Flaring'], colors=pal, alpha=0.4)
plt.legend(loc='upper left')
plt.title('CO2 emission by fuel type from 1950-2010')
plt.xlabel('Year')
plt.ylabel('CO2 emission (in million metric tons of C)')
plt.show()

# Let's also see two plots with total CO2 emission over time and per capita over time.

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(fuel_data['Year'], fuel_data['Total'], c='blue')
ax1.set_title('Total CO2 emission from all fuel from 1950-2010')
ax1.set_xlabel('Year')
ax1.set_ylabel('Total CO2 emission (in millions metric tons of C)')

ax2.plot(fuel_data['Year'], fuel_data['Per Capita'], c='purple')
ax2.set_title('CO2 Emission per capita from 1950-2010')
ax2.set_xlabel('Year')
ax2.set_ylabel('Per Capita Emissions (metric tons of carbon)')


plt.show()

"""### Question 3: Which country has the worst fuel emission? ###"""
fuel_nations_data = pd.read_csv('C:\\Users\\sm634\\OneDrive\\Desktop\\Folder\\GDC projects\\Greenhouse '
                                'Gases\\co2-fossil-by-nation_zip\\data\\fossil-fuel-co2-emissions-by-nation_csv.csv')

fuel_nations_data = fuel_nations_data[fuel_nations_data['Year'] >= 1950]
# We will look at which country had the highest amount of emission per capita and total averaged across all years.

agg_nations_total = fuel_nations_data[['Year', 'Country', 'Total']].groupby(by=['Country']).sum()
agg_nations_capita = fuel_nations_data[['Year', 'Country', 'Per Capita']].groupby(by=['Country']).mean()

agg_nations_total = agg_nations_total.sort_values(by=['Total'], ascending=False)
agg_nations_capita = agg_nations_capita.sort_values(by=['Per Capita'], ascending=False)

# Looking at the top and bottom 5 emitters in total and per capita.

top_total_emitters = agg_nations_total.iloc[:5, :]
bottom_total_emitters = agg_nations_total.iloc[-5:, :]

top_capita_emitters = agg_nations_capita.iloc[:5, :]
bottom_capita_emitters = agg_nations_capita.iloc[-5:, :]
bottom_capita_emitters = bottom_capita_emitters.sort_values(by=['Per Capita'], ascending=False)

# The aim is to create the stack of bar charts for the top and bottom five nations in terms of emitters.

fig, ([ax1, ax2]) = plt.subplots(2, 1)
ax1.bar(top_total_emitters.index, top_total_emitters['Total'], color='red')
ax1.set_xlabel('Country')
ax1.set_ylabel('Total Emission (million metric tons of C)')
ax1.set_title('Top 10 CO2 emitters in total from 1950 - 2014')

ax2.bar(bottom_total_emitters.index, bottom_total_emitters['Total'], color='green')
ax2.set_xlabel('Country')
ax2.set_ylabel('Total Emission (metric tons of C)')
ax2.set_title('Bottom 10 CO2 emitters in total from 1950 - 2014')

plt.tight_layout()
plt.show()

fig2, (ax3) = plt.subplots(1, 1)
ax3.barh(top_capita_emitters.index, top_capita_emitters['Per Capita'], color='red')
ax3.set_xlabel('Country')
ax3.set_ylabel('Average Emission (metric tons of C)')
ax3.set_title('Top 10 Per Capita CO2 emitters in average from 1950 - 2014')

# fig3, ax4 = plt.subplots(1, 1)
# ax4.barh(bottom_capita_emitters.index, bottom_capita_emitters['Per Capita'], color='green')
# ax4.set_xlabel('Country')
# ax4.set_ylabel('Average Emission (metric tons of C)')
# ax4.set_title('Bottom 10 Per Capita CO2 emitters in average from 1950 - 2014')

plt.tight_layout()
plt.show()

