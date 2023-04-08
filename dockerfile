FROM python:3
ADD requirements.txt /
run pip3 install -r requirements.txt
add counter_bot.py /
CMD ["python", "./counter_bot.py"]
