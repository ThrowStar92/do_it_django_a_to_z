from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag

class TestView(TestCase):
    def setUp(self):           # setUp :테스트가 시작되기 전의 사항은 준비하는것(가상 고객 준비)
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',
        password = 'somepassword')
        self.user_obama = User.objects.create_user(username='obama',
        password = 'somepassword')
        self.user_obama.is_staff = True
        self.user_obama.save()


        self.category_programming = Category.objects.create(name='programming',slug='programming')
        self.category_music = Category.objects.create(name='music',slug='music')

        self.tag_python_kor = Tag.objects.create(name = "파이썬 공부", slug = "파이썬-공부")
        self.tag_python = Tag.objects.create(name="python", slug="python")
        self.tag_hello = Tag.objects.create(name="hello", slug="hello")

        self.post_001 = Post.objects.create(
            title= '첫번째 포스트입니다.',
            content = 'Hello World. We are the world',
            category= self.category_programming,
            author = self.user_trump
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama
        )
        self.post_003 = Post.objects.create(
            title='세번째 포스트입니다.',
            content='카테고리 없는 컨텐츠!',
            author=self.user_obama
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())  #hello테그에 해당하는 곳에 들어가 루트를 요청한다.
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # 페이지 소스코드 확인

        self.navbar_test(soup)              #nav, category 정상인지 확인
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div',id= 'main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title,main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div',id= 'main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title,main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog',navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Future')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self,soup):
        categries_card= soup.find('div', id = 'categories-card')
        self.assertIn('Categories',categries_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categries_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categries_card.text)
        self.assertIn(f'미분류 (1)', categries_card.text)

    def test_post_list(self):
        # #1.1. 포스트 목록 페이지 가져온다.
        # response = self.client.get('/blog/')
        # # 1.2. 정상적으로 페이지가 로드된다.
        # self.assertEqual(response.status_code, 200)   # 응답코드가 200으로 정상인가?
        # # 1.3. 페이지 타이틀을 'Blog'이다
        # soup = BeautifulSoup(response.content, 'html.parser') #응답내용을 파싱
        # self.assertEqual(soup.title.text, 'Blog') # 파싱된 정보에서 Blog라는 단어가 있는지 확인
        # # 1.4. 내비게이션 바가있다.
        #
        # # navbar = soup.nav
        # # # 1.5. Blog,About Me 라는 문구가 내비게이션 바에 있다.
        # # self.assertIn('Blog', navbar.text)           # Blog,About Me 있는지 확인
        # # self.assertIn('About Me', navbar.text)
        # self.navbar_test(soup)  #호출, soup 제공
        #
        #
        # # 2.1. 포스트(게시물)가 하나도 없다면
        # self.assertEqual(Post.objects.count(), 0)
        # # 2.2. main area에 '아직 게시물이 없습니다'라는 문구가 나타난다.
        # main_area = soup.find('div', id="main-area")
        # self.assertIn('아직 게시물이 없습니다', main_area.text)   # main_area.text에 아직 게시물이 없습니다가 있나?
        # # 여기서 에러난다 (아직 게시물이 없습니다 << 이거 없어)
        # # 그동안 id= "main-area" 가 없었다  > main_area = none 상태
        #
        #
        #
        #
        # # 3.1. 포스트가 2개 있다면
        # post_001 = Post.objects.create(       # 게시물 2개 추가
        #     title= '첫 번째 포스트입니다.',
        #     content='Hello World. We are the world',
        #     author=self.user_trump
        # )
        #
        # post_002 = Post.objects.create(
        #     title = '두 번째 포스트입니다.',
        #     content = '1등이 전부는 아니잖아요?',
        #     author=self.user_obama
        #
        # )
        #
        # self.assertEqual(Post.objects.count(), 2)
        #
        # # 3.2. 포스트 목록 페이지를 새로고침했을 때
        # response = self.client.get('/blog/')
        # soup = BeautifulSoup(response.content, 'html.parser')
        # self.assertEqual(response.status_code, 200)
        # # 3.3. main area에 포스트 2개의 제목이 존재한다.
        # main_area = soup.find('div', id='main-area')
        # self.assertIn(post_001.title, main_area.text)
        # self.assertIn(post_002.title, main_area.text)
        # # 3.4. '아직 게시물이 없습니다'라는 문구는 더 이상 나타나지 않는다.
        # self.assertNotIn('아직 게시물이 없습니다', main_area.text)
        #
        # self.assertIn(self.user_trump.username.upper(), main_area.text)
        # self.assertIn(self.user_obama.username.upper(), main_area.text)

        #포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id ='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id = 'post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        #포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        # 1.1. Post가 하나 있다. - 제거



        #1.2 그 포스트의 url은 'blog/1/' 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # .2.1. 첫 번째 post url로 접근하면 정상적으로 작동한다(status code:200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2.포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        # navbar = soup.nav
        # self.assertIn('Blog',navbar.text)
        # self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)
        self.category_card_test(soup)
        # 2.3. 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4. 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div',id= 'main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name,post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.5. 첫번째 포스트의 작성자(author)가 포스트 영역에 있다.
        #아직 작성 불가

        # 2.6. 첫번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content,post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)



    def test_create_post(self):

        # 로그인 하지 않으면 status code가 200이면 안된다.
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        #로그인 한다.
        self.client.login(username='obama', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text )
        main_area = soup.find('div', id ='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id ='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': "Post Form 페이지 만듭시다.",
                'tags_str': 'new tag; 한글 태그, python'
            }
        )
        self.assertEqual(Post.objects.count(),4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title,"Post Form 만들기")
        self.assertEqual(last_post.author.username,'obama')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        #로그인 x
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code,200)

        #로그인, 작성자x
        self.assertNotEqual(self.post_003.author,self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password = 'somepassword'
        )
        response=self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        #작성자 접근
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post',main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title' : '세번째 포스트를 수정했습니다.',
                'content' : '안녕 세계? 우리는 하나!',
                'category': self.category_music.pk,
                'tags_str': '파이썬 공부; 한글 태그, some tag'

            },
            follow=True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id ='main-area')
        self.assertIn('세번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)













