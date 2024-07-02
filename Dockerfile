FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://root:nmLZ0UKO6BxNg2IBYiGwTXfb03YZirkO@dpg-cq20l33v2p9s73da88bg-a.frankfurt-postgres.render.com/taskage
ENV ALLOWED_ORIGINS="https://taskage-client.vercel.app/"
CMD ["python", "app.py"]