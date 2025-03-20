# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

ARG PLEACH_IMAGE
FROM $PLEACH_IMAGE

RUN rm -rf /app/.venv/pleach/frontend

CMD ["python", "-m", "pleach", "run", "--host", "0.0.0.0", "--port", "7860", "--backend-only"]
