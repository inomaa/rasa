# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
import sqlite3


class ActionShowContent(Action):
    def name(self) -> Text:
        return "action_show_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('dbfaqbot.db')
        c = conn.cursor()

        #perintah sql menampilkan data pada table
        tipee=tracker.get_slot("tipe")
        namaa=tracker.get_slot("nama_doc")
        c.execute('''SELECT linkk FROM data where tipe LIKE '{0}' AND nama LIKE '{1}';'''.format(tipee,namaa))
        out=c.fetchone()
        kalimat=""
        for row in out:
            row=str(row)
            kalimat+=row
        dispatcher.utter_message(text="Berikut ini merupakan dokumen yang kamu minta. "
                                       "Dokumen dapat dilihat di [sini]({}).".format(kalimat))
        c.close()
        conn.close()
        return []


class ActionChoose(Action):
    def name(self) -> Text:
        return "action_choose"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        buttons = [
            {"payload": '/form{"tipe":"formulir"}', "title": "Formulir"},
            {"payload": '/kuisioner{"tipe":"kuisioner"}', "title": "Kuisioner"}
        ]
        dispatcher.utter_message(
            text="Apa tipe dokumen yang kamu butuhkan?", buttons=buttons)

        return[]


class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [Restarted()]
        
class ActionKuis(Action):

    def name(self) -> Text:
        return "action_setkuis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output="kuisioner"
        return [SlotSet("tipe", output)]

class ActionForm(Action):

    def name(self) -> Text:
        return "action_setform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        output="formulir"
        return [SlotSet("tipe", output)]

class ActionResetDoc(Action):

    def name(self) -> Text:
        return "action_resetdoc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("nama_doc", None)]
