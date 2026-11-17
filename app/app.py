"""Visit-counter API: Flask + Redis. The Day 18 three-tier project (nginx -> app -> redis)."""
import os

import redis
from flask import Flask, jsonify

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2, decode_responses=True)


@app.get("/")
def index():
    try:
        visits = cache.incr("visits")
    except redis.exceptions.RedisError:
        return jsonify(error="cache unavailable"), 503
    return jsonify(message="Hello from Docker", visits=visits, host=os.uname().nodename)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    """Ready only if Redis answers."""
    try:
        cache.ping()
    except redis.exceptions.RedisError:
        return jsonify(status="redis unavailable"), 503
    return jsonify(status="ready")
