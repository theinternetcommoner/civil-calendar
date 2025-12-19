FROM python:3.13-alpine AS builder
WORKDIR /calendar
COPY ./ ./
RUN pip install -r requirements.txt

FROM python:3.13-alpine AS final
COPY --from=builder ./calendar ./calendar

WORKDIR /calendar
RUN pip install -r requirements.txt
EXPOSE 5050

CMD ["python", "app.py"]