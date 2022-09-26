FROM python:3.7

RUN mkdir /PyMixx
COPY . /PyMixx
WORKDIR /PyMixx
RUN ls
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py","config.json" ]