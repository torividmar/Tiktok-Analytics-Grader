"""
Tori Vidmar
Section 0105
"""

import csv
import matplotlib.pyplot as plt
import math
import time


def csv_to_dict(file_path):  # function that imports CSV data and turns it into a column dictionary
    data_dict = {}
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # read header row to get column labels
        labels = next(csv_reader)

        # initialize dictionary with empty lists for each column (excluding the first column)
        data_dict = {label: [] for label in labels[1:]}

        # read remaining lines and populate the dictionary
        for row in csv_reader:
            for label, value in zip(labels[1:], row[1:]):  # exclude the first column of dates because not str
                # convert numeric values to float
                data_dict[label].append(float(value))

    return data_dict


def count_rows(file_path):
    # function that counts # of rows (= timespan of file)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # skip header row
        num_rows = sum(1 for row in csv_reader)  # count remaining rows

    return num_rows


def averages(data_dict):
    averages = {}
    i = 0
    for label, values in data_dict.items():
        # calculate the average for each column (each data category)
        if len(values) > 0:
            average = round(sum(values) / len(values), 2)  # rounds to nearest hundredth
            averages[label] = average
        else:
            averages[label] = None  # if dividing by zero (aka an empty list)

    return averages


def plot_columns(data_dict):
    num_columns = len(data_dict)
    num_rows = (num_columns + 1) // 2  # adjust number of rows based on the number of columns
    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5 * num_rows))
    axes = axes.flatten()

    # plot each column in a separate subplot
    for i, (label, values) in enumerate(data_dict.items()):
        ax = axes[i]
        color = f'C{i}'
        ax.plot(values, label=label, color=color)
        ax.set_title(label)
        ax.set_xlabel('Time (in days)')
        ax.set_ylabel('Values')
        ax.legend()

    fig.suptitle('Graphs of Analytics from Key Metrics CSV')
    plt.tight_layout()  # adjust layout so no overlap
    plt.show()


def plot_columns2(data_dict, y_labels):
    num_columns = len(data_dict)
    num_rows = (num_columns + 1) // 2  # Adjust the number of rows based on the number of columns

    fig, axes = plt.subplots(num_rows, 2, figsize=(10, 5 * num_rows))

    # Flatten the axes array to simplify indexing
    axes = axes.flatten()

    # Plot each column in a separate subplot
    for i, (label, values) in enumerate(data_dict.items()):
        ax = axes[i]
        color = f'C{i}'
        ax.plot(values, label=label, color=color)
        ax.set_title(label)
        ax.set_xlabel('Time (in days)')
        ax.set_ylabel('')

        if label in y_labels:
            ax.set_ylabel(y_labels[label])
        else:
            ax.set_ylabel(label)

    fig.suptitle('Graphs of Analytics from Total Followers CSV')
    plt.tight_layout()
    plt.show()


def divide_averages(data_dict, numerator, denominator):
    if numerator in data_dict and denominator in data_dict:
        num_avg = sum(data_dict[numerator]) / len(data_dict[numerator])
        denom_avg = sum(data_dict[denominator]) / len(data_dict[denominator])

        if denom_avg != 0:
            ratio = round(num_avg / denom_avg)
            return ratio
        else:
            print("Error: Division by zero. Denominator average is zero.")
            return None
    else:
        print("Error: One or both column labels not found.")
        return None


def column_sum(data_dict, column_label):  # function that calculates the sum of a chosen column
        column_values = data_dict[column_label]
        column_sum = sum(column_values)
        return column_sum


def growth_percentage(data_dict, difference):  # calculates ratio of total profile views to followers gained
    column_label = 'Profile Views'
    if column_label in data_dict:
        # add all values in 'Profile Views' columns
        column_total = int(sum(data_dict[column_label]))
        growth_ratio = float(column_total / difference)  # calculate ratio
        growth_percent = round(float(difference / column_total * 100), 2)  # turn ratio to percent
        return growth_ratio, column_total, growth_percent
    else:
        print(f"Column '{column_label}' not found.")


