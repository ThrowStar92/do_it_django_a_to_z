from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
class TestView(TestCase):
    def setUp(self):           # setUp :테스트가 시작되기 전의 사항은 준비하는것(가상 고객 준비)
        self.client = Client()


    def test_post_list(self):
        #1.1. 포스트 목록 페이지 가져온다.
        response = self.client.get('/blog/')
        # 1.2. 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)   # 응답코드가 200으로 정상인가?
        # 1.3. 페이지 타이틀을 'Blog'이다
        soup = BeautifulSoup(response.content, 'html.parser') #응답내용을 파싱
        self.assertEqual(soup.title.text, 'Blog') # 파싱된 정보에서 Blog라는 단어가 있는지 확인
        # 1.4. 내비게이션 바가있다.
        navbar = soup.nav
        # 1.5. Blog,About Me 라는 문구가 내비게이션 바에 있다.
        self.assertIn('Blog', navbar.text)           # Blog,About Me 있는지 확인
        self.assertIn('About Me', navbar.text)

        # 2.1. 포스트(게시물)가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2. main area에 '아직 게시물이 없습니다'라는 문구가 나타난다.
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다', main_area.text)   # main_area.text에 아직 게시물이 없습니다가 있나?
        # 여기서 에러난다 (아직 게시물이 없습니다 << 이거 없어)
        # 그동안 id= "main-area" 가 없었다  > main_area = none 상태




        # 3.1. 포스트가 2개 있다면
        post_001 = Post.objects.create(       # 게시물 2개 추가
            title= '첫 번째 포스트입니다.',
            content='Hello World. We are the world',
        )

        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '1등이 전부는 아니잖아요?',
        )

        self.assertEqual(Post.objects.count(), 2)

        # 3.2. 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3. main area에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4. '아직 게시물이 없습니다'라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)