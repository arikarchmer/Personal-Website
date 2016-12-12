import tweepy
import re
import random
import time
import botkeys.keys as k


def createMap():
    dict = {}
    with open('waltwhitman.txt', 'r') as file:
        while file.readline():
            line = re.sub("[^a-zA-Z]", " ", file.readline())
            tokenized_line = line.split(' ')

            for w in range(len(tokenized_line)):

                if w < len(tokenized_line) - 2:

                    word = tokenized_line[w].lower().strip()
                    second_word = tokenized_line[w + 1].lower().strip()
                    next_word = tokenized_line[w + 2].lower().strip()

                    if next_word == ' ':
                        next_word = ''

                    if word is not '' and second_word is not '':
                        k = word + ' ' + second_word

                        if next_word is not '':
                            if k in dict.keys():
                                dict[k].append(next_word)
                            else:
                                dict[k] = list()
                                dict[k].append(next_word)

    return dict


def generateSentence(w1, w2, d, lim):
    res = w1 + ' ' + w2 + ' '
    for i in range(lim):
        if w1 + ' ' + w2 in d.keys():
            nxt = getCommonWord(d[w1 + ' ' + w2])
            res += nxt + ' '
            w1 = w2
            w2 = nxt
#             w3 = nxt
        else:
            return res
    return res


def getCommonWord(lst):
    return lst[random.randint(0, len(lst) - 1)]


def genPoem(lines, wpl, dict):
    s=[]
    str=''
    for i in range(lines):
        index = random.randint(0, len(dict.keys()) - 1)
        s = dict.keys()[index].split(' ')

        str += generateSentence(s[0], s[1], dict, wpl) + '\n'

    print 'done'
    return str


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = tweepy.OAuthHandler(k.Keys.consumer_key, k.Keys.consumer_secret)
    auth.set_access_token(k.Keys.access_token, k.Keys.access_token_secret)

    api = tweepy.API(auth)

    wordmap = createMap()

    while True:
        api.update_status(status=genPoem(2, random.randint(10,15), wordmap))
        # print 'tweeted'
        time.sleep(3600)
