FROM python:3.7

MAINTAINER ZHJ0125 <zhanghoujin123 AT gmail DOT COM>

WORKDIR /Projects/bushu

ENV PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production

COPY ./app .
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8103

COPY gunicorn.conf.py .

CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]
