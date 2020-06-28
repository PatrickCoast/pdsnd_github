import time
import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.2f}'.format

# dictionary and lists for relevant data for user input
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) period - user preference for time period for slicing data
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # loop to beginning in case user has entered incorrect data, check at end of loop
    while True:
        try:
            # get user input for city
            while True:
                try:
                    city = input("Please enter the city you would like to investigate:\
'Chicago', 'New York City', or 'Washington'\n").lower()
                    if city in CITY_DATA:
                        break
                except:
                    print("Please only enter Chicago, New York City, or Washington.\n")
                    continue

            # get user input for period
            while True:
                try:
                    period = input("Please enter the time period to filter by:\
'month', 'weekday', or 'both'\n").lower()
                    if period == 'month' or period == 'weekday' or period == 'both':
                        break
                except:
                        print("Please only enter month, weekday, or both.\n")
                        continue

            # get user input for month
            if period == 'month'or period == 'both':
                while True:
                    try:
                        month = input("Please enter the month you would like to investigate: \
All, January, February, March, April, May, June)\n").lower()
                        if month == 'all' or months.count(month) > 0:
                            break
                    except:
                        print("Please only enter all, January, February, March, April, May, June.\n")
                        continue
            elif period == 'weekday':
                month = 'all'

            # get user input for day of week
            if period == 'weekday'or period == 'both':
                while True:
                    try:
                        day = input("Please enter the day you would like to investigate: \
All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
                        if day == 'all' or weekdays.count(day) > 0:
                            break
                    except:
                        print("Please only enter All, Monday, Tuesday, Wednesday, Thursday, \
Friday, Saturday, Sunday.")
                        continue
            elif period == 'month':
                day = 'all'

            # present filters selected to user
            print('The following criteria have been selected:\n\
                    City:   {}'.format(city.title(), month.title()))
            if period != 'weekday':
                print('                    Month:  {}'.format(city.title(), month.title()))
            if period != 'month':
                print('                    Weekday:  {}'.format(city.title(), month.title()))

            # check to see if input data is correct, loop to beggining if not
            while True:
                try:
                    input_check = input('Is this correct? (Y or N)\n')
                    if input_check.lower() == 'yes' or input_check.lower() == 'y':
                        print('-'*40 + '\n')
                        break
                    elif input_check.lower() == 'no' or input_check.lower() == 'n':
                        print ('No problem, I will ask you to input the data again!\n')
                        print('-'*40 + '\n')
                        break
                    else:
                        print("Didn't quite catch that.")
                except:
                    print('Please enter Y or N.\n')
                    continue
            if input_check.lower() == 'yes' or input_check.lower() == 'y':
                break
            else:
                del city
                del period
                del month
                del day
                continue
        except:
            continue

    return city, period, month, day


def load_data(city, period, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) period - time period to filter by, month, weekday or both
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # create df based on filters provided in get_filters()
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        day = weekdays.index(day)
        df = df[df['day_of_week'] == day]

    # Replaces NaNs with the following (str)
    df = df.fillna('No Data Available')

    return df


def time_stats(df, period, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
    df - Pandas DataFrame containing city data filtered by month and day
    (str) period - time period to filter by, month, weekday or both
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # sample size
    sample_size = df.shape[0]
    print('Total number of trips:             {:,}'.format(sample_size))

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    occurences_month = df[df["month"] == popular_month].count()["month"]
    month_percentage = int((occurences_month/sample_size)*100)

    if month == 'all':
        print('Most Popular Month:                {}, {:,} occurences, {:.1f}% of trips'\
.format(months[(popular_month-1)].title(),occurences_month, month_percentage))

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday
    popular_day = df['day_of_week'].mode()[0]
    occurences_weekday = df[df["day_of_week"] == popular_day].count()["day_of_week"]
    weekday_percentage = int((occurences_weekday/sample_size)*100)

    if day == 'all':
        print('Most Popular Day:                  {}, {:,} occurences, {:.1f}% of trips'\
.format(weekdays[popular_day].title(), occurences_weekday, weekday_percentage))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    occurences_hour = df[df['hour'] == popular_hour].count()['hour']
    hour_percentage = int((occurences_hour/sample_size)*100)

    print('Most Popular Start Hour:           {}, {:,} occurences, {:.1f}% of trips'\
.format(popular_hour, occurences_hour, hour_percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args
    df - Pandas DataFrame containing city data filtered by month and day"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # sample size repeated for user ease of reference
    sample_size = df.shape[0]
    print('Total number of trips:             {:,}'.format(sample_size))

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    occurences_start_station = df[df["Start Station"] == popular_start_station].count()["Start Station"]
    start_station_percentage = int((occurences_start_station / sample_size)*100)

    print('Most common station of departure:  {}, {:,} occurences, {:.1f}% of trips'\
.format(popular_start_station.title(), occurences_start_station, start_station_percentage))

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    occurences_end_station = df[df["End Station"] == popular_end_station].count()["End Station"]
    end_station_percentage = int((occurences_end_station / sample_size)*100)

    print('Most common arrival destination:   {}, {:,} occurences, {:.1f}% of trips'\
.format(popular_end_station.title(), occurences_end_station, end_station_percentage))

    # display most frequent combination of start station and end station trip
    df['Station Combo'] = list(zip(df['Start Station'], df['End Station']))
    popular_combo = df['Station Combo'].mode()[0]
    popular_combo_stations = []
    for x in popular_combo:
        popular_combo_stations.append(x)
    occurences_combo_station = df[df['Station Combo'] == popular_combo].count()['Station Combo']
    combo_station_percentage = int((occurences_combo_station/sample_size)*100)

    # display the most common trip
    print('Most common journey:               {} (start), {} (end), {:,} occurences, {:.1f}% of trips'\
.format(popular_combo_stations[0].title(),popular_combo_stations[1].title(),\
occurences_combo_station, combo_station_percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args
    df - Pandas DataFrame containing city data filtered by month and day"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Duration Mins'] = df['Trip Duration']/60
    df['Trip Duration Hours'] = df['Trip Duration Mins']/60

    # display total travel time
    total_travel_time = df['Trip Duration Hours'].sum()
    print ('Total travel time:                 {:,} hours'.format(int(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration Mins'].mean()
    print ('Mean travel time:                  {:.1f} minutes\n'.format(mean_travel_time))

    # display other statistics for trips using .describe()
    df['Trip Duration Mins'] = df['Trip Duration']/60
    print('Some other useful Trip Duration statistics (minutes):\n{}'\
.format(df['Trip Duration Mins'].describe().astype(float)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n')


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args
    df - Pandas DataFrame containing city data filtered by month and day"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts and proportion of user types
    print('Breakdown of data user types:\n \n{}\n \n{}\n \n'\
.format(df['User Type'].value_counts().astype(float),\
df['User Type'].value_counts(normalize=True)))

    # Display counts and proportion of uesr type gender
    while True:
        try:
            print('Breakdown of data for passenger gender:\n \n{}\n \n{} \n \n'\
.format(df['Gender'].value_counts().astype(float).round(0),\
df['Gender'].value_counts(normalize=True)))
            break
        except:
            print('No passenger data in respect of gender')
            break

    # Display earliest, most recent, and most common year of birth
    while True:
        try:
            print('The earliest passenger birth year was {}, the most recent birth\
 year was {} and the most common birth year was {}.'.format(\
 int(df['Birth Year'].min()), int(df['Birth Year'].max()),int(df['Birth Year'].mode())))
            break
        except:
            print('No passenger data in respect of birth year')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40 + '\n')


def raw_data(df):
    """Asks the user if they would like to see the raw data and returns the
    next 5 trips transposed and split into two frames for ease of analysis.

    Args
    df - Pandas DataFrame containing city data filtered by month and day"""
    x = 0
    while True:
        try:
            next_five = input("\nWould you like to see the raw data? (Y or N)\n")
            if next_five.lower() == 'yes' or next_five.lower() == 'y' or next_five\
.lower() == 'no' or next_five.lower() == 'n':
                while next_five.lower() == 'yes' or next_five.lower() == 'y':
                    print("Index numbers may not be sequential due to filters applied.")
                    print(df.iloc[x:x+3, 1:-6].T)
                    print(df.iloc[x+3:x+5, 1:-6].T)
                    print("\n")
                    x += 5
                    next_five = input("Would you like to see data for another 5 \
trips from filtered data table? (Y or N)\n").lower()
                    if next_five == 'no' or next_five == 'n':
                            break
                else:
                    break
                break
            else:
                print("I didn't quite catch that, please enter Y or N.")
        except:
            print("Beg your pardon! Please enter Y or N.")
            continue


def main():
    """Calls functions above in intended order"""

    while True:
        city, period, month, day = get_filters()
        df = load_data(city, period, month, day)
        time_stats(df, period, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.count('y') != 1:
            break

if __name__ == "__main__":
	main()
