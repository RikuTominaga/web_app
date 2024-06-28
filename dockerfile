FROM python:3.9
WORKDIR /app
ADD . /app
RUN pip install Flask
RUN pip install huggingface_hub
RUN pip install langchain
RUN pip install sentence_transformers
RUN pip install webdriver_manager
RUN pip install selenium
RUN pip install -U langchain-community
EXPOSE 8000
CMD ["python", "app.py"]