def follower_growth(data_dict):
    column_label = 'Followers'
    column_values = data_dict[column_label]
    # calculate follower growth
    ideal_followers = (column_values[0] * 0.07) + column_values[0]
    actual_followers = column_values[-1]
    if ideal_followers <= actual_followers:
        growth_letter1 = 'A'
        growth_grade1 = 95
        return growth_grade1, growth_letter1
    else:
        growth_letter1 = 'F'
        growth_grade1 = 55
        return growth_grade1, growth_letter1


def growth_grading(growth_percent):  # function that returns users grade based on their account growth stats
    # also works for account reach stats
    if growth_percent <= 5:
        growth_grade = 55
        growth_letter = 'F'
        return growth_grade, growth_letter
    elif (growth_percent > 5) and (growth_percent <= 10):
        growth_grade = 75
        growth_letter = 'C'
        return growth_grade, growth_letter
    elif (growth_percent > 10) and (growth_percent <= 20):
        growth_grade = 85
        growth_letter = 'B'
        return growth_grade, growth_letter
    else:
        growth_grade = 95
        growth_letter = 'A'
        return growth_grade, growth_letter


def growth_grading_total(growth_grade, growth_grade1):
    total = round(((growth_grade + growth_grade1) / 2), 2)
    if total >= 90:
        total_grade = total
        total_letter = 'A'
        exp = "You are excelling in your account growth! Keep doing what you are doing, it's clearly working."
        return total_grade, total_letter, exp
    elif (total < 90) and (total >= 80):
        total_grade = total
        total_letter = 'B'
        exp = "Your account growth is good, but could be better."
        return total_grade, total_letter, exp
    elif (total < 80) and (total >= 70):
        total_grade = total
        total_letter = 'C'
        exp = "Your account growth is okay, but it needs improvement."
        return total_grade, total_letter, exp
    else:
        total_grade = total
        total_letter = 'F'
        exp = "Your account growth needs serious improvement."
        return total_grade, total_letter, exp


def reach_grading(viral_rate):  # function that returns users grade based on their virality rate
    if viral_rate <= 0.1:
        viral_grade = 55
        viral_letter = 'F'
        return viral_grade, viral_letter
    elif (viral_rate > 0.1) and (viral_rate <= 2):
        viral_grade = 75
        viral_letter = 'C'
        return viral_grade, viral_letter
    elif (viral_rate > 2) and (viral_rate <= 5):
        viral_grade = 85
        viral_letter = 'B'
        return viral_grade, viral_letter
    else:
        viral_grade = 95
        viral_letter = 'A'
        return viral_grade, viral_letter


def reach_grading_total(reach_grade, viral_grade):  # function that returns users grade based on their account reach
    total = (reach_grade + viral_grade) / 2
    if total >= 90:
        total_grade = total
        total_letter = 'A'
        exp2 = "You are excelling in your account reach! Keep doing what you are doing, it's clearly working."
        return total_grade, total_letter, exp2
    elif (total < 90) and (total >= 80):
        total_grade = total
        total_letter = 'B'
        exp2 = "Your account reach is pretty good, but could be better."
        return total_grade, total_letter, exp2
    elif (total < 80) and (total >= 70):
        total_grade = total
        total_letter = 'C'
        exp2 = "Your account reach is okay, but it needs improvement."
        return total_grade, total_letter, exp2
    else:
        total_grade = total
        total_letter = 'F'
        exp2 = "Your account reach needs serious improvement."
        return total_grade, total_letter, exp2


def consistency_grade(diff_in_follows):  # function that grades follower growth day to day
    if diff_in_follows > 0:
        cons_grade = 95
        cons_letter = 'A'
        return cons_grade, cons_letter
    else:
        cons_grade = 55
        cons_letter = 'F'
        return cons_grade, cons_letter


