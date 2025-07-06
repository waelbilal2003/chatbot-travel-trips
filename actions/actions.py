from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionExecuted, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List, Text
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# خريطة الردود بناءً على النية + اللغة + مستوى اللغة
RESPONSE_MAP = {
    
    ("travel_work", "english", "language_excellent"): "utter_question_3_work_in_general",
    ("travel_work", "english", "language_good"): "utter_question_3_work_in_general",
    ("travel_work", "english", "language_itsokay"): "utter_question_3_work_in_general",
    ("travel_work", "english", "language_bad"): "utter_question_3_work_in_general",
    ("travel_work", "french", "language_excellent"): "utter_question_3_work_in_general",
    ("travel_work", "french", "language_good"): "utter_question_3_work_in_general",
    ("travel_work", "french", "language_itsokay"): "utter_question_3_work_in_general",
    ("travel_work", "french", "language_bad"): "utter_question_3_work_in_general",
    ("travel_work", "germany", "language_excellent"): "utter_question_3_work_in_general",
    ("travel_work", "germany", "language_good"): "utter_question_3_work_in_general",
    ("travel_work", "germany", "language_itsokay"): "utter_question_3_work_in_general",
    ("travel_work", "germany", "language_bad"): "utter_question_3_work_in_general",
    ("travel_work", "espanol", "language_excellent"): "utter_question_3_work_in_general",
    ("travel_work", "espanol", "language_good"): "utter_question_3_work_in_general",
    ("travel_work", "espanol", "language_itsokay"): "utter_question_3_work_in_general",
    ("travel_work", "espanol", "language_bad"): "utter_question_3_work_in_general",
    ("travel_work", "other", "language_excellent"): "utter_question_3_work_in_general",
    ("travel_work", "other", "language_good"): "utter_question_3_work_in_general",
    ("travel_work", "other", "language_itsokay"): "utter_question_3_work_in_general",
    ("travel_work", "other", "language_bad"): "utter_question_3_work_in_general",
    ("travel_study", "english", "language_excellent"): "utter_question_study_work_3",
    ("travel_study", "english", "language_good"): "utter_question_study_work_3",
    ("travel_study", "english", "language_itsokay"): "utter_question_study_work_3",
    ("travel_study", "english", "language_bad"): "utter_question_study_work_3",
    ("travel_study", "french", "language_excellent"): "utter_question_study_work_3",
    ("travel_study", "french", "language_good"): "utter_question_study_work_3",
    ("travel_study", "french", "language_itsokay"): "utter_question_study_work_3",
    ("travel_study", "french", "language_bad"): "utter_question_study_work_3",
    ("travel_study", "germany", "language_excellent"): "utter_question_study_work_3",
    ("travel_study", "germany", "language_good"): "utter_question_study_work_3",
    ("travel_study", "germany", "language_itsokay"): "utter_question_study_work_3",
    ("travel_study", "germany", "language_bad"): "utter_question_study_work_3",
    ("travel_study", "espanol", "language_excellent"): "utter_question_study_work_3",
    ("travel_study", "espanol", "language_good"): "utter_question_study_work_3",
    ("travel_study", "espanol", "language_itsokay"): "utter_question_study_work_3",
    ("travel_study", "espanol", "language_bad"): "utter_question_study_work_3",
    ("travel_study", "other", "language_excellent"): "utter_question_study_work_3",
    ("travel_study", "other", "language_good"): "utter_question_study_work_3",
    ("travel_study", "other", "language_itsokay"): "utter_question_study_work_3",
    ("travel_study", "other", "language_bad"): "utter_question_study_work_3"
}

# تعريف نموذج قاعدة البيانات
Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(255))

# إعداد اتصال قاعدة البيانات
DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/sywa_bot'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# التحقق من النوايا السابقة وتعيين الفتحات تلقائيًا وإرسال الرد المناسب
class ActionCheckPreviousIntents(Action):
    def name(self):
        return "action_check_previous_intents"

    def run(self, dispatcher, tracker, domain):
        intent_slots = {
            "travel_study": "travel_study",
            "travel_work": "travel_work",
            "english": "english",
            "french": "french",
            "germany": "germany",
            "espanol": "espanol",
            "other": "other",
            "language_excellent": "language_excellent",
            "language_good": "language_good",
            "language_itsokay": "language_itsokay",
            "language_bad": "language_bad"
        }

        found_intents = {slot: False for slot in intent_slots.values()}

        for event in tracker.events:
            if event.get("event") == "user" and "parse_data" in event:
                intent_name = event["parse_data"].get("intent", {}).get("name")
                if intent_name in intent_slots:
                    found_intents[intent_slots[intent_name]] = True

        slots = [SlotSet(slot, value) for slot, value in found_intents.items()]

        travel_type = next((k for k in ["travel_study", "travel_work"] if found_intents.get(k)), None)
        language = next((k for k in ["english", "french", "germany", "espanol", "other"] if found_intents.get(k)), None)
        level = next((k for k in ["language_excellent", "language_good", "language_itsokay", "language_bad"] if found_intents.get(k)), None)

        print("🔍 Expected key values:", travel_type, language, level)

        if travel_type and language and level:
            response_key = (travel_type, language, level)
            response = RESPONSE_MAP.get(response_key)
            if response:
                dispatcher.utter_message(response=response)
            else:
                dispatcher.utter_message(text="⚠️ No response found for this combination.")
        else:
            dispatcher.utter_message(text="❌ Not all required slots were identified.")

        return slots

