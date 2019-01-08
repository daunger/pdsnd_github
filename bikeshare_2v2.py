# import pandas, numpy, and time module
import time
import pandas as pd
import numpy as np

#load data files into dictionary of panda series called CITY_DATA
CITY_DATA = { 'chicago': 'c://Udacity/Project_2/chicago.csv',
          'new york city': 'c://Udacity/Project_2/new_york_city.csv',
          'washington': 'c://Udacity/Project_2/washington.csv' }

def get_city():
    """
    Asks user to specify a city to start the analysis.

    Args:

        none

    Returns:
        (str) city - name of the city to analyze

    """
    print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city to analyze; Chicago, New York City or Washington: ')
    city = city.lower()

        # use while loop to handle invalid inputs

    while True:
        if city == 'chicago':
            print("\n You have chosen Chicago\n")
            return 'chicago'
        if city == 'new york city':
            print("\n You have chosen New York City\n")
            return 'new york city'
        elif city == 'washington':
            print("\n You have chosen Washington\n")
            return 'washington'
        else:
            print("\n I don't know what you mean\n")
            city = input('Please re-input city; Chicago, New York City  or Washington: ')
            city = city.lower()
    return city

print('*'*40)

def get_time_period():
    """
    Defines the period (month, day, or no filter) to perform the statistical analysis in
    User decides to filter by month, day, or no filter at all

    Args:
        none
    Returns:
        (str) time filter for the period of statistics to be run on
    """

    # determine whether to filter by month or day of month

    period = input('n\Do you want to filter the data by: "month", "day", or "no" filter? \n')

    period = period.lower()

    while True:
        if period == "month":
            while True:
                day_month = input('\n Do you want to filter the data by day of the month as well? Yes or No\n')
                if day_month == 'no':
                    print('\n Filtering will be by month\n')
                    return 'month'
                elif day_month == 'yes':
                    print('\n The data will be filtered by month and day of month\n')
                    return 'day_of_month'
        if period == "day":
            print('\n The data will be filtered by the day of the week\n')
            return 'day_of_week'
        elif period == "no":
            print('\n No filter for the time period will be applied\n')
            return 'none'
        else:
            print('\n I don\'t know what you mean\n')
            period = input('\n Please enter a filter option, "month", "day"  or "no" filter \n').lower()

# determine what month will be analyzed or if all months will be analyzed

def what_month(m):
    if m =='month':
        month = input('\nEnter in the full month name for analysis [ie.January]\n ')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('I don\'t know what you mean.  Please enter in the full month name [ie. January]')
        return month.strip().lower()
    else:
        return 'none'

# this determines the month and the day of the month if month and day of month was chosen as the filter

def month_day_info(df, month_day):
    month_and_day = []
    if month_day == 'day_of_month':
        month = what_month('month')
        month_and_day.append(month)
        maximum_day_month = max_day_month(df, month)

        while (True):
            q = """\n Which day of the month? \n
            Please type the day of the month as an integer between 1 and """
            q = q + str(maximum_day_month) + '\n'
            month_day = input (q)

            try:    #using try expression to handle exceptions
                month_day = int(month_day)
                if 1 <= month_day <= maximum_day_month:
                    month_and_day.append(month_day)
                    return month_and_day
            except ValueError:
                print('That is not a numeric value')
    else:
        return 'none'

# If filter is for day of week, this function asks for and returns that day

def day_info(d):
    if d == 'day_of_week':
        day = input('\nInput day of week to be analyzed; M, Tu, W, Th, F, Sa, Su:\n')
        while day.lower().strip() not in ['m', 'tu','w', 'th', 'f', 'sa', 'su']:
            day = input('\nI don\'t know what you mean, Please enter in a day; M, Tu, W, Th, F, Sa, Su\n')
        return day.lower().strip()
    else:
        return 'none'

print('-'*40)

# load data for selected City

def load_data(city):
    print('\n Loading city data ..')
    df=pd.read_csv(CITY_DATA[city])

# extracting
# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
# extract month and day of week from Start Time column in csv files to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['day_of_month'] = df['Start Time'].dt.day
    return df

