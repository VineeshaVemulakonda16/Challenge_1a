FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install PyPDF2 pycryptodome

CMD ["python", "process_pdfs.py"]
