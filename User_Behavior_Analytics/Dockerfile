FROM python:3.14.7-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the project into the image
COPY . /code/

#CMD ["ls"]
CMD ["/venv/bin/python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
