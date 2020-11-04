"""
Написать код, который сможет:
1.  Получить текст последних 20 постов со стены какого-то сообщества вк
* у каждого поста есть id, записывайте его куда-нибудь
* сохранить текст каждого поста в текстовый документ в папке, название которой совпадает с именем сообщества
2. После этого получить текст комментов к каждому посту
* сохранить текст каждого коммента по пути id_поста/id_коммента.txt
3. Сложить это все в архив и отправить вам в телеграме
"""

import requests
import os
import tarfile


def get_access_token(filename):
    with open(filename) as f:
        return f.readline()


def get_posts(access_token, community):
    return requests.get("https://api.vk.com/method/wall.get", {
        "domain": community,
        "access_token": access_token,
        "v": "5.92"
    }).json()["response"]["items"]


def get_post_comments(access_token, owner_id, post_id):
    return requests.get("https://api.vk.com/method/wall.getComments", {
        "owner_id": owner_id,
        "post_id": post_id,
        "access_token": access_token,
        "v": "5.92"
    }).json()["response"]["items"]


def download_vk_info(communityId):
    access_token = get_access_token("access_token.txt")

    posts = get_posts(access_token, communityId)[:20]

    for post in posts:
        try:
            os.makedirs("%s/%s" % (communityId, post["id"]))
        except:
            pass

        post_file = open("%s/%s.txt" % (communityId, post["id"]), "w+")
        post_file.write(post["text"])
        post_file.flush()
        post_file.close()

        comments = get_post_comments(access_token, post["owner_id"], post["id"])
        for comment in comments:
            comment_file = open("%s/%s/%s.txt" % (communityId, post["id"], comment["id"]), "w+")
            comment_file.write(comment["text"])
            comment_file.flush()
            comment_file.close()

    tar = tarfile.open("%s.tar.gz" % (communityId), "w:gz")
    tar.add("%s/" % (communityId), arcname=communityId)
    tar.close()

    os.system("telegram-send --config channel.conf --caption 'VK community %s info' --file %s.tar.gz" % (communityId, communityId))


download_vk_info("thevillage")