# 도커파일에는 지금까지 진행한 로컬환경과 동일한 컨테이너 이미지 만들기 위해 지정할 내용 작성

# 파이썬이 설치되어 있는 이미지를 기본으로 제공. 이 이미지 불러오기
FROM python:3.10.8-slim-buster

# 프로젝트 작업 폴더 지정
WORKDIR /usr/src/app
# 파이썬이 소스 코드 컴파일시 생성하는 .pyc파일 생성 않도록 지정
ENV PYTHONDONTWRITEBYCODE 1
# 파이썬 로그가 버퍼링 없이 즉각 출력
ENV PYTHONUNBUFFERED 1

# . :현재 폴더 , /usr/src/app/ : 작업폴더   , 이렇게 복사한다
COPY . /usr/src/app/

# requirements.txt에 나열된 라이브러리 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