# اقتراح المدينة الأكثر تكرارًا وتجاهل مدينة المستخدم
class ActionRecommendCity(Action):
    def name(self):
        return "action_recommend_city"

    async def run(self, dispatcher, tracker, domain):
        city_counts = {}

        # استخراج المدينة التي ينتمي إليها المستخدم
        user_city = None
        for event in tracker.events:
            if event.get("event") == "user" and "parse_data" in event:
                intent_name = event["parse_data"].get("intent", {}).get("name", "")
                if intent_name.startswith("province_"):
                    user_city = intent_name.replace("province_", "").lower()

        # استخراج المدن من نوايا المستخدم السابقة
        for event in tracker.events:
            if event.get("event") == "user" and "parse_data" in event:
                intent_name = event["parse_data"].get("intent", {}).get("name", "")
                if intent_name.startswith("travel_to_"):
                    parts = intent_name.split("_")
                    if len(parts) >= 3:
                        city = parts[2].lower()
                    elif len(parts) == 2:
                        city = parts[1].lower()
                    else:
                        continue
                    city_counts[city] = city_counts.get(city, 0) + 1

        if not city_counts:
            dispatcher.utter_message(text="المعذرة المعلومات التي ادخلتها غير كافية ❌ بالرجاء الاعادة ثم الاكمال من حيث توقفت")
            dispatcher.utter_message(response="utter_question_1_tourism")
            return []

        # إزالة مدينة المستخدم من الاقتراحات
        if user_city and user_city in city_counts:
            print(f"🚫 Skipping user's own city: {user_city}")
            del city_counts[user_city]

        # طباعة المدن المكررة في الـ terminal
        full_city_list = []
        for city, count in city_counts.items():
            full_city_list.extend([city] * count)
        print("📍 Clicked cities during conversation:", full_city_list)

        sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)

        session = Session()
        try:
            for city, count in sorted_cities:
                exists = session.query(City).filter_by(city_name=city.capitalize()).first()
                if exists:
                    utter_name = f"utter_{city}"
                    if "responses" in domain and utter_name in domain["responses"]:
                        dispatcher.utter_message(response=utter_name)
                        
                        # تحديث سجل الاقتراحات
                        history = tracker.get_slot("recommended_cities_history") or []
                        if city not in history:
                            history.append(city)
                            if len(history) > 3:
                                history = history[-3:]
                        return [SlotSet("recommended_city", city), SlotSet("recommended_cities_history", history)]
        except Exception as e:
            dispatcher.utter_message(text=f"⚠️ An error occurred while checking cities: {e}")
        finally:
            session.close()

        dispatcher.utter_message(text="عذراً لا تتوفر رحلة تتناسب مع تفضيلاتك حالياً 😔 حاول مرة أخرى في وقت لاحق 🔁")
        return []

# عرض آخر المدن المقترحة
class ActionShowRecommendedCities(Action):
    def name(self):
        return "action_show_recommended_cities"

    def run(self, dispatcher, tracker, domain):
        history = tracker.get_slot("recommended_cities_history") or []

        if not history:
            dispatcher.utter_message(text="📭 لم يتم اقتراح أي مدن بعد.")
        else:
            formatted_cities = "\n".join([f"{i+1}. {city.capitalize()}" for i, city in enumerate(history)])
            dispatcher.utter_message(text=f"📌 هذه هي آخر المدن التي تم اقتراحها لك:\n\n{formatted_cities}")

        return []

# إضافة فعل التراجع عن الرسالة الأخيرة وإعادة النية السابقة
class ActionResetConversation(Action):
    def name(self):
        return "action_reset_conversation"

    def run(self, dispatcher, tracker, domain):
        intent_history = []

        for event in tracker.events:
            if event.get("event") == "user" and "parse_data" in event:
                intent_name = event["parse_data"].get("intent", {}).get("name")
                if intent_name and intent_name != "reset_conversation":
                    intent_history.append(intent_name)

        print(f"📜 Intent history: {intent_history}")

        if len(intent_history) >= 3:
            latest_intent = intent_history[-1]
            target_intent = intent_history[-2]
            previous_intent = intent_history[-3] if len(intent_history) >= 3 else None

            print(f"🔄 Resetting conversation:")
            print(f"  - Removing latest intent: '{latest_intent}'")
            print(f"  - Skipping target intent: '{target_intent}'")
            print(f"  - Returning to previous intent: '{previous_intent}'")

            events = [UserUtteranceReverted(), UserUtteranceReverted()]

            for intent in [latest_intent, target_intent]:
                if intent.startswith("travel_to_"):
                    parts = intent.split("_")
                    if len(parts) >= 3:
                        city = parts[2].lower()
                        events.append(SlotSet(f"latest_city", None))

                        if len(parts) >= 5 and parts[3] == "specialization":
                            specialization = parts[4].lower()
                            events.append(SlotSet(f"latest_specialization", None))

            dispatcher.utter_message(text=f"🥰تم التراجع  بالنجاح ")
            events.append(ActionExecuted("action_listen"))
            events.append(FollowupAction(previous_intent))

            return events
        else:
            dispatcher.utter_message(text="لا يمكن التراجع فعدد الرسائل قليل للغاية اضغط على زر الحذف 🗑😁.")
            return []
