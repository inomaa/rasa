# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher

data = {
    "formulir": {
        "Formulir Usulan Penulisan Ijazah": "https://ia601401.us.archive.org/1/items/formulir-usulan-penulisan-ijazah/Formulir%20Usulan%20Penulisan%20Ijazah.pdf",
        "Ceklis Berkas Persyaratan Wisuda": "https://ia601404.us.archive.org/12/items/formulir-check-list-persyaratan-wisuda/Formulir%20Check%20List%20Persyaratan%20Wisuda.pdf",
        "Formulir Pelayanan Legalisasi Ijazah/ Transkrip": "https://ia601501.us.archive.org/6/items/formulir-pelayanan-legalisir-ijazah-transkrip/Formulir%20Pelayanan%20Legalisir%20Ijazah%20Transkrip.pdf",
        "Formulir Pembuatan Terjemahan Ijazah Bahasa Inggris": "https://ia601509.us.archive.org/28/items/formulir-pelayanan-pembuatan-terjemahan-ijazah-transkrip-ke-dalam-bahasa-inggris/Formulir%20Pelayanan%20Pembuatan%20Terjemahan%20Ijazah%20Transkrip%20ke%20dalam%20Bahasa%20Inggris.pdf",
        "Formulir Pembuatan Surat Keterangan Ijazah Rusak/ Hilang": "https://ia601404.us.archive.org/24/items/formulir-pelayanan-pembuatan-surat-keterangan-pengganti-ijazah-transkrip-yang-rusak-hilang/Formulir%20Pelayanan%20Pembuatan%20Surat%20Keterangan%20Pengganti%20Ijazah%20Transkrip%20yang%20Rusak%20Hilang.pdf",
        "Surat Pernyataan Orang Tua/ Wali": "https://ia601506.us.archive.org/22/items/formulir-surat-pernyataan-orang-tua-atau-wali-mahasiswa/Formulir%20Surat%20Pernyataan%20Orang%20Tua%20atau%20Wali%20Mahasiswa.pdf"
    },
    "kuisioner": {
        "Kuisioner Alumni": "https://ia601503.us.archive.org/11/items/formulir-kuisioner-alumni/Formulir%20Kuisioner%20Alumni.pdf"
    }
}


class ActionShowContent(Action):
    def name(self) -> Text:
        return "action_show_content"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tipe_check, nama_check = tracker.get_slot(
            "tipe"), tracker.get_slot("nama_doc")
        out = data[tipe_check][nama_check]
        dispatcher.utter_message(text="Berikut ini merupakan dokumen yang kamu minta. "
                                      "Dokumen dapat dilihat di [sini]({}).".format(out))

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
