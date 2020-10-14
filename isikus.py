import json
import requests
import re
import os
import shutil
import sys
import telegram_send

from os import listdir, mkdir, chdir, sep

from credentials import Token


def get_posts(token, public_id, offset=0, count_total=20, include_comments=True, clean_links=False, verbose=False):
    Total = 0
    fTotal = count_total
    try:
        public_id = abs(int(public_id))
    except ValueError:
        pass
    
    response = requests.get("https://api.vk.com/method/groups.getById?v=5.124&group_id=%s&access_token=%s" % (str(public_id), token))
    public_name = json.loads(response.text)["response"][0]["name"]
    public_id = json.loads(response.text)["response"][0]["id"] * (-1)
    
    mkdir(public_name)
    chdir(public_name)
    
    while (count_total // 100):
        Succeed = False
        while (not Succeed):
            response = requests.get("https://api.vk.com/method/wall.get?v=5.69&owner_id=%s&offset=%s&count=%s&access_token=%s" % (public_id, str(offset), '100', token))
            if verbose:
                print("Loaded https://api.vk.com/method/wall.get?v=5.69&owner_id=%s&offset=%s&count=%s&access_token=%s" % (public_id, str(offset), '100', token))
            json_string = response.text
            current_request = json.loads(json_string)
            try:
                current_request['response']
                Succeed = True
            except:
                print('Failed to get request, resending')
                Succeed = False
        for item in current_request['response']["items"]:
            try:
                text = item['text']
                if clean_links:
                    text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
                text = re.sub(r'\<.*?\>',' ',text)
                with open(str(item['id'])+".txt", "w") as outtxt:
                    outtxt.write(text)
                Total += 1
                if verbose:
                    print("Processing item %s with id %s. %s to go" % (str(Total), str(item['id']), str(fTotal-Total)))
                if include_comments:
                    mkdir(str(item['id']))
                    current_post_comments = []
                    comments_count = item['comments']['count']
                    while (comments_count // 100):
                        Succeed = False
                        while (not Succeed):
                            response = requests.get("https://api.vk.com/method/wall.getComments?v=5.69&owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s" % (public_id, str(item['id']), token))
                            json_string = response.text
                            current_request = json.loads(json_string)
                            try:
                                current_request['response']
                                Succeed = True
                            except:
                                print('Failed to get request for COMMENTS, resending')
                                Succeed = False
                        for comment in current_request['response']["items"]:
                            try:
                                text = comment['text']
                                if clean_links:
                                    text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
                                text = re.sub(r'\<.*?\>',' ',text)
                                with open(os.path.join(str(item['id']), str(comment['id'])+".txt"), "w") as outtxt:
                                    outtxt.write(text)
                            except:
                                print('Exception caught while processing comments')
                        comments_count -= 100
                    Succeed = False
                    while (not Succeed):
                        response = requests.get("https://api.vk.com/method/wall.getComments?v=5.69&owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s" % (public_id, str(item['id']), token))
                        json_string = response.text
                        current_request = json.loads(json_string)
                        try:
                            current_request['response']
                            Succeed = True
                        except:
                            print('Failed to get request for COMMENTS, resending')
                            Succeed = False
                    for comment in current_request['response']["items"]:
                        try:
                            text = comment['text']
                            if clean_links:
                                text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
                            text = re.sub(r'\<.*?\>',' ',text)
                            with open(os.path.join(str(item['id']), str(comment['id'])+".txt"), "w") as outtxt:
                                outtxt.write(text)
                        except:
                            print('Exception caught while processing comments')
            except Exception as e:
                print(str(e)+' happened while processing posts')
        offset -= 100
        count_total -= 100
    Succeed = False
    while (not Succeed):
        response = requests.get("https://api.vk.com/method/wall.get?v=5.69&owner_id=%s&offset=%s&count=%s&access_token=%s" % (public_id, str(offset), str(count_total), token))
        if verbose:
            print("Loaded https://api.vk.com/method/wall.get?v=5.69&owner_id=%s&offset=%s&count=%s&access_token=%s" % (public_id, str(offset), str(count_total), token))
        json_string = response.text
        current_request = json.loads(json_string)
        try:
            current_request['response']
            Succeed = True
        except:
            print('Failed to get request, resending')
            Succeed = False
    for item in current_request['response']["items"]:
        try:
            text = item['text']
            if clean_links:
                text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
            with open(str(item['id'])+".txt", "w") as outtxt:
                outtxt.write(text)
            Total += 1
            if verbose:
                print("Processing item %s with id %s. %s to go" % (str(Total), str(item['id']), str(fTotal-Total)))
            if include_comments:
                mkdir(str(item['id']))
                current_post_comments = []
                comments_count = item['comments']['count']
                while (comments_count // 100):
                    Succeed = False
                    while (not Succeed):
                        response = requests.get("https://api.vk.com/method/wall.getComments?v=5.69&owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s" % (public_id, str(item['id']), token))
                        json_string = response.text
                        current_request = json.loads(json_string)
                        try:
                            current_request['response']
                            Succeed = True
                        except:
                            print('Failed to get request for COMMENTS, resending')
                            Succeed = False
                    for comment in current_request['response']["items"]:
                        try:
                            text = comment['text']
                            if clean_links:
                                text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
                            text = re.sub(r'\<.*?\>',' ',text)
                            with open(os.path.join(str(item['id']), str(comment['id'])+".txt"), "w") as outtxt:
                                outtxt.write(text)
                        except:
                            print('Exception caught while processing comments')
                    comments_count -= 100
                Succeed = False
                while (not Succeed):
                    response = requests.get("https://api.vk.com/method/wall.getComments?v=5.69&owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s" % (public_id, str(item['id']), token))
                    json_string = response.text
                    current_request = json.loads(json_string)
                    try:
                        current_request['response']
                        Succeed = True
                    except:
                        print('Failed to get request for COMMENTS, resending')
                        Succeed = False
                for comment in current_request['response']["items"]:
                    try:
                        text = comment['text']
                        if clean_links:
                            text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
                        text = re.sub(r'\<.*?\>',' ',text)
                        with open(os.path.join(str(item['id']), str(comment['id'])+".txt"), "w") as outtxt:
                            outtxt.write(text)
                    except:
                        print('Exception caught while processing comments')
        except Exception as e:
            print(str(e)+' happened while processing posts')
    
    chdir("../")
    return public_name

def main(public_id="oldlentach"):
    """
    Usage: python main.py <public_id>
    
    public_id (str): the id or short url of the desired vk public to get
    """
    name = get_posts(Token, sys.argv[1])
    shutil.make_archive(name, 'zip', name)
    telegram_send.send(files=[open(name+".zip", "rb")], captions=["Archived 20 posts for "+name], conf="channel.conf")

if __name__ == "__main__":
    main()
