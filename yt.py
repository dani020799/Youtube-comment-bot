import os
import google.oauth2.credentials
import requests
from bs4 import BeautifulSoup
import math
import random
from random import random
from random import randint
import json
import google_auth_oauthlib.flow
import urllib.request
import time
from datetime import datetime
 # from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
 # from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow


CLIENT_SECRETS_INDEX=0
CLIENT_SECRETS_FILES = ["client_secret.json","client_secret2.json","client_secret3.json"]
API_INDEX=1
API_KEYS=["AIzaSyDpHJU7zoGV385RIpFO0krqdWABsTvhglE","AIzaSyAggqW0I_vt2hJ4usiVTFwO6c-fUkDtCPo"]
counter=0
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
youtube = None
videoslist=[]
userstosend=[] # (commentid,userid)
usersseen=[]
videolisttosend=[]
topcooments=[]
subcomments=[]
goodcom=[]
sent=[]
badwords=[]
channellist=[]


def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def print_response(response):
  print(response)

def build_resource(properties):
  resource = {}
  for p in properties:
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        ref[key] = {}
        ref = ref[key]
      else:
        ref = ref[key]
  return resource

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def comment_threads_insert(client, properties, **kwargs):
  resource = build_resource(properties)

  kwargs = remove_empty_kwargs(**kwargs)

  response = client.commentThreads().insert(
    body=resource,
    **kwargs
  ).execute()

  return print_response(response)

def scrape(keyword):
    url = 'https://www.youtube.com/results?q={}&sp=CAISAggBUBQ%253D'.format(keyword)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    f = open(r'data\links.txt', 'w')
    for link in soup.findAll('a', {'class': 'yt-uix-tile-link'}):
        href = link.get('href')
        newhref = href.replace("/watch?v=", "")
        f.write(newhref + '\n')

def choosetopcomment():
    rand=topcooments[math.floor(random()*len(topcooments))]
    rand=rand+"ובבקשה אל תראו את הסרטון בשבת הוא גם ככה יהיה נעול"
    rand=rand+"\n"


    rand=rand+"והנה משפט מעורר השראה להמשך היום: "

    rand=rand+sent[math.floor(random()*len(sent))]
    return str(rand)

def choosesubcomment():
    rand=subcomments[math.floor(random()*len(subcomments))]
    rand=rand+"ובבקשה אל תראה את הסרטון בשבת הוא גם ככה יהיה נעול"
    rand = rand + "\n"
   # rand = rand + " https://www.youtube.com/watch?v=wyFvmKNysXk הנה קישור אליו אם זה יותר נוח לכם :"
   # rand = rand + "\n"
    rand = rand +" אני יודע שהתגובה שלי לא ממש קשורה לתגובה שלכם אבל זה פעם אחרונה אני מפריע לכם"
    rand = rand + "\n"
    rand = rand + "והנה משפט מעורר השראה להמשך היום: "
    rand = rand + sent[math.floor(random() * len(sent))]

    return str(rand)


def CheckVideo(videoid):
  global videoslist
  try:
     videoslist.index(videoid)
     return False
  except :
    return True
def Checkcomm(comid,userid,commtext,likes,reply):
    global usersseen
    grade=20 +0.4*likes +8*reply
    try:
        i=usersseen.index(userid)
        return False
    except:
        if Checkifcomminlist(commtext.replace(" ","")):
            grade=70
        rand=random()*100
        if rand <= grade:
            print("grade: " +str(grade)+ " likes= "+str(likes)+" reply: "+ str(reply))
            return True

    return False

def Checkifcomminlist(comm):
    for good in goodcom:
        try:
            comm.index(good)
            return True
        except:
            t=5

    return False
def Checkifnameinlist(name):
    for bad in badwords:
        try:
            name.index(bad)
            return True
        except:
            t=5

    return False


def writeTofile(file,text):
     f= open(file,"a")
     f.write(text+"\n")
     f.close()

def getvideosId():
    global videoslist
    videofile= open("data\\videos.txt",'rb' )
    for  id in videofile.readlines():
        if id.rstrip().decode("utf-8") != "":
         videoslist.append(id.rstrip().decode("utf-8"))
    videofile.close()