def time_filters(df, time, month, week_day, md):
    """
    Filters the data specified by the user be it, month, day_of_month, or day_of_week
    Variables:
        df          city DataFrame
        time        month, day_of_month, day_of_week
        month       the month specified to filter by
        week_day    the week day used to filter by
        md          a list for the month (index[0]) and day of month (index[1])
    returns:
        df - dataframe to be used for stats and calcs
    """

    # use the index of the months list to get the corresponding int
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week to create the new dataframe
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    #filter by day of month to create the new dataframe
    if time == 'day_of_month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month'] == month]
        day = md[1]
        df = df[df['day_of_month'] == day]

    return df

# get the maximum day of the month

def max_day_month(df, month):
    months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day

# determine the most popular month for bike ride (start time)

def month_freq(df):
    print('\nWhat is the most popular month for biking?')
    m = df.month.mode() [0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m-1].capitalize()
    return popular_month

# determine the most popular day of the week for a bike ride (day_of_week)

def day_freq(df):
    print('\nWhat is the most popular day of the week for a bike ride?')
    return df['day_of_week'].value_counts().reset_index() ['index'] [0]

# determine the most popular hour of the day to start biking

def hour_freq(df):
    print('\nWhat is the most popular hour to start a bike ride?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode() [0]

# determine ride duration both total ride duration from January through to June and the average ride duration

def ride_duration(df):
    print('\nWhat was the total ride duration done in the first half of 2017 and what was the average ride time per trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    # sum for total trip time, mean to get average trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split() [0]
    print('\nThe total travel time in the first half of 2017 was ' + total_days + 'days\n')
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split() [0]
    print('\nThe average travel time in the first half of 2017 was ' + avg_days + 'days\n')
    return total_ride_time, avg_ride_time

# determine the most popular start and finish station

def stations_freq(df):
    print('\nWhat is the most popular station to start a bike trip from?')
    start_station = df['Start Station'].value_counts().reset_index() ['index'] [0]
    print(start_station)
    print('\nWhat is the most popular station to finish a bike trip?')
    end_station = df['End Station'].value_counts().reset_index() ['index'] [0]
    print(end_station)
    return start_station, end_station

# determine what the most common bike trip (route) is

def common_trip(df):
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nWhat was the most popular route from starting point to finish point?')
    return result

# determine the counts of each user type; subscribers, customers, or others

def user_type(df):
    print('\nCounts of user types; subscribers, customers, or other')
    return df['User Type'].value_counts()

# determine counts of gender

def gender_data(df):
    try:
        print('\nBreakdown of user gender types \n ')
        return df['Gender'].value_counts()
    except:
        print('\nThere is no gender information in this dataset')

# determine birth years information: earliest, most recent, and most common

def birth_years(df):
    try:
        print('\nWhat is the earliest, latest, and most frequent birth years?')
        earliest = np.min(df['Birth Year'])
        latest = np.max(df['Birth Year'])
        most_frequent = df['Birth Year'].mode() [0]
        print('\nEarliest: ' + str(earliest) + ', latest: ' + str(latest) + ', most frequest :' +str(most_frequent))
        return earliest, latest, most_frequent
    except:
        print('There is no available birth information in this dataset')

# calculate the time it takes to perform a particular analysis

def process(f, df):
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print('Computing this stat took %s seconds.' % (time.time() - start_time))

# display the data used to compute all the stats

def disp_raw_data(df):
    #drop out unnecessary columns to tighten up display
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0
    see_data = input("\nDo you want to see rows of the data used in the statistics calculations? Input 'yes' or 'no\n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\nWould you like to see 5 more rows of data? 'yes' or 'no' ").lower()


def main():
    """
    The main function is what calls and calculates the requested filter information
    """

    while True:
        city = get_city()
        df = load_data(city)
        period = get_time_period()
        month = what_month(period)
        day = day_info(period)
        month_and_day = month_day_info(df, period)

        df = time_filters(df, period, month, day, month_and_day)
        disp_raw_data(df)

        # blurt out all the stats

        stats_funcs_list = [month_freq, day_freq, hour_freq, ride_duration, common_trip, stations_freq, user_type, birth_years, gender_data]

        # print out calculation time for each function

        for x in stats_funcs_list:
            process(x, df)


        restart = input("\n Would you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
