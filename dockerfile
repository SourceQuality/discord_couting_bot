FROM python:3
ADD requirements.txt /
RUN pip3 install -r requirements.txt
RUN mkdir /data
ADD counter_bot.py /data
CMD ["python", "./counter_bot.py"]
