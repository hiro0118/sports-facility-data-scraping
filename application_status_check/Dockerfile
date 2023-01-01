FROM python:3.9-alpine
USER root

RUN apk add --no-cache tzdata
ENV TZ=Asia/Tokyo

RUN pip install schedule
RUN pip install requests
RUN pip install selenium

RUN mkdir -p /root/src
COPY src /root/src
WORKDIR /root/src

CMD ["python","-u","main.py"]