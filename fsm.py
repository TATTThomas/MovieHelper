from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message, send_movie_details, send_actor_details, send_series_details

from tmdbv3api import TMDb
from tmdbv3api import Movie, Person,  TV
tmdb = TMDb()
tmdb.api_key = 'f307d56f424dae1f5d31e23e0b78ee09'
tmdb.language = 'zh-TW'
noinfo = '抱歉餒~ 暫時沒有資料'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_chose_list(self, event):
        text = event.message.text
        return text.lower() == "熱門清單"

    def is_going_to_search(self, event):
        text = event.message.text
        return text.lower() == "搜尋"

    def is_going_to_popular_movies(self, event):
        text = event.message.text
        return text.lower() == "熱門電影"

    def is_going_to_popular_series(self, event):
        text = event.message.text
        return text.lower() == "熱門影集"

    def is_going_to_search_movie(self, event):
        text = event.message.text
        return text.lower() == "電影"

    def is_going_to_search_actor(self, event):
        text = event.message.text
        return text.lower() == "演員"

    def is_going_to_search_series(self, event):
        text = event.message.text
        return text.lower() == "影集"

    def is_going_to_movie_details(self, event):
        text = event.message.text
        movie = Movie()
        try:
            movie.details(int(text))
            return True
        except:
            return False

    def is_going_to_actor_details(self, event):
        text = event.message.text
        person = Person()
        try:
            person.details(int(text))
            return True
        except:
            return False

    def is_going_to_series_details(self, event):
        text = event.message.text
        tv = TV()
        try:
            tv.details(int(text))
            return True
        except:
            return False

    def is_going_to_popular_actor(self, event):
        text = event.message.text
        return text.lower() == "熱門演員"

    def is_going_to_movie_result(self, event):
        text = event.message.text
        movie = Movie()
        search = movie.search(text)
        if len(search) == 0:
            return False
        else:
            return True

    def is_going_to_actor_result(self, event):
        text = event.message.text
        person = Person()
        search = person.search(text)
        if len(search) == 0:
            return False
        else:
            return True

    def is_going_to_series_result(self, event):
        text = event.message.text
        tv = TV()
        search = tv.search(text)
        if len(search) == 0:
            return False
        else:
            return True

    def on_enter_search(self, event):
        print("I'm entering search list")
        reply_token = event.reply_token
        title = '搜尋項目'
        instro = '選擇想要搜尋的項目'
        labels = ['電影', '演員', '影集']
        texts = ['電影', '演員', '影集']
        img = 'https://pbs.twimg.com/profile_images/1243623122089041920/gVZIvphd_400x400.jpg'
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_movie_result(self, event):
        print("I'm entering movie result")
        text = event.message.text
        reply_token = event.reply_token
        title = '電影'
        instro = '搜尋結果'
        labels = []
        texts = []
        movie = Movie()
        search = movie.search(text)
        img = 'https://image.tmdb.org/t/p/w780/' + str(search[0].backdrop_path)
        lenth = len(search)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(search[i].title) > 20:
                title = search[i].title[0:15] + '...' 
                labels.append(title)
            else:
                labels.append(search[i].title)
            texts.append(search[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_actor_result(self, event):
        print("I'm entering actor result")
        text = event.message.text
        reply_token = event.reply_token
        title = '演員'
        instro = '搜尋結果'
        labels = []
        texts = []
        person = Person()
        search = person.search(text)
        img = 'https://image.tmdb.org/t/p/w780/' + str(search[0].profile_path)
        lenth = len(search)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(search[i].name) > 20:
                name = search[i].name[0:15] + '...' 
                labels.append(name)
            else:
                labels.append(search[i].name)
            texts.append(search[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_series_result(self, event):
        print("I'm entering series result")
        text = event.message.text
        reply_token = event.reply_token
        title = '影集'
        instro = '搜尋結果'
        labels = []
        texts = []
        tv = TV()
        search = tv.search(text)
        img = 'https://image.tmdb.org/t/p/w780/' + str(search[0].backdrop_path)
        lenth = len(search)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(search[i].name) > 20:
                name = search[i].name[0:15] + '...' 
                labels.append(name)
            else:
                labels.append(search[i].name)
            texts.append(search[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_search_movie(self, event):
        print("I'm entering search movie")
        reply_token = event.reply_token
        send_text_message(reply_token, '請輸入想要搜尋的電影關鍵字!')

    def on_enter_search_actor(self, event):
        print("I'm entering search actor")
        reply_token = event.reply_token
        send_text_message(reply_token, '請輸入想要搜尋的演員關鍵字!')

    def on_enter_search_series(self, event):
        print("I'm entering search series")
        reply_token = event.reply_token
        send_text_message(reply_token, '請輸入想要搜尋的影集關鍵字!')

    def on_enter_chose_list(self, event):
        print("I'm entering choose list")
        reply_token = event.reply_token
        title = '今日熱門'
        instro = '選擇想要的查看的熱門項目'
        labels = ['今日熱門電影', '今日熱門演員', '今日熱門影集']
        texts = ['熱門電影', '熱門演員', '熱門影集']
        img = 'https://pbs.twimg.com/profile_images/1243623122089041920/gVZIvphd_400x400.jpg'
        send_button_message(reply_token, title, instro, labels, texts, img)


    def on_enter_popular_movies(self, event):
        print("I'm entering popular movies")
        reply_token = event.reply_token
        title = '熱門電影'
        instro = '今日最熱門電影 Top4'
        labels = []
        texts = []
        movie = Movie()
        popular = movie.popular()
        img = 'https://image.tmdb.org/t/p/w780/' + str(popular[0].backdrop_path)
        lenth = len(popular)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(popular[i].title) > 20:
                title = popular[i].title[0:15] + '...' 
                labels.append(title)
            else:
                labels.append(popular[i].title)
            texts.append(popular[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_popular_actor(self, event):
        print("I'm entering popular actors")
        reply_token = event.reply_token
        title = '熱門演員'
        instro = '今日最熱門演員 Top4'
        labels = []
        texts = []
        person = Person()
        popular = person.popular()
        img = 'https://image.tmdb.org/t/p/w780/' + str(popular[0].profile_path)
        lenth = len(popular)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(popular[i].name) > 20:
                name = popular[i].name[0:15] + '...' 
                labels.append(name)
            else:
                labels.append(popular[i].name)
            texts.append(popular[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_popular_series(self, event):
        print("I'm entering popular series")
        reply_token = event.reply_token
        title = '熱門影集'
        instro = '今日最熱門影集 Top4'
        labels = []
        texts = []
        tv = TV()
        popular = tv.popular()
        img = 'https://image.tmdb.org/t/p/w780/' + str(popular[0].poster_path)
        lenth = len(popular)
        for i in range(0, 4):
            #print(popular[i].title)
            if len(popular[i].name) > 20:
                name = popular[i].name[0:15] + '...' 
                labels.append(name)
            else:
                labels.append(popular[i].name)
            texts.append(popular[i].id)

            if i == lenth - 1:
                break
        send_button_message(reply_token, title, instro, labels, texts, img)

    def on_enter_movie_details(self, event):
        print("I'm entering movie detail")
        reply_token = event.reply_token
        movie = Movie()
        m = movie.details(int(event.message.text))
        title = '電影 : ' + m.title
        if m.overview == '':
            overview = '劇情簡介 :\n' + noinfo
        else:
            overview = '劇情簡介 :\n' + m.overview
        release_date = '上映日期 : ' + m.release_date
        score = '評分 : ' + str(round(m.vote_average, 1))
        img = 'https://image.tmdb.org/t/p/w780/' + str(m.poster_path)
        send_movie_details(reply_token ,title, overview, release_date, score, img)
        #self.go_back()

    def on_enter_actor_details(self, event):
        print("I'm entering actor detail")
        reply_token = event.reply_token
        person = Person()
        p = person.details(int(event.message.text))
        name = '姓名 : ' + p.name
        if p.biography == '':
            overview = '演員介紹 :\n' + noinfo
        else:
            overview = '演員介紹 :\n' + p.biography
        popularity = '人氣 : ' + str(int(p.popularity))
        img = 'https://image.tmdb.org/t/p/w780/' + str(p.profile_path)
        send_actor_details(reply_token , name, overview, popularity, img)
        #self.go_back()

    def on_enter_series_details(self, event):
        print("I'm entering series detail")
        reply_token = event.reply_token
        tv = TV()
        t = tv.details(int(event.message.text))
        name = '劇名 : ' + t.name
        if t.overview == '':
            overview = '劇情大綱 :\n' + noinfo
        else:
            overview = '劇情大綱 :\n' + t.overview
        score = '評分 : ' + str(round(t.vote_average, 1))
        eposide = '季數 : ' + str(t.number_of_seasons) + '\n' + '總集數 : ' + str(t.number_of_episodes) + '\n' + '目前狀態 : ' + t.status
        img = 'https://image.tmdb.org/t/p/w780/' + str(t.poster_path)
        send_series_details(reply_token , name, overview, score, eposide, img)
        #self.go_back()