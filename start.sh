#!/bin/bash

# تشغيل خادم Rasa في الخلفية
rasa run --enable-api --cors "*" --port $PORT 