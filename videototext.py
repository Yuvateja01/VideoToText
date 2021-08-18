import moviepy.editor as  mp
import speech_recognition as sr
from pydub import AudioSegment
import os
from pydub.silence import split_on_silence



uploaded_clip=mp.VideoFileClip(r"taliban.mp4")
print(uploaded_clip)
uploaded_clip.audio.write_audiofile(r"audio.wav")
r = sr.Recognizer()
def get_audio_transcription(path):
	sound = AudioSegment.from_wav(path)
	chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
	folder_name = "audio-split"
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	whole_text = ""
	for i, audio_chunk in enumerate(chunks, start=1):

		chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
		audio_chunk.export(chunk_filename, format="wav")

		with sr.AudioFile(chunk_filename) as source:
			audio_listened = r.record(source)

			try:
				text = r.recognize_google(audio_listened)
			except sr.UnknownValueError as e:
				print("Error:", str(e))
			else:
				text = f"{text.capitalize()}. "
				print(chunk_filename, ":", text)
				whole_text += text
	return whole_text
print(get_audio_transcription("audio.wav"))




