import hassapi as hass
import helpermodule as h

"""
Class Phone_Manager handles sending call to voice notfyng service
"""

__NOTIFY__ = "notify/"
SUB_TTS = [(r"[\*\-\[\]_\(\)\{\~\|\}\s]+", " ")]


class Phone_Manager(hass.Hass):
    def initialize(self):
        self.tts_language = self.args.get("tts_language")
        self.dict_lingua = {
            "it-IT": "it-IT-Standard-A",
            "en-GB": "en-GB-Standard-A",
            "en-US": "en-US-Standard-A",
            "fr-FR": "fr-FR-Standard-A",
            "de-DE": "de-DE-Standard-A",
            "es-ES": "es-ES-Standard-A",
        }

    def send_voice_call(self, data, phone_name: str, sip_server_name: str):
        message = h.replace_regular(data["message"], SUB_TTS)
        message_tts = message.replace(" ", "%20")
        called_number = data["called_number"]
        lang = self.dict_lingua.get(self.get_state(self.tts_language))
        phone_name = phone_name.lower().replace(" ", "_")
        if phone_name.find("voip_call") != -1:
            if called_number != "":
                called_number = "sip:{}@{}".format(called_number, sip_server_name)
                self.call_service(
                    "hassio/addon_stdin",
                    addon="89275b70_dss_voip",
                    input={"call_sip_uri": called_number, "message_tts": message},
                )
        else:
            if called_number != "":
                url_tts = "http://api.callmebot.com/start.php?source=HA&user={}&text={}&lang={}".format(
                    called_number, message_tts, lang
                )
                self.call_service("shell_command/telegram_call", url=url_tts)
