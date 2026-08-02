FROM python:3.13.14-alpine3.24
RUN addgroup app && adduser -S -G app app
WORKDIR /app/
RUN chown app:app /app/
USER app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
