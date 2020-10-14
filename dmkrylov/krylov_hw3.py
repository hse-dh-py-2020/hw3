group_id='-162456019' #id паблика "мальчик онфим устал"
import os
import requests
import re

TOKEN = "293229b6293229b6293229b64c29467cba22932293229b676b2da9f5a69a03e78526db1"
data = requests.get( #в эту переменную запоминается словарь, в котором хранятся данные о последних двадцати пастах МОУ, не считая закрепленного
	'https://api.vk.com/method/wall.get',
	params = {
	'owner_id':group_id,
	'count':'20',
	'offset':'1',
	'screen_name':'onfimustal',
	'v':'5.92',
	'access_token':TOKEN}
	).json()
for i in range(20):
	post_id = data['response']['items'][i]['id'] #запоминаем id поста
	post_text = data['response']['items'][i]['text'] #запоминаем текст поста
	try:
		os.makedirs('C:\\Users\\Arseny\\Desktop\\repository\\hw3\\onfimustal\\'+str(post_id)) 
	except: #создаем папку, названием которой является id поста
		pass #если она создана, ничего не делаем
	with open("C:\\Users\\Arseny\\Desktop\\repository\\hw3\\onfimustal\\"+str(post_id)+"\\" + str(post_id) + ".txt",'w',encoding='utf8') as file:
		file.write(post_text) #в файл с таким же названием пишем текст поста
	comment = requests.get( #получаем данные о комментах к этому посту
	'https://api.vk.com/method/wall.getComments',
	params = {
	'owner_id':group_id,
	'post_id':post_id,
	'offset':'0',
	'screen_name':'onfimustal',
	'v':'5.92',
	'access_token':TOKEN,
	'extended':'1',
	'thread_items_count':'10' #из каждого треда достаем не более 10 ответов к комменту
	}
	).json()['response']['items']
	if len(comment)>0: #если вообще есть хоть один коммент к посту,
		with open ("C:\\Users\\Arseny\\Desktop\\repository\\hw3\\onfimustal\\"+str(post_id)+"\\" + str(comment[0]['id']) + ".txt",'w',encoding='utf8') as file2:
			file2.write(comment[0]['text']) #то записываем этот коммент в той же папке в файл, названием которого является id коммента
		if comment[0]['thread']['count']!='0': #если на коммент хоть кто-нибудь ответил,
			for i in range (len(comment[0]['thread']['items'])):#то для каждого ответа...
				with open ("C:\\Users\\Arseny\\Desktop\\repository\\hw3\\onfimustal\\"+str(post_id)+"\\" + str(comment[0]['thread']['items'][i]['id']) + ".txt",'w',encoding='utf8') as file3:
					file3.write(comment[0]['thread']['items'][i]['text'])#пишем этот ответв той же папке в файл, названием которого является id ответа
	#print(comment)



