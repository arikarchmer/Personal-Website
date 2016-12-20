__author__ = 'arikarchmer'

# Import the necessary methods from tweepy library
import tweepy
import json
import time

# Variables that contains the user credentials to access Twitter API
access_token = '808498225900613633-aeGBgA2JZk8wB1mLLOQbR63Zq5UviDs'
access_token_secret = 'doesjrt3PieG5vhDcXdbsBDlraCM0Oms4C0AhwmGHk7MX'
consumer_key = '6wOQlvSvooysExtJ5UDv0DbdU'
consumer_secret = 'AeIfxo2FZqARwwp9tHnlkCM0d9cnPCdiyjHggzDPhbOxyo1tge'


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        obj = json.loads(data)

        if 'text' in obj and obj['text']:
            if 'id' in obj and obj['id']:
                tweet_id = obj['id']
                user_name = obj['user']['screen_name']
                if 'retweeted_status' in obj and obj['retweeted_status']:
                    print 'retweet'
                    orig_status = obj['retweeted_status']
                    orig_status_name = orig_status['user']['screen_name']
                    orig_status_id = orig_status['id']
                    api.update_status(status='@'+user_name+' '+'@'+orig_status_name+' RIP',
                                      in_reply_to_status_id=orig_status_id)
                else:
                    api.update_status(status='@' + user_name + ' RIP',
                                  in_reply_to_status_id=tweet_id)

                print 'tweet'

        return True

    def on_error(self, status):
        print status
        print 'restarting stream.....'
        time.sleep(5)
        print 'stream is restarted.'
        return True


if __name__ == '__main__':


    # # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, l)

    stream.filter(track=['lol "im dead"', 'lmao "im dead"', 'lmao "im ded"', 'lol "im ded"'])

    # got suspended :(

    # s = api.user_timeline(count=29)
    #
    # for t in s:
    #     api.destroy_status(t.id)
