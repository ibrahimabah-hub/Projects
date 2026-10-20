FROM python:3.13-slim

WORKDIR /code

COPY requirements.txt .


RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the project into the image
COPY . .

#CMD ["ls"]
CMD ["/venv/bin/python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
