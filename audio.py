import whisper
from pydub import AudioSegment
from os.path import join as j
from os import remove

class AudioParser:
	def __init__(self, path_to_file, whisper_model="tiny"):
		self.audio = AudioSegment.from_file(path_to_file)
		self.model_name = whisper_model
		self.marker_pos = 0
		print("INITING AUDIOPARSER, path to file is", path_to_file)

	def Transcribe(self):
		
		model =  whisper.load_model(self.model_name)
		print('Model loaded, starting recognision...')
		self.audio.export('orig' + '.mp3', format='mp3')
		self.transcribtion = model.transcribe('orig' + '.mp3', verbose=True)
		remove('orig' + '.mp3')
		self.length = len(self.transcribtion['segments'])
		print('Recognision finished, total:', self.length, 'phrases.')


	def CutItUp(self):
		self.audio_parts = []
		for num, phrase in enumerate(self.transcribtion['segments']):
			self.MakeCut(j('tmp', str(num) + '.mp3'), phrase['start'], phrase['end'])


	def MakeCut(self, path_to_output, start_time, end_time):
		#making start and end time are in seconds
		start_time = start_time * 1000
		end_time = end_time * 1000

		
		#audio = AudioSegment.from_file(path_to_input)
		cut = self.audio[start_time:end_time]
		self.audio_parts.append(cut)
		#cut.export(path_to_output, format="mp3")

	def GetCurrentPart(self):
		return self.audio_parts[self.marker_pos-1]

	def GetNextLine(self):
		self.marker_pos += 1
		return self.transcribtion['segments'][self.marker_pos - 1]

	def GetPreviousLine(self):
		self.marker_pos -= 1
		return self.transcribtion['segments'][self.marker_pos - 1]

	def Set_text(self, text):
		print('setting text - ', text)
		self.transcribtion['segments'][self.marker_pos-1]['text'] = text

	def ExportText(self):
		all_text = []
		for line in self.transcribtion['segments']:
			all_text.append(line['text'].replace('\n', ''))

		import pandas as pd
		data = {'text':all_text}
		df = pd.DataFrame(data)

		df.to_excel('output.xlsx', index = True)