def max_to_average(data_dict, column_label):  # function that compares max views/likes to their averages
        column_values = data_dict[column_label]
        largest_val = max(column_values)
        column_average = sum(column_values) / len(column_values)
        ideal_num = 0.1 * largest_val  # good threshold is to have a minimum average of 10% of your maximum

        if column_average >= ideal_num:
            cons_grade1 = 95
            cons_letter1 = 'A'
        else:
            cons_grade1 = 55
            cons_letter1 = 'F'

        return cons_grade1, cons_letter1, largest_val


def cons_grading_total(grade1, grade2, grade3):  # function calculating total consistency grade
    total = round(((grade1 + grade2 + grade3) / 3), 2)
    if total >= 90:
        total_grade = total
        total_letter = 'A'
        exp1 = "You are excelling in your account consistency! Keep doing what you are doing, it's clearly working."
        return total_grade, total_letter, exp1
    elif (total < 90) and (total >= 80):
        total_grade = total
        total_letter = 'B'
        exp1 = "Your account consistency is pretty good, but could be better."
        return total_grade, total_letter, exp1
    elif (total < 80) and (total >= 70):
        total_grade = total
        total_letter = 'C'
        exp1 = "Your account consistency is okay, but it needs improvement."
        return total_grade, total_letter, exp1
    else:
        total_grade = total
        total_letter = 'F'
        exp1 = "Your account consistency needs serious improvement."
        return total_grade, total_letter, exp1


def growth_feedback(total):  # outputs targeted feedback based on growth
    if total >= 80:
        print("Based on our analysis, your account growth is doing well. But, we still have some tips for you:")
        print("Although you are doing well with your overall growth, make sure continue focusing on creating short but")
        print("engaging content that is able to hold your audience's attention.")
    else:
        print("Based on our analysis, your account's growth is a weak point. To improve this, we recommend you:")
        print(" - Keep your videos short and straight to the point, you want to try and hold your audience's attention")
        print("   until the end of your video. The best way to ensure this is to make your videos quick yet engaging.")
        print(" - Promote your TikTok on other social media platforms (Instagram, Snapchat, Youtube, etc.), you are much")
        print("   more likely to gain new followers and viewers this way.")


def reach_feedback(total):  # outputs targeted feedback based on reach
    if total >= 80:
        print("Based on our analysis, your account is reaching a lot of people. In order to keep this momentum, try:")
        print("Obviously, what you are doing is working. However, remember to stay on tops of trends, whether it be ")
        print("trending audios, hashtags, etc. They are popular for a reason!")
    else:
        print("Based on our analysis, your account is not reaching many people. In order to improve, we recommend:")
        print(" - Use trending audios in your videos and posts.")
        print(" - Also, use hashtags related to the content you are posting. This will target people in your niche, who are more ")
        print("   likely to interact with you. ")
        print(" - Keep up with popular TikTok trends, if you can catch onto a trend early, you are more likely to gain popularity,")
        print("   or even go viral!")


def consistency_feedback(total):  # outputs targeted feedback based on consistency
    if total >= 80:
        print("Based on our analysis, your account has a reliable audience who consistently interacts with your content.")
        print("Don't change much with what your doing in regards to consistency. Keep in mind, the more consistent you are ")
        print("with what and when you post, the more viewers and interactions you will get.")
    else:
        print("Based on our analysis, your content and its impressions are inconsistent. To establish a reliable audience:")
        print(" - Find a niche (ex. fashion, fitness, lifestyle, etc.) and stick with it. If you are not consistent with")
        print("   what you are posting, you will not establish a definitive group of viewers.")
        print(" - Post at similar times on similar days of the week.")
        print(" - Find optimal times for you to post based on what videos do best. For reference, good times to post are")
        print("   during the week days around lunch (noon) or dinner time (5-6 pm).")


# MAIN starts below
print("TIKTOK ANALYTICS GRADER")
print("\nWelcome to the TikTok Analytics Grader! Follow the steps below to receive an analysis on your TikTok metrics.")
print('\nMake sure to enter your filepaths in the correct order (first keymetrics.csv, then totalfollowers.csv)')
file_path = input('Enter in the file path to your Key Metrics CSV file (then press Enter): ')
file_path2 = input('Now Enter in the file path to your Total Followers CSV file (then press Enter): ')

