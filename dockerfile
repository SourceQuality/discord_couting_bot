FROM python:3
ADD requirements.txt /
RUN mkdir -p /data
RUN pip3 install -r requirements.txt
ADD counter_bot.py /data
CMD ["python", "/data/counter_bot.py"]