def getchannellist():
    global channellist
    channelfile= open("data\\channels.txt",'rb' )
    for  id in channelfile.readlines():
        if id.rstrip().decode("utf-8") != "":
         channellist.append(id.rstrip().decode("utf-8"))
        channelfile.close()
    for i in range(len( channellist) - 1, 0, -1):
        # Pick a random index from 0 to i
        j = math.floor(random()*(i+1))

        # Swap arr[i] with the element at random index
        channellist[i],  channellist[j] =  channellist[j],  channellist[i]
def getUserseen():
    userfile = open("data\\users.txt", "r")
    for user in userfile.readlines():
        usersseen.append(user.replace("\n",""))
    userfile.close()
def getgoodcom():
    goodcomfile= open("data\\goodcom.txt",encoding="utf-8" )
    for com in goodcomfile.readlines():
        goodcom.append(com.rstrip())
    goodcomfile.close()
def getbadwords():
    badfile = open("data\\badwords.txt", encoding="utf-8")
    for com in badfile.readlines():
        badwords.append(com.rstrip())
        badfile.close()

def gettopcomments():
    commentfile = open("data\\topcomment2.txt", encoding="utf-8")
    for cooments in commentfile.readlines():
        topcooments.append(cooments)
    commentfile.close()
def getsubcomments():
    commentfile = open("data\\comments.txt", encoding="utf-8")
    for cooments in commentfile.readlines():

        subcomments.append(cooments)
    commentfile.close()
def getsent():
    senttfile = open("data\\sentenses.txt", encoding="utf-8")
    for s in senttfile.readlines():

        sent.append(s)
        senttfile.close()

def sendtopcomments():
    for vid in videolisttosend:
        if(CheckVideo(vid)):
         SendComment(vid,choosetopcomment())
def sendsubcomments(vidid):
     for com in userstosend:
         comid,userid= com
         SendSubComment(comid,choosesubcomment(),userid,vidid)




def getVideosfromChannel(channelId,pagetoken,videonum):
   numvideo=videonum
   videolisttosend=[]
   URL = "https://www.googleapis.com/youtube/v3/search?key="+API_KEYS[API_INDEX]+"&channelId="+channelId+"&part=snippet,id&order=date&maxResults=20&pageToken="+pagetoken
   # print(URL)
   try:
    with urllib.request.urlopen(URL) as response:
        html = response.read()
    jcode = json.loads(html.decode("UTF-8"))
    nextpagetoken=jcode["nextPageToken"]
   # print(jcode["items"][0]['id']["videoId"])
    for item in jcode["items"]:
        if item["id"]["kind"] == 'youtube#video':
             if(timediff(item["snippet"]["publishedAt"])>=24) and not  Checkifnameinlist(item["snippet"]["title"]) :
              videolisttosend.append(item['id']["videoId"])
              numvideo=numvideo+1

   except:
       return []
   if numvideo >=10:
       return videolisttosend
   else:
       return videolisttosend + getVideosfromChannel(channelId,nextpagetoken,numvideo)

def getcomfromvid(videoId,order):
   counterc=0
   commentlisttosend=[]
   URL = "https://www.googleapis.com/youtube/v3/commentThreads?key="+API_KEYS[API_INDEX]+"&textFormat=plainText&part=snippet&videoId="+videoId+"&maxResults=100&order="+order
   # print(URL)
   try:
    with urllib.request.urlopen(URL) as response:
        html = response.read()
    jcode = json.loads(html.decode("UTF-8"))
   # print(jcode["items"][0]['id']["videoId"])
    for item in jcode["items"]:
        if item["kind"] == 'youtube#commentThread':
           if (timediff(item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]) <= 144):
            if   Checkcomm(item['id'],item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"],item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],item["snippet"]["topLevelComment"]["snippet"]["likeCount"],item["snippet"]["totalReplyCount"]):

              commentlisttosend.append((item['id'],item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]))
              counterc=counterc+1
    if  order == "relevance":
        if counterc >0:
           #print ("the order is:"+ order)
           return commentlisttosend
        else:

            return getcomfromvid(videoId,"time")
    else:
        #print("the order is:" + order)
        return commentlisttosend


   except:
       print("comm diable")
       return []


