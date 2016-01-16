#! python
import time
import re
import pickle
import praw
import tweepy
postedTweetsarray = []



redditObj = praw.Reddit(user_agent = "x")
redditObj.login("x", "x")

#Reddit API call functions
def listentothis():
    """Search for posts in listentothis subreddit"""

    subreddit = redditObj.get_subreddit("listentothis")

    for submission in subreddit.get_hot(limit=23):
        if is_music(submission.url, submission.title):
            tweet_post(submission.title, submission.url, submission.link_flair_text)

def music():
    """Search for posts in music subreddit"""
    subreddit = redditObj.get_subreddit("music")
    postFlair = ''

    for submission in subreddit.get_hot(limit=20):
        if is_music(submission.url, submission.title):
            if ('music streaming' in submission.link_flair_text) or ('stream' in submission.link_flair_text):
                postFlair = submission.title
                postFlair = postFlair[postFlair.find("[")+1:postFlair.find("]")]
                tweet_post(submission.title, submission.url, postFlair)         
def indieheads():
    """Search for posts in indieheads subreddit"""
    subreddit = redditObj.get_subreddit("indieheads")

    for submission in subreddit.get_hot(limit=20):
        if is_music(submission.url, submission.title):
            if('Fresh' in submission.title) or('fresh' in submission.title)or('FRESH' in submission.title)or('ORIGINAL' in submission.title)or('Original' in submission.title) or ('original' in submission.title):
                tweet_post(submission.title, submission.url, "Indie")
def hiphopheads():
    """Search for posts in hiphopheads subreddit"""
    subreddit = redditObj.get_subreddit("hiphopheads")

    for submission in subreddit.get_hot(limit=20):
        if is_music(submission.url, submission.title):
            if('Fresh' in submission.title) or('fresh' in submission.title)or('FRESH' in submission.title)or('ORIGINAL' in submission.title)or('Original' in submission.title) or ('original' in submission.title):
                tweet_post(submission.title, submission.url, 'hiphop')
def electronicmusic():
    """Search for posts in electronicmusic subreddit"""
    subreddit = redditObj.get_subreddit("electronicmusic")
    postFlair = 'electronic'

    for submission in subreddit.get_hot(limit=20):
        if is_music(submission.url, submission.title):
            tweet_post(submission.title, submission.url, postFlair)
#twitter bot function
def tweet_post(title, url, flair):
    """Post found tweets to twitter"""
    CONSUMERKEY = 'x'#keep the quotes, replace this with your consumer key
    CONSUMERSECRET = 'x'#keep the quotes, replace this with your consumer secret key
    ACCESSKEY = 'x'#keep the quotes, replace this with your access token
    ACCESSSECRET = 'x'#keep the quotes, replace this with your access token secret
    nonDuplicateFlag = True
    auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
    auth.set_access_token(ACCESSKEY, ACCESSSECRET)
    api = tweepy.API(auth)
    #Clean link to prepare for tweeting
    try:
        flair = '#'+ flair_cleanup(flair)
    except:
        print('flair is not of type string. Moving on without flairedditObj.')
        flair = ''
    title = tweet_cleanup(title)
    c = tweepy.Cursor(api.search, q ='cracklebox ' + title, show_user= True, count=400)#search for duplicates
    time.sleep(10)#API max request compensation delay 
    #handle if duplicates found
    for tweet in c.items():
        nonDuplicateFlag = False#if duplicate exists the tweet is discarded
    
    tweet = (title + " " + url + flair)#final post composition
    tweet = tweet_cleanup(tweet)               #final cleanup
    if (tweet in postedTweetsarray):
        nonDuplicateFlag = False
    
    if (nonDuplicateFlag):
        try:
            api.update_status(tweet)#add tweet to timeline
        except:
            print('tweet not posted. Probably a length issue')
            #verbose output for failed tweet. To be determined.
        time.sleep(290)
    postedTweetsarray.append(tweet)
    update_db()
#Minor functions
def flair_cleanup(returnFlair):
    """format flair to tweet content """
    returnFlair = re.sub('&', 'and', returnFlair)
    #turn drum & bass into drumandbass for hashtag handling and uniformity
    returnFlair = re.sub('[/, ]', ' #', returnFlair) 
    returnFlair = re.sub('[#][\s]', '', returnFlair)
    return returnFlair
def tweet_cleanup(returnTweet):
    """format actual content of the flair"""
    returnTweet = re.sub('[(){}<>]', '', returnTweet)
    #delete unnecessary parentheses
    returnTweet = re.sub('[0-9]{4}', '', returnTweet)
    #delete year
    returnTweet = re.sub('[-]{2, 3}', '-', returnTweet)
    #delete double dashes
    returnTweet = re.sub('#[\w]{3}[-][\w]{3}', '#hiphop', returnTweet)
    #turn hip-hop into hiphop for hashtag handling
    return returnTweet
def is_music(url, title):
    """check if reddit post is playlist"""
    if ('youtube.com' in url) or ('soundcloud.com' in url) or ('spotify.com' in url) or ('bandcamp.com' in url):
        if('playlist' in title) or ('Playlist' in title):
        #check if playlist link or not. If playlist detected the link is discarded
            return False
        else:
            return True
#Main runtime function
def init_db():
    """Initialize postarray"""

    global postedTweetsarray
    try:
        with open('posts.DAT', 'rb') as fileRead:
            postedTweetsarray = pickle.load(fileRead)
    except:
        print('no previous posts found')
        return
def update_db():
    """dump posted tweet to array"""
    global postedTweetsarray
    with open('posts.DAT', 'wb+') as fileWrite:
        pickle.dump(postedTweetsarray, fileWrite)
        
if __name__ == "__main__":
    init_db()
    while True:
        listentothis()
        music()
        indieheads()
        hiphopheads()
        electronicmusic()
