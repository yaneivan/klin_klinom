import whisper
from pydub import AudioSegment
from os.path import join as j

class AudioParser:
	def __init__(self, path_to_file, whisper_model="tiny"):
		self.audio = AudioSegment.from_file(path_to_file)
		self.model_name = whisper_model
		print("INITING AUDIOPARSER, path to file is", path_to_file)

	def Transcribe(self):
		#self.audio.export(j('tmp', 'origingal' + '.mp3'), format='mp3')
		#print("БЛЯТЬ")
		model =  whisper.load_model(self.model_name)
		print('Model loaded, starting recognision...')
		self.transcribtion = model.transcribe(j('tmp', 'origingal' + '.mp3'), verbose=True)
		self.length = len(self.transcribtion['segments'])
		print('Recognision finished, total:', self.length, 'phrases.')
		
	def CreateGenerator(self):
		self.generator = self.NextLineGenerator()


	def CutItUp(self):
		for num, phrase in enumerate(self.transcribtion['segments']):
			self.MakeCut(j('tmp', str(num) + '.mp3'), phrase['start'], phrase['end'])


	def MakeCut(self, path_to_output, start_time, end_time):
		#start and end time are in seconds

		start_time = start_time * 1000
		end_time = end_time * 1000

		#audio = AudioSegment.from_file(path_to_input)
		cut = self.audio[start_time:end_time]
		cut.export(path_to_output, format="mp3")


	def NextLineGenerator(self):
		for phrase in self.transcribtion['segments']:
			#print("Debug, phrase is", type(phrase), phrase)
			yield phrase


		yield {'text':"That's all folks!"}

