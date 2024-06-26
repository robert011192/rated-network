FROM python:3.11

WORKDIR /app

COPY . /app

# Install dependencies following best practices
RUN pip install --no-cache-dir -r requirements.txt

# Health Check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD [ "curl", "-f", "http://localhost:8000/check_health" ]

# CMD with JSON notation
CMD ["./entrypoint.sh"]