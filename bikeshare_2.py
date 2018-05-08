import time
import pandas as pd
from statistics import mode
import calendar
import random

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_names = ['chicago','new york city','washington']
    city = '';   
    while city not in city_names:
        city = input('''Enter the city you would like to explore:'
                     Chicago
                     New York City
                     Washington
                         
                     Input: ''')
        city = city.lower()
        if city in city_names:
            print('Let\'s explore: {}!'.format(city.title()))
        if city not in city_names:
            print('I did not understand that, please try again')   
            
 

    # get user input for month (all, january, february, ... , june)
    month_names = ['all months','january','february','march','april','may','june']
    month = '';   
    while month not in month_names:
        month = input('''Enter one of the following options you would like to explore:'
                     All Months
                     January
                     February
                     March
                     April
                     May
                     June
                         
                     Input: ''')
        month = month.lower()
        if month in month_names:
            print('Let\'s explore: {}!'.format(month.title()))
        if month not in month_names:
            print('I did not understand that, please try again')  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_names = ['all days','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = '';   
    while day not in day_names:
        day = input('''Enter one of the following options you would like to explore:'
                     All Days
                     Monday
                     Tuesday
                     Wednesday
                     Thursday
                     Friday
                     Saturday
                     Sunday
                         
                     Input: ''')
        day = day.lower()
        if day in day_names:
            print('Let\'s explore: {}!'.format(day.title()))
        if day not in day_names:
            print('I did not understand that, please try again')  

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all months':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all days':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data(df):
    '''Allows user to view raw data.'''
    while True:
        print('\nThe data has been loaded and sorted.')
        choice = input('Would you like to see a sample of the data?\n')
        if choice.lower()  == 'yes':
            print('\nColumn Names                       Data Sample')
            print(df.loc[random.choice(df.index)])
        else:     
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('')
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_num = mode(df['month'])
    print('The most popular month to ride is: {}'.format(calendar.month_name[month_num]))

    # display the most common day of week
    print('The most popular day to ride is: {}'.format(mode(df['day_of_week'])))

    # display the most common start hour
    print('The most popular hour to start riding is: {}'.format(mode(df['start_hour'])))

    print("\nThis took {0:.5f}s seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = mode(df['Start Station'])
    mode_count_start = len(df[df['Start Station'] == mode_start_station])
    print('The most common Start Station is: {}'.format(mode_start_station))
    print('Users start at this station {0:.2f}% of the time.'.format(100*mode_count_start/len(df)))
    print('')
    
    # display most commonly used end station
    mode_end_station = mode(df['End Station'])
    mode_count_end = len(df[df['End Station'] == mode_end_station])
    print('The most common End Station is: {}'.format(mode(df['End Station'])))
    print('Users end at this station {0:.2f}% of the time.'.format(100*mode_count_end/len(df)))
    print('')
    
    # display most frequent combination of start station and end station trip
    df['combined_stations'] = df['Start Station'] + " - " + df['End Station']
    mode_combined_stations = mode(df['combined_stations'])
    mode_count_combined = len(df[df['combined_stations'] == mode_combined_stations])
    print('The most common combination of Start & End Stations is:')
    print('{}'.format(mode(df['combined_stations'])))
    print('Users make this specific trip {0:.2f}% of the time.'.format(100*mode_count_combined/len(df)))
    

    print("\nThis took {0:.5f}s seconds.".format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trips_mins = df['Trip Duration'].sum() / 60
    total_trips_days = total_trips_mins / 1440.0
    print('For the period selected, all users rode a combined {0:,.0f} minutes!'.format(total_trips_mins))
    print('That\'s too many minutes.  It\'s easier to think about it as {0:,.1f} days.'.format(total_trips_days))
    print('')
    # display mean travel time
    print('For the period selected, the average ride was {0:,.1f} minutes.'.format(df['Trip Duration'].mean()/60))

    print("\nThis took {0:.5f}s seconds.".format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print('')

    if 'Gender' in df.columns:
        # Display counts of gender
        print(df['Gender'].value_counts())
        print('')
    
        # Display earliest, most recent, and most common year of birth
        print('Birth Year Information:')
        print('Earliest Birth Year: {}'.format(int(df['Birth Year'].min())))
        print('Most Recent Birth Year: {}'.format(int(df['Birth Year'].max())))
        print('Average Birth Year: {}'.format(int(df['Birth Year'].mean())))
    
        print("\nThis took {0:.5f}s seconds.".format(time.time() - start_time))
        print('-'*40)
    else:
        print('Sorry, Gender and Birth Year information is not available for Washington.')
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
