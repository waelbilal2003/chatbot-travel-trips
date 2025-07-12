#!/bin/bash

# تشغيل خادم Rasa في الخلفية
rasa run --enable-api --cors "*" --port $PORT &

# تشغيل خادم Actions
rasa run actions --port $ACTION_PORT

# يمكنك إضافة تحقق من الأخطاء هنا إذا لزم الأمر