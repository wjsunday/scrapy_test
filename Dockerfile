FROM python:3.6.8
MAINTAINER zepinglai "zezecn@163.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN groupadd www -g 500 && useradd -s /sbin/nologin -g www www -u 500
USER www
CMD ["/bin/bash","run.sh"]