"""
iago
----
This script contains
the Iago class

Date: 2020-07-15

Author: Lorenzo Coacci
"""
# + + + + + Libraries + + + + +
# to manage data - pandas
import pandas as pd
# to manage speech recognition (speech 2 text)
import speech_recognition as sr
# to manage text 2 speech
import pyttsx3
# to manage time
import time
# to play sounds
from playsound import playsound
# for log funcs
from golog import (
    error_print, warning_print,
    ERROR_COLOR, info_print
)
# + + + + + Libraries + + + + +


# + + + + + Classes + + + + +
class Iago():
    """
    Iago : a Python Speaking Assistant

    A Python bot that helps you with speaking and listening

    Parameters
    ----------
    trigger_string (optional): string
            The trigger string to activate ok python bot
    stop_string (optional): string
        The trigger string to stop Iago
    volume (optional): float
        The volume [it goes from a min of 0.0 to a max of 1.0]
    voice_speed (optional): float
        The rate of speaking in % (can go over 100% ex: 150%)
    voice_name (optional): string
        The voice name (default Samantha - woman)
    show_debug (optional) : bool
            Show the debug info if it fails?

    Attributes
    ----------

    Methods
    -------

    """
    def __init__(self, volume=0.9, voice_speed=150, voice_name="Samantha",
                 trigger_string="iago", stop_string="exit", show_debug=True):
        # welcome - begin setup
        if show_debug:
            info_print("""\n\t* * * Iago * * *\n""")
            info_print("Begin setup...")

        # set recognizer [speech 2 text]
        try:
            self.recognizer = sr.Recognizer()
        except Exception as e:
            error_print("Cannot load recognizer object from speech_recognition package", exception=e)

        # set speak engine to talk [text 2 speech]
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            error_print("Cannot load engine to speak from pyttsx3. Are you using Python3?", exception=e)

        # initialize default settings
        self.volume = 0.9
        self.voice_speed = 150
        self.voice_name = "Samantha"
        self.trigger_string = trigger_string
        self.stop_string = stop_string

        # set user settings
        self.set_volume(volume)
        self.set_voice_speed(voice_speed)
        self.set_voice(voice_name)

        # end setup
        if show_debug:
            info_print("End setup...")

    def say(self, string_to_say,
            volume=None, voice_speed=None,
            voice_name=None, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 say the string

        Parameters
        ----------
        string_to_say : string
            The string to say
        volume (optional): float
            The volume [it goes from a min of 0.0 to a max of 1.0]
        voice_name (optional) : string
            The voice name
        voice_speed (optional) : float
            The rate of speaking in % (can go over 100% ex: 150%)
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        # set default
        if volume is None:
            volume = self.volume
        if voice_speed is None:
            voice_speed = self.voice_speed
        if voice_name is None:
            voice_name = self.voice_name

        # parameters validation
        if volume < 0 or volume > 1:
            if show_debug:
                error_print("Please insert a valid volume [from 0.0 to 1.0]")
            return {"status": False, "error": "Please insert a valid volume [from 0.0 to 1.0]"}
        if voice_speed <= 0:
            if show_debug:
                error_print("Please insert a valid speed [> 0]")
            return {"status": False, "error": "Please insert a valid speed [> 0]"}

        # pyttsx3 setup change
        try:
            self.engine.setProperty("rate", voice_speed)   # Speed percent (can go over 100)
            self.engine.setProperty("volume", volume)      # Volume 0-1
        except Exception as e:
            if show_debug:
                error_print("Cannot change voice speed and volume", exception=e)
            return {"status": False, "error": "Cannot change voice speed and volume because -> {}".format(str(e))}
        # voices available
        try:
            voices = self.engine.getProperty('voices')
        except Exception as e:
            if show_debug:
                error_print("Cannot get list of al voices", exception=e)
            return {"status": False, "error": "Cannot get list of al voices because -> {}".format(str(e))}
        # voice id
        voice_id = ""
        for voice in voices:
            if voice.name == voice_name:
                voice_id = voice.id
        if voice_id == "":
            if show_debug:
                error_print("Cannot find a voice with this name")
            return {"status": False, "error": "Cannot find a voice with this name"}
        else:
            try:
                self.engine.setProperty('voice', voice_id)
            except Exception as e:
                if show_debug:
                    error_print("Cannot set this voice", exception=e)
                return {"status": False, "error": "Cannot set this voice because -> {}".format(str(e))}

        # say the string
        try:
            self.engine.say(string_to_say)
        except Exception as e:
            if show_debug:
                error_print("Cannot say that string", exception=e)
            return {"status": False, "error": "Cannot say that string, because -> {}".format(str(e))}

        # run the say command and talk
        try:
            self.engine.runAndWait()
        except Exception as e:
            if show_debug:
                error_print("Cannot run the speech engine and talk", exception=e)
            return {"status": False, "error": "Cannot run the speech engine and talk, because -> {}".format(str(e))}

        # pyttsx3 restore original values
        try:
            self.engine.setProperty("rate", self.voice_speed)   # restore Speed percent (can go over 100)
            self.engine.setProperty("volume", self.volume)      # restore Volume 0-1
            self.set_voice(self.voice_name)                     # restore voice
        except Exception as e:
            if show_debug:
                warning_print("Cannot restore default Iago proprieties")

        return {"status": True, "error": ""}

    def speech_to_text(self, audio, recognizer='google', language='en-US',
                       show_debug=True, **kwargs):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 the sentence (string) of the user

        Parameters
        ----------
        audio : audio
            The audio to convert in text
        recognizer (optional): string
            The API/engine to recognize speech
        language (optional): string
            The language to recognize
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        # process sentence
        try:
            # print what I said
            if recognizer == 'google':
                sentence = self.recognizer.recognize_google(audio, language=language)
            elif recognizer == 'bing':
                sentence = self.recognizer.recognize_bing(audio)
            elif recognizer == 'google_cloud':
                sentence = self.recognizer.recognize_google_cloud(audio)
            elif recognizer == 'houndify':
                sentence = self.recognizer.recognize_houndify(audio, **kwargs)
            elif recognizer == 'ibm':
                sentence = self.recognizer.recognize_ibm(audio)
            elif recognizer == 'sphinx':
                sentence = self.recognizer.recognize_sphinx(audio)
            elif recognizer == 'wit':
                sentence = self.recognizer.recognize_wit(audio)

            return {"status": True, "error": "", "value": sentence}
        except sr.UnknownValueError:
            # Cannot understand your sentence
            if show_debug:
                warning_print("Warning: Could not understand audio")
            return {"status": False, "value": None, "error": "Cannot understand audio"}
        except sr.RequestError as e:
            # Error with API request
            if show_debug:
                error_print("Cannot request results from the API", exception=e)
            return {"status": False, "value": None, "error": "Cannot request results from the API, because -> {}".format(str(e))}
        except Exception as e:
            if show_debug:
                error_print("Cannot convert sentence to text (other error)", exception=e)
            return {"status": False, "value": None, "error": "Cannot convert sentence to text (other error), because -> {}".format(str(e))}

    def play_sound(self, file_name, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 play the sound

        Parameters
        ----------
        file_name : string
            Path (with extension) to the audio file
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            playsound(file_name)
            return {"status": False, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot play the audio, check the format or cannot find it", exception=e)
            return {"status": False, "error": "Cannot play the audio, check the format or cannot find it, reason -> {}".format(str(e))}

    def audio_to_text(self, file_path,
                      recognizer='google', language='en-US',
                      reduce_noise=True, offset=0,
                      duration=None, noise_duration=None, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 audio file converted to text

        Parameters
        ----------
        file_path : string
             The path for the audio file
        recognizer (optional): string
            The API/engine to recognize speech
        language (optional): string
            The language to recognize
        offset (optional) : float
            Offset for the beginning
        duration (optional) : float
            Duration for recording audio
        noise_duration (optional) : float
            Duration for noise reduce filter
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        # listen the audio
        try:
            try:
                file = sr.AudioFile(file_path)
            except Exception as e:
                if show_debug:
                    error_print("Cannot find the audio file", exception=e)
                return {"status": False, "value": None, "error": "Cannot find the audio file because -> {}".format(str(e))}
            with file as source:
                # reduce noise
                if reduce_noise:
                    if noise_duration is None:
                        self.recognizer.adjust_for_ambient_noise(source)
                    else:
                        self.recognizer.adjust_for_ambient_noise(source,
                                                                 duration=noise_duration)
                # capture audio
                if duration is None:
                    audio = self.recognizer.record(source, offset=offset)
                else:
                    audio = self.recognizer.record(source, offset=offset,
                                                   duration=duration)
                # speech 2 sentence
                text = self.speech_to_text(audio, recognizer=recognizer,
                                           language=language, show_debug=True)['value']
                return {"status": False, "value": text, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot parse the audio, check format, only WAV!", exception=e)
            return {"status": False, "value": None, "error": "Cannot parse the audio, check format, only WAV! reason -> {}".format(str(e))}

    def listen(self, reply="Speak, I'm listening",
               recognizer='google', language='en-US',
               trigger_string=None, stop_string=None,
               sample_rate=48000, chunk_size=2048,
               skip_reply=False,
               reduce_noise=True, noise_duration=None,
               audio_trigger=None, audio_trigger_path="./",
               show_debug=True):
        """
        RETURN : the sentence (string) of the user

        Parameters
        ----------
        reply (optional): string
            The reply when listening is triggered
        recognizer (optional): string
            The API/engine to recognize speech
        language (optional): string
            The language to recognize
        sample_rate (optioanl): float
            The sample rate for the mic
        chunk_size (optional): float
            The bytes chunk size for the mic
        trigger_string (optional): string
            The trigger string to activate ok python bot
        stop_string (optional): string
            The trigger string to stop Iago
        reduce_noise (optional): bool
            Do you want to reduce noise around?
        noise_duration (optional): float
            The float noise duration
        skip_reply (optional): bool
            Skip the reply part?
        audio_trigger (optional): bool
            Use an audio to trigger listening?
        audio_trigger_path (optioanl): string
            The audio path to the wav file trigger audio
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        sentence : string
            The sentence of the user
            or None if error
        """
        # load saved data
        if trigger_string is None:
            trigger_string = self.trigger_string
        if stop_string is None:
            stop_string = self.stop_string

        if not skip_reply:
            if language == 'it-IT':
                reply = "Parla pure, ti ascolto!"

            # reply
            self.say(reply, show_debug=False)
            info_print(reply)
            info_print("...")

        # listen the user
        try:
            with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
                sentence = ""
                # play go sound
                if audio_trigger is not None:
                    self.play_sound(audio_trigger_path + audio_trigger)
                if reduce_noise:
                        if noise_duration is None:
                            self.recognizer.adjust_for_ambient_noise(source)
                        else:
                            self.recognizer.adjust_for_ambient_noise(source,
                                                                     duration=noise_duration)
                while(trigger_string not in sentence.lower()):
                    # capture audio
                    audio = self.recognizer.listen(source)
                    # speech 2 sentence
                    result_sentence = self.speech_to_text(audio, recognizer=recognizer,
                                                          language=language, show_debug=True)
                    sentence = result_sentence['value']
                    info_print("Sentence: \"{}\"".format(sentence))
                    if sentence is None:
                        # I didnt understand
                        cannot_understand = "Sorry, I didn't get that"
                        info_print(cannot_understand)

                        sentence = ""
                        # play go sound
                        if audio_trigger is not None:
                            self.play_sound(audio_trigger_path + audio_trigger)
                    if stop_string in sentence.lower():
                        # Ok no problem bye
                        byebye = "Ok, no problem, bye bye!"
                        info_print(byebye)
                        self.say(byebye, show_debug=True)
                        return None

                if sentence is None:
                    # I didnt understand
                    cannot_understand = "Sorry, I didn't get that"
                    info_print(cannot_understand)
                    if language == 'it-IT':
                        cannot_understand = "Non ho capito bene"
                    self.say(cannot_understand)
                    sentence = ""
                    # play go sound
                    if audio_trigger is not None:
                        self.play_sound(audio_trigger_path + audio_trigger)

                return sentence.lower()
        except Exception as e:
            error_print("Error: Cannot connect to the microphone", exception=e)
            return None

    def mute(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 mute

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            self.engine.setProperty('volume', 0)
            self.volume = 0
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot mute volume", exception=e)
            return {"status": False, "error": "Cannot mute volume because {}".format(str(e))}

    def set_mic(self, show_debug=True):
        pass

    def set_volume(self, volume, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set volume

        Parameters
        ----------
        volume : float
            The volume [it goes from a min of 0.0 to a max of 1.0]
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        if volume < 0 or volume > 1:
            if show_debug:
                error_print("Please insert a valid volume [from 0.0 to 1.0]")
            return {"status": False, "error": "Please insert a valid volume [from 0.0 to 1.0]"}
        try:
            self.engine.setProperty("volume", volume)  # Volume 0-1
            self.volume = volume
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot set volume because -> {}".format(str(e)))
            return {"status": False, "error": "Cannot set volume because -> {}".format(str(e))}

    def set_voice_speed(self, voice_speed, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set volume

        Parameters
        ----------
        voice_speed : float
            The rate of speaking in % (can go over 100% ex: 150%)
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        # parameter validation
        if voice_speed <= 0:
            if show_debug:
                error_print("Please insert a valid speed [> 0]")
            return {"status": False, "error": "Please insert a valid speed [> 0]"}
        try:
            self.engine.setProperty('rate', voice_speed)
            self.voice_speed = voice_speed
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot set voice speed, because -> {}".format(str(e)))
            return {"status": False, "error": "Cannot set voice speed, because -> {}".format(str(e))}

    def set_voice_by_id(self, voice_id, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set volume

        Parameters
        ----------
        voice_id : string
            The id of a particular voice
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            self.engine.setProperty('voice', voice_id)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if voice.id == voice_id:
                    self.voice_name = voice.name
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot find a voice with that ID", exception=e)
            return {"status": False, "error": "Cannot find a voice with that ID because -> {}".format(str(e))}

    def set_voice(self, voice_name, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set volume

        Parameters
        ----------
        name : string
            The name of a particular voice
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            voices = self.engine.getProperty('voices')
            voice_id = ""
            for voice in voices:
                if voice.name == voice_name:
                    voice_id = voice.id
            if voice_id == "":
                if show_debug:
                    error_print("Cannot find a voice with this name")
                return {"status": False, "error": "Cannot find a voice with this name"}
            else:
                self.engine.setProperty('voice', voice_id)
                self.voice_name = voice_name
                return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot change ok python voice", exception=e)
            return {"status": False, "error": "Cannot change ok python voice because -> {}".format(str(e))}

    def set_trigger_string(self, trigger_string, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set trigger string

        Parameters
        ----------
        trigger_string : string
            The trigger string for Iago to listen
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            self.trigger_string = trigger_string
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot set trigger string", exception=e)
            return {"status": False, "error": "Cannot set trigger string because -> {}".format(str(e))}

    def set_stop_string(self, stop_string, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 set stop string

        Parameters
        ----------
        stop_string : string
            The trigger string for Iago to listen
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            self.stop_string = stop_string
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot set stop string", exception=e)
            return {"status": False, "error": "Cannot set stop string because -> {}".format(str(e))}

    def get_mics(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 get mics

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        # find working mics
        try:
            info_print(sr.Microphone.list_working_microphones())
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot print all mics", exception=e)
            return {"status": False, "error": "Cannot print all mics because -> {}".format(str(e))}

    def get_voices(self, show_names_only=False, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg },
                 get mics

        Parameters
        ----------
        show_names_only : bool
            Show only names?
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg }
        """
        try:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if show_names_only:
                    print(" Name: %s" % voice.name)
                else:
                    print("Voice:")
                    print(" - ID: %s" % voice.id)
                    print(" - Name: %s" % voice.name)
                    print(" - Languages: %s" % voice.languages)
                    print(" - Gender: %s" % voice.gender)
                    print(" - Age: %s" % voice.age)
            return {"status": True, "error": ""}
        except Exception as e:
            if show_debug:
                error_print("Cannot print voices list", exception=e)
            return {"status": False, "error": "Cannot print voices list because -> {}".format(str(e))}

    def get_mic(self, show_debug=True):
        pass

    def get_volume(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 get volume

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        try:
            volume = self.volume
            return {"status": True, "error": "", "value": volume}
        except Exception as e:
            if show_debug:
                error_print("Cannot get volume", exception=e)
            return {"status": False, "error": "Cannot get volume because -> {}".format(str(e)), "value": None}

    def get_voice_speed(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 get voice speed

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        try:
            voice_speed = self.voice_speed
            return {"status": True, "error": "", "value": voice_speed}
        except Exception as e:
            if show_debug:
                error_print("Cannot get voice_speed", exception=e)
            return {"status": False, "error": "Cannot get voice_speed because -> {}".format(str(e)), "value": None}

    def get_voice(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 get voice name

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        try:
            voice_name = self.voice_name
            return {"status": True, "error": "", "value": voice_name}
        except Exception as e:
            if show_debug:
                error_print("Cannot get voice_speed", exception=e)
            return {"status": False, "error": "Cannot get voice_speed because -> {}".format(str(e)), "value": None}

    def get_trigger_string(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 get trigger string

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        try:
            trigger_string = self.trigger_string
            return {"status": True, "error": "", "value": trigger_string}
        except Exception as e:
            if show_debug:
                error_print("Cannot get trigger_string", exception=e)
            return {"status": False, "error": "Cannot get trigger_string because -> {}".format(str(e)), "value": None}

    def get_stop_string(self, show_debug=True):
        """
        RETURN : {"status": True/False, "error": error_msg, "value": value},
                 get stop string

        Parameters
        ----------
        show_debug (optional) : bool
            Show the debug info if it fails?

        Returns
        -------
        status : dict
            {"status": True/False, "error": error_msg, "value": value}
        """
        try:
            stop_string = self.stop_string
            return {"status": True, "error": "", "value": stop_string}
        except Exception as e:
            if show_debug:
                error_print("Cannot get stop_string", exception=e)
            return {"status": False, "error": "Cannot get stop_string because -> {}".format(str(e)), "value": None}
# + + + + + Classes + + + + +