def main():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()
    URL="https://www.googleapis.com/youtube/v3/search?key=AIzaSyAjhwEsEmyWJRXx5CDyRf0rld7CY08HO9Y&channelId=UC_HwfTAcjBESKZRJq6BTCpg&part=snippet,id&order=date&maxResults=20"

    with urllib.request.urlopen(URL) as response:
        html=response.read()
    jcode= json.loads(html.decode("UTF-8"))
    print (jcode["items"][0]['id']["videoId"])



def MakeYoutubeObj():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = CLIENT_SECRETS_FILES[CLIENT_SECRETS_INDEX]

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

def SendSubComment(parentID,Text,userId,vidid):
    global counter
    request = youtube.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": parentID,
                "textOriginal": Text
            }
        }
    )
    try:
     response = request.execute()
     st="Sent subcoment at https://www.youtube.com/watch?v="+vidid+"&lc="+parentID
     print(st)
     timer = random() * 3 +20
     time.sleep(timer)
     writeTofile("data\\users.txt", userId)
     usersseen.append(userId)
     counter=counter+1

    except:
        print("no good at " +parentID )

    return 0
def SendComment(videoid,text):

    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": videoid,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text
                    }
                }
            }
        }
    )
    try:
     response = request.execute()
     st="Sent topcomment to https://www.youtube.com/watch?v="+videoid
     print (st)
     writeTofile("data\\videos.txt", videoid)
     timer=random()*3 +20
     time.sleep(timer)
    except:
        print("comment are disable")
        return 0
    return response
def getData():
    getvideosId()
    gettopcomments()
    getgoodcom()
    getUserseen()
    getchannellist()
    getsubcomments()
    getbadwords()
    getsent()

def action():
    global  videolisttosend, userstosend ,counter
    for channel in channellist:
        videolisttosend = getVideosfromChannel(channel,'',0)
        for vid in videolisttosend:
            userstosend = getcomfromvid(vid,"relevance")
            sendsubcomments(vid)
            userstosend = []

        #sendtopcomments()
        videolisttosend = []
        if (counter>=50):
            break

def timediff(commtime):
    realtime=commtime.replace("T"," ")
    realtime = realtime.replace("Z","")
    nowtime= datetime.now()
    realtime=datetime.strptime( realtime, "%Y-%m-%d %H:%M:%S")
    diff=nowtime-realtime

    hours=diff.days*1440 +math.floor(diff.seconds/3600)
    return hours


def main2():

     global  youtube , videolisttosend ,userstosend
     youtube = MakeYoutubeObj()
     getData()

     #print(subcomments)
     while (counter <50):
       action()
       print("bot sent " + str(counter))
       timer = random() *300 + 600
       time.sleep(timer)
    # print(usersseen)
     print("bot sent " +str(counter))






    # videolisttosend=getVideosfromChannel('UCeDXtizFv7cvAcpvmVpnMKg')

    #https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDpHJU7zoGV385RIpFO0krqdWABsTvhglE&textFormat=plainText&part=snippet&videoId=gb5tCBGpPyo&maxResults=100
    #time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
     #sendtopcomments()
     #print(getcomfromvid("j-3Kp97xN20"))



if __name__ == '__main__':
  main2()


def stam():
 with open(r'data\comments.txt', 'r') as f:
    foo = [line.strip() for line in f]

# keyword
 with open(r'data\keywords.txt', 'r') as f:
    foooo = [line.strip() for line in f]

 keywords = open(r'data\keywords.txt', 'r')
 x = 10
 while x < 20:
    for line in keywords:
        scrape(line)

        with open(r"data\links.txt", 'r+') as f:
            f.readline()
            data = f.read()
            f.seek(0)
            f.write(data)
            f.truncate()

            try:
                with open(r'data\links.txt', 'r') as f:
                    urls = []
                    for url in f:
                        rand = random.choice(foo)

                        comment_threads_insert(client,
                        {'snippet.channelId': 'UCNlM-pgjmd0NNE5I6MzlEGg',
                         'snippet.videoId': url,
                         'snippet.topLevelComment.snippet.textOriginal': rand},
                        part='snippet')
            except:
                pass
            print("Searching for video based in your keywords...")
