import time
import json
import audio
import requests

URL = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
# URL = "https://stream.watsonplatform.net/speech-to-text/api"
USER = "1d5bbded-2ec9-4580-afd2-3344fc3189dc"
PASSWORD = "Qes6oDWENr3a"


def dumps(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


class Watson:
    def __init__(self):
        self.__recorder = audio.Recorder()

    def start(self):
        self.__recorder.start()

    def stop(self):
        self.__recorder.stop()

    def text(self):
        data = open("unnamed.wav", "rb").read()

        response = requests.post(url=URL, auth=(USER, PASSWORD), headers={'Content-Type': 'audio/wav'}, data=data)

        data = response.content
        data = data.decode()
        data = json.loads(data)

        results = data["results"]
        result_0 = results[0]
        alternatives = result_0["alternatives"]
        alternative_0 = alternatives[0]
        text = alternative_0["transcript"]

        return text

if "__main__" == __name__:
    watson = Watson()
    watson.start()
    time.sleep(2)
    watson.stop()
    print(watson.text())