# these are the filepaths to my own TikTok analytics files (used to test my code)
# file_path = '/Users/torividmar/Downloads/final_project_380/keymetrics.csv'
# file_path2 = '/Users/torividmar/Downloads/final_project_380/totalfollowers.csv'

# running functions
data_dict = csv_to_dict(file_path)  # key metrics dictionary
data_dict2 = csv_to_dict(file_path2)  # total followers dictionary

num_rows = count_rows(file_path)  # time window of key metrics file
num_rows2 = count_rows(file_path2)  # time window of total followers file

# display the original column dictionary
# print("\nHere are your TikTok Analytics!...unsimplified...\n")
# for label, values in data_dict.items():
    # print(f"{label}: {values}")
# for label, values in data_dict2.items():
    # print(f"{label}: {values}")

# print("\nGross right? Let's simplify all these numbers a bit!")

# calculate and display the column averages
data_averages = averages(data_dict)
data_averages2 = averages(data_dict2)
print("\nThese are your Key Metrics averages (per day):")
averages1 = {}
for label, average in data_averages.items():
    print(f"{label}: {average}")
    averages1[label] = average
print("\nHere are a few more averages, but from your Followers data:")
averages2 = {}
for label, average in data_averages2.items():
    averages2[label] = average
print(f"Average Follower Count (over the past {num_rows2} days): {averages2['Followers']}")
print(f"Change in Followers from Previous Day: {averages2['Difference in followers from previous day']}")

# plot graphs for key metrics and total followers data
plot_columns(data_dict)
y_labels = {'Followers': '# of Followers', 'Difference in followers from previous day': 'Change in # of Followers'}
plot_columns2(data_dict2, y_labels)

print("\nHere are a few interesting stats from your data...")
print("Also make sure to check out the graphs of your analytics under the top right toolbar!")

# choosing two columns for division (ratio of video views to likes)
numerator = 'Video Views'
denominator = 'Likes'
result1 = divide_averages(data_dict, numerator, denominator)  # run function
if result1 is not None:
    print(
        f"\nYou have a view-to-like ratio of {result1}:1. In other words, you get about {result1} views for every like on your videos.")

# like to comment ratio
numerator = 'Likes'
denominator = 'Comments'
result2 = divide_averages(data_dict, numerator, denominator)
if result2 is not None:
    print(
        f"You have a like-to-comment ratio of {result2}:1. So, you get about {result2} likes for every comment on your videos.")

# like to share ratio
numerator = 'Likes'
denominator = 'Shares'
result3 = divide_averages(data_dict, numerator, denominator)
if result3 is not None:
    print(
        f"You have a like-to-share ratio of {result3}:1. So, you get about {result3} likes for every share on your videos.")


# outputting more statistics
print(f'\nOver the past {num_rows2} days...')

# difference between most recent follower count and initial
follower_count = data_dict2[next(iter(data_dict2))]  # extract values of the first column
difference = 0
if follower_count:
    init_value = follower_count[0]
    last_value = follower_count[-1]
    difference = last_value - init_value
    print(f"You have gained {difference} followers.")
else:
    print("ERROR: First column is empty. Check to make sure you downloaded the correct CSV file.")

# GRADING ACCOUNT GROWTH

# run growth_percentage function
growth_ratio, column_total, growth_percent = growth_percentage(data_dict, difference)

# total profile views
print(f'{column_total} people have viewed your profile.')
# total unique viewers
column_label2 = 'Unique Viewers'
unique_viewers = int(sum(data_dict[column_label2]))
print(f'{unique_viewers} unique users have viewed your TikTok videos.')

# run growth functions
growth_grade, growth_letter = growth_grading(growth_percent)
growth_grade1, growth_letter1 = follower_growth(data_dict2)
total_grade, total_letter, exp = growth_grading_total(growth_grade, growth_grade1)

