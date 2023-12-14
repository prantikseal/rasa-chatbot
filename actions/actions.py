# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionOperationalHours(Action):
    def name(self) -> Text:
        return "action_operational_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open("data.json", "r") as file:
            data = json.load(file)

        # Fetching and providing operational hours information
        store_location = tracker.get_slot("store_location")
        if store_location in data["operational_hours"]:
            hours_info = data["operational_hours"][store_location]
            dispatcher.utter_message(f"The store is open {hours_info}.")
        else:
            dispatcher.utter_message("I'm sorry, I don't have information for that store location.")

        return []

class ActionFlowerRecommendations(Action):
    def name(self) -> Text:
        return "action_flower_recommendations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open("data.json", "r") as file:
            data = json.load(file)

        # Fetching and providing flower recommendations
        occasion = tracker.get_slot("occasion")
        if occasion in data["flower_recommendations"]:
            recommendations = data["flower_recommendations"][occasion]
            dispatcher.utter_message(f"For {occasion}, I recommend the following flowers: {', '.join(recommendations)}.")
        else:
            dispatcher.utter_message(f"I'm sorry, I don't have recommendations for {occasion}.")

        return []

