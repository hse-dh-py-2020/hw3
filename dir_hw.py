import os
import requests


TOKEN = "c0633979c0633979c063397944c0176728cc063c06339799fe76c58c10b77924a0cceff"
data = requests.get(
    'https://api.vk.com/method/wall.get', 
    params={
        "owner_id": -72326580,
        "v":"5.94",
        "count":20,
        "access_token": TOKEN
    }
).json()



for post in data["response"]["items"]:
    post_id = post["id"]
    texts = post["text"]
    data3 = requests.get(
        'https://api.vk.com/method/wall.getComments', 
            params={
            "owner_id": -72326580,
            "post_id": post_id,
            "v":"5.92",
            "access_token": TOKEN
        }
    ).json()
    
    try:
        os.makedirs("ussrchaosss\\"+str(post_id))
    except:
        pass

    for comment in data3["response"]["items"]:
        with open("ussrchaosss\\"+str(post_id)+"\\"+str(comment["id"])+".txt", "w", encoding="UTF-8") as text_file:
            text_file.write(comment["text"])
    
os.system("tar -a -c -f VK_posts.zip ussrchaosss")
os.system('telegram-send --config channel.conf --file VK_posts.zip --caption "вот тебе папки"')
    