time.sleep(1)
# outputting account growth grade to user
print("\nNow, let's grade your data and see how you can improve your TikTok!")
print("You will be graded based on three different metrics: account reach, growth, and consistency.")
time.sleep(1)
print("\nLet's start by reviewing your account growth...")
print(f"\nFor every {round(growth_ratio)} people who viewed your profile, one person followed you.")
print(f"Meaning that about {growth_percent}% of users that clicked on your profile, also pressed the follow button.")
print("Obviously, the higher this percentage is, the better.")
print(f"Based on our calculations, your overall grade in account growth over the past {num_rows} days is: {total_letter} - {total_grade}%")
print(exp)

# GRADING ACCOUNT REACH

# declare variables
avg_likes = averages1['Likes']
avg_shares = averages1['Shares']
percent_share = float(round(((1 / (avg_likes / avg_shares)) * 100), 2))
sum_shares = column_sum(data_dict, 'Shares')
sum_viewers = column_sum(data_dict, 'Unique Viewers')
viral_rate = float(round(((sum_shares / sum_viewers) * 100), 2))

# run functions for account reach
reach_grade, reach_letter = growth_grading(percent_share)
viral_grade, viral_letter = reach_grading(viral_rate)
reach_grade_total, reach_letter_total, exp2 = reach_grading_total(reach_grade, viral_grade)

# outputting account reach grade
print("\nLet's now move on to your account's reach...")
print(f"\nFor every {result3} people who liked your videos, one person shared it with someone else.")
print(f"In other words, your total shares were {percent_share}% of the amount of likes liked your videos.")
print("You should be aiming for around 10%, however, the higher, the better.")
print(f"Over the past {num_rows} days, you had a virality rate of {viral_rate}%.")
print("The higher this percentage is, the more likely you are to go viral.")
print(f"Your overall grade in account reach is: {reach_letter_total} - {reach_grade_total}%")
print(exp2)

# GRADING ACCOUNT CONSISTENCY

# declare variables
diff_in_follows = averages2['Difference in followers from previous day']
avg_views = averages1['Video Views']

# run first function for grading consistency
cons_grade, cons_letter = consistency_grade(diff_in_follows)

# run max_to_average function for views and likes
video_views = 'Video Views'
max_to_average(data_dict, video_views)
cons_grade1, cons_letter1, largest_views = max_to_average(data_dict, video_views)
likes = 'Likes'
max_to_average(data_dict, likes)
cons_grade2, cons_letter2, largest_likes = max_to_average(data_dict, likes)
final_cons_grade, final_cons_letter, exp1 = cons_grading_total(cons_grade, cons_grade1, cons_grade2)

# outputting account consistency grade
print("\nLastly, what about your account's consistency...")
print(f"\nYou gained about {diff_in_follows} followers each day in the past {num_rows2} days.")
print("For optimized consistency, this number needs to be positive. You want to consistently GAIN followers.")
print(f'The most views you got in a day was {largest_views} views, while you averaged {avg_views} views daily.')
print(f'The most likes you got in a day was {largest_likes} likes, while you averaged {avg_likes} likes daily.')
print("The closer together these numbers are, the better. You want to have consistent video views and interactions.")
print(f"Your overall grade in consistency over the past {num_rows2} days is: {final_cons_letter} - {final_cons_grade}%")
print(exp1)

# targeted feedback starts here
print("\nFinally, we have some personalized tips on how you can improve your account!")

# run all feedback functions

# account growth
print("\nFOR ACCOUNT GROWTH:")
growth_feedback(total_grade)

# account reach
print("\nFOR ACCOUNT REACH:")
reach_feedback(reach_grade_total)

# account consistency
print("\nFOR ACCOUNT CONSISTENCY:")
consistency_feedback(final_cons_grade)
print("\n")

# end
print("Thank you for trying the TikTok Analytics Grader! Enjoy the rest of your day :)")


