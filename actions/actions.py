# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import smtplib
import ssl
from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (SlotSet,AllSlotsReset,EventType,)
class ActionDeactivateLoop(Action):
    SLOT_NAMES = ["requested_slot", "road_accident", "victim_or_no_victim", 
                  "number_victims", "adult_or_child", "breath", "bleeding",
                  "victim_position", "spinal_injury","walk", "other_injury", "location", "send"]
    def name(self) -> Text:
        return "action_deactivate_loop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def get_slot_value(tracker, slot_name):
            slot_value = tracker.get_slot(slot_name)
            return slot_value.upper() if slot_value else ""
        def get_formatted_date():
            now = datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        


        ra = get_slot_value(tracker, "road_accident")
        vn = get_slot_value(tracker, "victim_or_no_victim")
        nv = get_slot_value(tracker, "number_victims")
        ac = get_slot_value(tracker, "adult_or_child")
        br = get_slot_value(tracker, "breath")
        uc = get_slot_value(tracker, "unconscious")
        bl = get_slot_value(tracker, "bleeding")
        vp = get_slot_value(tracker, "victim_position")
        si = get_slot_value(tracker, "spinal_injury")
        wlk = get_slot_value(tracker, "walk")
        oi = get_slot_value(tracker, "other_injury")
        gps = get_slot_value(tracker, "location")
        send = get_slot_value(tracker, "send")
        final_result = f"HELP! CALL EMERGENCY!\nThere is: {ra}.\n{vn}\nNumber of victims: {nv}.\nThe victim is {ac}, {uc}, is {br}, has {bl}, {si} and {wlk} {oi}\nI'm giving first aid required from EJRILI YAMMI APP\nLocation is: {gps}\nDate :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        message = final_result if send == "SEND" else ""
        print(message)
        smtp_port = 587                 # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server
        
        email_from = "ejrili.yammi2023@gmail.com"
        email_to = "benhaddadaisraa@gmail.com"
        # email_to = "onpc@email.ati.tn"
        
        pswd = "czbutbqeerjvftbu"
        
        # content of message
        
        message = final_result
        
        # Create context
        simple_email_context = ssl.create_default_context()

        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pswd)
            print("Connected to server :-)")

            # Send the actual email
            print()
            print(f"Sending email to - {email_to}")
            TIE_server.sendmail(email_from, email_to, message)
            print(f"Email successfully sent to - {email_to}")

        # If there's an error, print it out
        except Exception as e:
            print(e)
        dispatcher.utter_message(text=message)

        slots_to_reset = [SlotSet(slot, None) for slot in self.SLOT_NAMES]
        return slots_to_reset
class CheckBleeding(Action):
    
    
    def name(self) -> Text:
        return "utter_action_check_bleeding"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answer_blood_stop = tracker.latest_message['text'].lower()

        response_dict = {
            "bleeding stopped": {"text": "Okay, make sure to keep the wound clean and watch for any signs of infection."},
            "bleeding is very heavy": {"text": "Call an ambulance or go to the nearest emergency department. It may be necessary for a doctor or nurse to pack the nose with dressings to stop the bleeding.", "image": "https://i.ibb.co/dD2x2gp/ambulance.jpg"}
        }

        if answer_blood_stop in response_dict:
            response = response_dict[answer_blood_stop]
            dispatcher.utter_message(text=response["text"], image=response.get("image"))
            print(answer_blood_stop)

        return []
    
