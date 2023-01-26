import datetime

last_timestamp = 25
print(last_timestamp)

start_game_day = int(str(datetime.datetime.today()).split(' ')[0].split('-')[2])

whole_days = 0

if last_timestamp < start_game_day:
    days_passed = 31 - last_timestamp + start_game_day
    print(days_passed)
else:
    days_passed = last_timestamp - start_game_day
    print(days_passed)




# print(last_timestamp - start_game_day)

