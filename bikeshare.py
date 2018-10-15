import time
import pandas as pd
import numpy as np
import math
from datetime import datetime
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filter_city():
    '''Asks user to specify a city
    Returns:(str) city - name of the city to analyze
    '''
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n''Would you like to see data for Chicago, New York, or'' Washington?\n')
        if city.lower() == 'chicago':
            return 'chicago.csv'
        elif city.lower() == 'new york':
            return 'new_york_city.csv'
        elif city.lower() == 'washington':
            return 'washington.csv'
        else:
            print('Sorry, I do not understand your input. Please input either ''Chicago, New York, or Washington.')
def get_time_period():
    time_period = ''
    while time_period.lower() not in ['month', 'day', 'none']:
        time_period = input('\nWould you like to filter the data by month, day,'' or not at all? Type "none" for no time filter.\n')
        if time_period.lower() not in ['month', 'day', 'none']:
            print('Sorry, I do not understand your input.')
    return time_period
def get_filters_month():
    '''Asks user to specify a month
    Returns:(str) month - name of the month to filter by, or "all" to apply no month filter
    '''
    month_input = ''
    months_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,'may': 5, 'june': 6}
    while month_input.lower() not in months_dict.keys():
        month_input = input('\nWhich month? January, February, March, April,'' May, or June?\n')
        if month_input.lower() not in months_dict.keys():
            print('Sorry, I do not understand your input. Please type in a ''month between January and June')
    month = months_dict[month_input.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))
def get_filters_day():
    '''Asks user to specify a day
    Returns:(str) day - name of the day of week to filter by, or "all" to apply no day filter
    '''
    particular_month = get_filters_month()[0]
    month = int(particular_month[5:])
    valid_date = False
    while valid_date == False:
        is_int = False
        day = input('\nWhich day? Please type your response as an integer.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('invalid response. Please type your'' response as an integer.')
                day = input('\nWhich day? Please type your response as an integer.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))
def popular_month(df):
    '''display the most common month
    '''
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    pop_month = months[index - 1]
    print('The most popular month is {}.'.format(pop_month))
def popular_day(df):
    '''display the most common day of week
    '''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
    indexno = int(df['start_time'].dt.dayofweek.mode())
    pop_day = days_of_week[indexno]
    print('The most popular day of week for start time is {}.'.format(pop_day))
def popular_hour(df):
    '''display the most common start hour
    '''
    pop_hour = int(df['start_time'].dt.hour.mode())
    if pop_hour == 0:
       am_pm = 'am'
       pop_hour1 = 12
    elif 1 <= pop_hour < 13:
        am_pm = 'am'
        pop_hour1 = pop_hour
    elif 13 <= pop_hour < 24:
        am_pm = 'pm'
        pop_hour1 = pop_hour - 12
    print('The most popular hour of day for start time is {}{}.'.format(pop_hour1, am_pm))
def trip_duration(df):
    """Displays statistics on the total and average trip duration."""
    total_duration = df['trip_duration'].sum()
    mins, sec = divmod(total_duration, 60)
    hour, mins = divmod(mins, 60)
    print('The total trip duration is {} hours, {} minutes and {}'' seconds.'.format(hour, mins, sec))
    average_duration = round(df['trip_duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hour, mins = divmod(mins, 60)
        print('The average trip duration is {} hours, {} minutes and {}'' seconds.'.format(hour, mins, sec))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(mins, sec))
def popular_stations(df):
    """Displays statistics on the most popular stations and trip."""
    # TO DO: display most commonly used start station
    # TO DO: display most commonly used end station
    start_sta = df['start_station'].mode().to_string(index = False)
    end_sta = df['end_station'].mode().to_string(index = False)
    print('The most popular start station is {}.'.format(start_sta))
    print('The most popular end station is {}.'.format(end_sta))
    # TO DO: display most frequent combination of start station and end station trip
    pop_trip = df['journey'].mode().to_string(index = False)
    print('The most popular trip is {}.'.format(pop_trip))
def users(df):
    """Displays statistics on bikeshare users."""
    # TO DO: Display counts of user types
    print('\nCalculating User Stats...\n')
    subsriber = df.query('user_type == "Subscriber"').user_type.count()
    customer = df.query('user_type == "Customer"').user_type.count()
    print('There are {} Subscribers and {} Customers.'.format(subsriber, customer))

def display_data(df):
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        # prints every column except the 'journey' column created in statistics()
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = is_valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break
def birth_years(df):
    earliest = int(df['birth_year'].min())
    recent = int(df['birth_year'].max())
    pop = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe youngest users are born in {}.''\nThe most popular birth year is {}.'.format(earliest, recent, pop))
def load_data():
    '''Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
        dff - Pandas DataFrame containing city data filtered by month and day
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_filter_city()
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])
    dff=df
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels
    pd.set_option('max_colwidth', 100)
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')
    time_period = get_time_period()
    if time_period == 'none':
        dff = df
    elif time_period == 'month' or time_period == 'day':
        if time_period == 'month':
            filter_lower, filter_upper = get_filters_month()
        elif time_period == 'day':
            filter_lower, filter_upper = get_filters_day()
        dff = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    if time_period == 'none':
        start_time = time.time()
        popular_month(dff)
        print("That took %s seconds." % (time.time() - start_time))
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        popular_day(dff)
        print("That took %s seconds." % (time.time() - start_time))
        start_time = time.time()
    popular_hour(dff)
    start_time = time.time()
    print("That took %s seconds." % (time.time() - start_time))
    trip_duration(dff)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()
    # What is the most popular start station and most popular end station?
    popular_stations(dff)
    print("That took %s seconds." % (time.time() - start_time))
    start_time = time.time()
    print("That took %s seconds." % (time.time() - start_time))
    start_time = time.time()
    users(dff)
    print("That took %s seconds." % (time.time() - start_time))
    display_data(dff)
    if city == 'chicago.csv' or city == 'new_york_city.csv' :
        print("\nCalculating the next statistic...")
        start_time = time.time()
        print("That took %s seconds." % (time.time() - start_time))
        start_time = time.time()
        birth_years(dff)
        print("That took %s seconds." % (time.time() - start_time))
        # TO DO: Display counts of gender
        male = df.query('gender == "Male"').gender.count()
        female = df.query('gender == "Female"').gender.count()
        print('There are {} male users and {} female users.'.format(male, female))

def main():
    while True:
        load_data()
if __name__ == "__main__":
	main()
