FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code/

ENV PYTHONPATH="${PYTHONPATH}:/code"

# Set the command to run the ASGI server using uvicorn
CMD ["uvicorn", "cp_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
