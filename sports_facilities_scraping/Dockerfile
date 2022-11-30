FROM python:3
USER root

RUN mkdir -p /root/src
COPY src /root/src
WORKDIR /root/src

RUN pip install schedule
RUN pip install requests
RUN pip install selenium

CMD ["python","-u","check_availability.py"]