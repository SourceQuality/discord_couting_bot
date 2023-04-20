FROM python:3
ADD requirements.txt /
RUN mkdir -p /config
RUN pip3 install -r requirements.txt
ADD counter_bot.py /
CMD ["python", "/counter_bot.py"]
