FROM alpine:latest
RUN apk add --no-cache py3-transmission-rpc
COPY trm.py .
USER nobody
CMD ["python3", "trm.py"]
