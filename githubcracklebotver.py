#! python
import praw, tweepy, time, re, pickle

postedTweetsarray = []



r = praw.Reddit(user_agent = "x")
r.login("x","x")

#Reddit API call functions
def listenToThis():
    subreddit = r.get_subreddit("listentothis")

    for submission in subreddit.get_hot(limit=23):
        if (isMusic(submission.url,submission.title)):
            tweetPost(submission.title,submission.url,submission.link_flair_text)

def music():
    subreddit = r.get_subreddit("music")
    PostFlair = ''

    for submission in subreddit.get_hot(limit=20):
        if (isMusic(submission.url,submission.title)):
            if ('music streaming' in submission.link_flair_text) or ('stream' in submission.link_flair_text):
                PostFlair = submission.title
                PostFlair = PostFlair[PostFlair.find("[")+1:PostFlair.find("]")]
                tweetPost(submission.title,submission.url,PostFlair)
                
def indieHeads():
    subreddit = r.get_subreddit("indieheads")

    for submission in subreddit.get_hot(limit=20):
        if (isMusic(submission.url,submission.title)):
            if('Fresh' in submission.title) or('fresh' in submission.title)or('FRESH' in submission.title)or('ORIGINAL' in submission.title)or('Original' in submission.title) or ('original' in submission.title):
                tweetPost(submission.title,submission.url,"Indie")

def hiphopHeads():
    subreddit = r.get_subreddit("hiphopheads")

    for submission in subreddit.get_hot(limit=20):
        if (isMusic(submission.url,submission.title)):
            if('Fresh' in submission.title) or('fresh' in submission.title)or('FRESH' in submission.title)or('ORIGINAL' in submission.title)or('Original' in submission.title) or ('original' in submission.title):
                tweetPost(submission.title,submission.url,'hiphop')

def electronicMusic():
    subreddit = r.get_subreddit("electronicmusic")
    PostFlair = 'electronic'

    for submission in subreddit.get_hot(limit=20):
        if (isMusic(submission.url,submission.title)):
            tweetPost(submission.title,submission.url,PostFlair)

#twitter bot function
def tweetPost(title,url,flair):
    CONSUMER_KEY = 'x'#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = 'x'#keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = 'x'#keep the quotes, replace this with your access token
    ACCESS_SECRET = 'x'#keep the quotes, replace this with your access token secret
    nonDuplicateFlag = True
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    #Clean link to prepare for tweeting
    try:
        flair = '#'+ flairCleanup(flair)
    except:
        print('flair is not of type string. Moving on without flair.')
        flair =''
    title = tweetCleanup(title)
    c = tweepy.Cursor(api.search, q='cracklebox ' + title,show_user = True,count=400)#search for duplicates
    time.sleep(10)#API max request compensation delay
    
    #handle if duplicates found
    for tweet in c.items():
        nonDuplicateFlag = False#if duplicate exists the tweet is discarded
    
    tweet = (title + " " + url + flair)#final post composition
    tweet = tweetCleanup(tweet)               #final cleanup
    if (tweet in postedTweetsarray):
        nonDuplicateFlag = False
    
    if (nonDuplicateFlag):

        try:
            api.update_status(tweet)#add tweet to timeline
        except:
            print('tweet not posted. Probably a length issue')#verbose output for failed tweet. To be determined.
    
        time.sleep(290)
    postedTweetsarray.append(tweet)
    updateDB()
#Minor functions
def flairCleanup(returnFlair):
    returnFlair = re.sub('&', 'and', returnFlair)#turn drum & bass into drumandbass for hashtag handling and uniformity
    returnFlair = re.sub('[/, ]', ' #', returnFlair) 
    returnFlair = re.sub('[#][\s]', '', returnFlair)
    return returnFlair

def tweetCleanup(returnTweet):
    returnTweet = re.sub('[(){}<>]', '', returnTweet)#delete unnecessary parentheses
    returnTweet = re.sub('[0-9]{4}', '', returnTweet)#delete year
    returnTweet = re.sub('[-]{2,3}', '-', returnTweet)#delete double dashes
    returnTweet = re.sub('#[\w]{3}[-][\w]{3}', '#hiphop', returnTweet)#turn hip-hop into hiphop for hashtag handling
        
    return returnTweet

def isMusic(URL, title):
    if ('youtube.com' in URL) or ('soundcloud.com' in URL) or ('spotify.com' in URL) or ('bandcamp.com' in URL):
        if('playlist' in title) or ( 'Playlist' in title):#check if playlist link or not. If playlist detected the link is discarded
            return False
        else:
            return True

#Main runtime function

def initDB():

    global postedTweetsarray
    try:
        with open('posts.DAT', 'rb') as f:
            postedTweetsarray = pickle.load(f)
    except:
        print('no previous posts found')
        return
def updateDB():
    global postedTweetsarray
    with open('posts.DAT', 'wb+') as f:
        pickle.dump(postedTweetsarray, f)
        
if __name__ == "__main__":
    initDB()
    while True:
        listenToThis()
        music()
        indieHeads()
        hiphopHeads()
        electronicMusic()
