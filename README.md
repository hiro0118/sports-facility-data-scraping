# What does this do?

The scipt in this project gathers the current data about how many people have joined raffles for using tennis courts, which possibly hepls you get a better chance of winning the raffles for the next month.

When reserving sports facilities in Tokyo, you go to the [official website]([http/:](https://yoyaku.sports.metro.tokyo.lg.jp/web/)) and make reservations. As Tokyo is the most crowded city in the world, you need to participate in raffles every month to use a tennis court on a weekend, for example.

This website by the goverment is, however, not very user-friendly, which makes it hard for you to check on which days/time and which courts you have a better chance of winning. 

The script in this project will collect helpful data by scraping the website pages which consits of the following.

- Date
- Park name
- Start/end time
- Available courts
- Number of applicants


# Requirements
The following need to be installed to run the python sripts. (Thinking of running them in a docker container...)
- Windows 11
- python 3.10.5
- pip 22.0.4

The dependencies can be installed using pip and the `pip_list.txt` file. The data scraping process is mainly done using Selenium.
```
pip isntall -r pip_list.txt
```

# How to run the script
1. Put your login info in `login_info.py`
2. Run `python ./get_tennis_application_status.py`
3. A result file will be generated under the output directoy. 
 
# Cautionary notes

## The service monitors irregular requests

It seems that if too many requests are sent from a account, the server starts throttling any requests coming from the same account at some point. Requests still go through, but responses become very very slow. Do not run the scripts so many times in a short period of time. The intended use of the script for tennis court, is once a month before the deadline of the raffles.

The intervals of the steps can be easily configured, but make sure the intervals never go below one second.

## Automatic reservation using scripts is over the top IMO

I am not going to create another script that automatically reserves a tennis court when someone cancells it because that will require frequent data scraping which could overload the service. Also that does not seem fair to those who want to play tennis in the same way.