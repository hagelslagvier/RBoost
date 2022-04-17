import wave

import pyaudio


class Recorder:
    def __init__(self, audio_settings=None, file_path=None):

        self.__audio_settings = (
            audio_settings
            if audio_settings
            else {
                "input": True,
                "format": pyaudio.paInt16,
                "channels": 2,
                "rate": 44100,
                "frames_per_buffer": 1024,
                "stream_callback": self.__defaultCallback(),
            }
        )

        file_path = file_path if file_path else "unnamed.wav"

        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(**self.__audio_settings)
        self.__file = self.__openFile(file_path)

    def __del__(self):
        self.close()

    def __defaultCallback(self):
        def callback(in_data, frame_count, time_info, status):
            self.__file.writeframes(in_data)
            return in_data, pyaudio.paContinue

        return callback

    def __openFile(self, path):
        file = wave.open(path, "wb")
        file.setsampwidth(self.__audio.get_sample_size(pyaudio.paInt16))
        file.setnchannels(self.__audio_settings["channels"])
        file.setframerate(self.__audio_settings["rate"])
        return file

    def start(self):
        self.__stream.start_stream()

    def stop(self):
        self.__stream.stop_stream()

    def close(self):
        self.__stream.close()
        self.__audio.terminate()
        self.__file.close()


if "__main__" == __name__:
    import time

    recorder = Recorder()
    recorder.start()
    time.sleep(5)
    recorder.stop()

    data = recorder.audio()
    print(type(data))
