FROM python:3.9
WORKDIR /app
ADD . /app
RUN pip install Flask
EXPOSE 8000
CMD ["python", "app.py"]
