#!/bin/bash
PORT=${PORT:-8080}

# تأخير لضمان جاهزية الشبكة (للمشاكل المتكررة)
sleep 10

echo "🚀 Starting Rasa on port $PORT"
rasa run --enable-api --cors "*" --port $PORT --debug