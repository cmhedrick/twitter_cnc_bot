#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import time
from credentials import *
from random import randint

# perform authentication with OAuth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

lasttweet = None
toggle = True
delay = 10

# wordlist (sentencelist) of content bot will tweet
filename = open(TWEETLIST, 'r')
tweettext = filename.readlines()
filename.close()

def linenum():
    '''
    selects random line int between the 0 and the length of the lines in the
    text file
    :return: None
    '''
    return randint(0, (len(tweettext)-1))


def runTime():
    '''
    runs the actual bot
    :return: None
    '''
    global lasttweet
    global toggle

    # checks for the most recent tweet from master account
    mostrecenttweet = api.user_timeline(MASTER_ACC)[0]
    print(">>> MASTER\'S RECENT TWEET ID: {0}".format(mostrecenttweet.id))
    parsed_tweet = mostrecenttweet.text.lower().split()
    print(">>> MASTER\'S PARSED TWEET: {0}".format(parsed_tweet))
    if 'start' in parsed_tweet:
        doTweet()
    elif 'stop' in parsed_tweet:
        print("[X] STOPPED")
    elif 'end' in parsed_tweet:
        toggle = False
        print("[!] KILLING BOT")
    else:
        print("[!] LINE ERROR!!")
    lasttweet = mostrecenttweet

def doTweet():
    '''
    picks tweet at random from tweet list and then performs the tweet
    :return: None
    '''
    try:
        line = tweettext[linenum()]
        api.update_status(status=line)
        print(">>> SLAVE RESPONSE: {0}".format(line))
    except tweepy.error.TweepError:
        print("[!] DUPLICATE DAMNIT")    
        
while toggle:
    runTime()
    print("[X] SLEEPING FOR {0}".format(delay))
    time.sleep(delay)
    delay += 5
