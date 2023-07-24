import time
import pandas as pd
import numpy as np
from datetime import timedelta
import random

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']

def get_month():
    """
    Get user input  for month of the year (all, january, february, ... , june)

    Returns:
        (str) month - name of the month to filter by
    """
    print("\nWhich month data would you be interested in exploring")
    month = None
    while month is None:
        month = input("Month - ").lower()
        if month not in set(MONTH_DATA):
            print("\nIs there a spelling error. Can you please enter the correct month name")
            month = None
    
    return month
    

def get_day():
    """
    Get user input for day of week (all, monday, tuesday, ... sunday)

    Returns:
        (str) day - name of the day of week to filter by
    """
    day_list = ["monday",'tuesday','wednesday','thursday','friday','saturday','sunday']
    print("\nWhich day data would you be interested in exploring")
    day = None
    while day is None:
        day = input("Day - ").lower()
        if day not in day_list:
            print("\nIs there a spelling error. Can you please enter the correct day name")
            day = None
        
    return day



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
    city = None
    print("Which city data would you be interested in exploring - Chicago, New York City or Washington ")
    while city is None:
        city = input("City - ").lower()
        if city not in CITY_DATA.keys():
            print("\nUnfortunately we don't hold data for given city. Can you please enter the city name from the given choices")
            city = None

    # get user input for data filter choice (month, day, both, none)        
    filter_choice = None
    print("\nHow would you like to filter your data - by month, day, both or none")
    while filter_choice is None:
        filter_choice = input("Choice - ").lower()
        if filter_choice not in ["month","day","both","none"]:
            print("\nOops, thats not an available choice. Please select from the options available - month, day, both or none")
            filter_choice = None
    
    print(random.choice(["Great choice!","Amazing!","Alright..."]))

    # get user input for month and day based on the filter choice selected, or "all" to apply no filter
    month = "all"
    day = "all"
    if filter_choice == "month":
        month = get_month()
    elif filter_choice == "day":
        day = get_day()
    elif filter_choice == "both":
        month = get_month()
        day = get_day()    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*120)
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
    global CITY_DATA

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city],index_col='Unnamed: 0')
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    


    # filter by month if applicable
    if month != 'all':
        month = MONTH_DATA.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month+1]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    df['hour'] = df['Start Time'].dt.hour
    df['path'] = df['Start Station'] + df['End Station']
    df.sort_values(by=['Start Time'])
    
    if city != 'washington':
        df['Birth Year'] = df['Birth Year'].round().astype('Int64')

    df = df.reset_index(drop=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = MONTH_DATA[df['month'].mode()[0]-1]
    print("Most common month - {}".format(most_common_month))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("\nMost common day of the week - {}".format(most_common_day))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("\nMost common start hour - {}".format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most popular start station - {}".format(most_common_start_station))


    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most popular end station - {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most frequent combination - {}".format(most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum()
    print("Total Trip duration - {} ".format(timedelta(seconds = int(total_travel_duration))))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average Travel Duration - {} ".format(timedelta(seconds=int(mean_travel_time))))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_by_user_type = df['User Type'].value_counts()
    print("Total Subscribers - {}".format(count_by_user_type["Subscriber"]))
    print("Total Customers - {}".format(count_by_user_type["Customer"]))

    if city != 'washington':
        # Display counts of gender
        count_by_gender = df['Gender'].value_counts()
        print("\nTotal Male users - {}".format(count_by_gender["Male"]))
        print("Total Female users - {}".format(count_by_gender["Female"]))

        print("We have most {} riders in this dataset".format(["Male" if count_by_gender["Male"] > count_by_gender["Female"] else "Female"]))


        # Display earliest, most recent, and most common year of birth

        # Display youngest rider's birth year 
        youngest_rider_birth_year = df['Birth Year'].max()
        print("\nYounger bike rider's birth year - {}".format(youngest_rider_birth_year))

        # Display older rider's birth year
        oldest_rider_birth_year = df['Birth Year'].min()
        print("Oldest bike rider's birth year - {}".format(oldest_rider_birth_year))

        # Display the birth year of the first rider
        earliest_ride_birth_year = df['Birth Year'].iloc[0]
        print("\nEarliest bike rider's birth year - {}".format(earliest_ride_birth_year))

        # Display the birth year of the recent rider
        most_recent_ride_birth_year = df['Birth Year'].iloc[-1]
        print("Most Recent bike rider's birth year - {}".format(most_recent_ride_birth_year))

        # Display the most common birth year
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nMost common birth year - {}".format(common_birth_year))
    
    else:
        print("Unfortunately, no data available related to Gender and Birth Year for Washington city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def display_data(df):
    choice = input("Do you want to view raw data. Enter yes or no - ")
    start = 0
    while True:
        if choice not in ["yes","no"]:
            choice = input("Please select yes or no - ")
        elif choice == "yes":
            print(df.iloc[start:start+5])
            start +=5
            choice = input("Do you want to continue exploring raw data? Enter yes or no - ")
            if choice.lower() == "no":
                break
        else:
            break
    


def menu_header():
    #Displays Menu Header for the first run

    print("*"*120)
    print("*"*120)
    print("""
                   ___        ___        __  __             __   __                               __    __
            |   | |___       |___| | |/ |_  |__ |__|  /_\  |__| |_         /_\  |\ |  /_\  |   | |__ | |__
            |___| ___|       |___| | |\ |__ __| |  | /   \ |  \ |__       /   \ | \| /   \ |__ | __| | __|
          
    """)
    print("*"*120)
    print("*"*120)

def main():
    menu_header()
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
