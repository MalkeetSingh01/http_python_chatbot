

import threading

import requests

import json

import time



URL='http://127.0.0.1:8000'


cached_error=""




# URL='127.0.0.1:8000'



def get_message(user,friend):

    param={

        'param1':user,

        'param2':friend

    }

    while True:

        res=requests.get(URL+"/message",params=param)

        # print(res.status_code)

        time.sleep(1)

        # if res.text :print(res.text)

        if res.text!="" and cached_error!=res.text:

          print("[{}]-{}".format(friend,res.text))

          cached_error=res.text

        else: cached_error=res.text

        # print(res.text)



def post_message(user,friend,message):

    payload={

        "user":user,

        "friend":friend,

        "message":message

    }

    # print(payload)

    res=requests.post(URL,data=json.dumps(payload))

    return res.status_code



def chat():

    user=input("Enter user: ")

    friend=input("Enter friend: ")

    t=threading.Thread(target=get_message,args=(user,friend))

    t.start()

    res=200

    while True and res==200:

        time.sleep(1)

        # message=input("[{}]-".format(user))

        message=input()
        res=post_message(user,friend,message)

    t.join()



if __name__ == '__main__':

    chat()