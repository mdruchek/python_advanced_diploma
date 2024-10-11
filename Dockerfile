FROM python:3.10-alpine
WORKDIR /code
COPY requirements/ requirements/
RUN pip install -r requirements/production.txt
COPY src/blogs_app/ blogs_app/
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "blogs_app:create_app()"]