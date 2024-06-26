import whisper
from pydub import AudioSegment
from os.path import join, isdir
from os import remove, mkdir, walk
import pickle


class AudioParser:
	def __init__(self, path_to_file, whisper_model="tiny", save_me='no', load_me='no'):
		self.audio = AudioSegment.from_file(path_to_file)
		self.model_name = whisper_model
		self.marker_pos = 0
		self.audio_parts = []
		self.transcribtion = []
		self.load_me = (load_me == 'yes')
		self.save_me = (save_me == 'yes')
		print("INITING AUDIOPARSER, path to file is", path_to_file)

	def __eq__(self, other):
		if self.audio != other.audio:
			return False
		if self.model_name != other.model_name:
			return False
		return True

	def Save(self):
		if not(isdir('storage')):
			mkdir('storage')

		with open(join('storage', str(hash(self.audio))), 'wb') as file:
			pickle.dump(self, file)

	def Load(self):
		success = False
		for root, dirs, files in walk('storage'):
			for file in files:
				with open(join(str(root), str(file)) , 'rb') as file:
					obj = pickle.load(file)
					if obj == self:
						self.transcribtion = obj.transcribtion
						self.length = obj.length
						success = True
						break
		if success == False:
			print("Не нашлось ничего блин")
		else:
			print("Жесть чето нашлось вау")
		return success


	def Transcribe(self):
		if self.load_me:
			print('Trying to load previous progres...')
			self.Load()
		elif not( self.load_me ):
			model =  whisper.load_model(self.model_name)
			print('Model loaded, starting recognision...')
			self.audio.export('orig' + '.mp3', format='mp3')
			self.transcribtion = model.transcribe('orig' + '.mp3', verbose=True)
			remove('orig' + '.mp3')
			self.length = len(self.transcribtion['segments'])
			print('Recognision finished, total:', self.length, 'phrases.')

		if self.save_me and not(self.load_me):
			self.Save()
			print('Flag for saving was set, saving...')

	def join_small_parts(self, min_duration):
		result = []
		tmp = {'id':0, 'start':self.transcribtion['segments'][0].get('start'), 'text':''}
		for num, phrase in enumerate(self.transcribtion['segments']):
			print(phrase)
			tmp.update({'end':phrase.get('end'), 'text':tmp.get('text') + ' ' + phrase.get('text')})

			if (int(tmp.get('end')) - int(tmp.get('start'))) > min_duration:
				print("Making another cut, tmp: ", tmp)
				result.append(tmp.copy())

				tmp.update({'id':tmp.get('id')+1, 'start':tmp.get('end'), 'text':''})
				print("\n AFTER TMP CLEARING", tmp)
		result.append(tmp)
		print("Join Small Parts result", result)
		return result


	def CutItUp(self):
		#if not(isdir('tmp')):
		#	mkdir('tmp')

		#print(self.transcribtion['segments'])
		self.parsed_segments = self.join_small_parts(10)
		self.length = len(self.parsed_segments)

		print('Parsed Segments: ', self.parsed_segments)


		self.audio_parts = []
		#for num, phrase in enumerate(self.transcribtion['segments']):
		for num, phrase in enumerate(self.parsed_segments):
			self.MakeCut(join('tmp', str(num) + '.mp3'), phrase['start'], phrase['end'])





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
		print("GET NEXT LINE", self.parsed_segments[self.marker_pos-1])
		return self.parsed_segments[self.marker_pos-1]
		#return self.transcribtion['segments'][self.marker_pos - 1]

	def GetPreviousLine(self):
		self.marker_pos -= 1
		return self.parsed_segments[self.marker_pos-1]
		#return self.transcribtion['segments'][self.marker_pos - 1]

	def Set_text(self, text):
		print('setting text - ', text)
		#self.transcribtion['segments'][self.marker_pos-1]['text'] = text
		self.parsed_segments[self.marker_pos - 1]['text'] = text

	def ExportText(self):
		import pandas as pd
		for i in range(len(self.parsed_segments)):
			(self.parsed_segments[i]['start']) = str( int ((self.parsed_segments[i]['start']) // 60)) + " Мин. " + str( int((self.parsed_segments[i]['start']) % 60)) + " с."

		df = pd.DataFrame.from_dict(self.parsed_segments)



		#all_text = []
		#for line in self.transcribtion['segments']:
		#print("Exported Text")
		#print(self.parsed_segments)
		#for line in self.parsed_segments:
		#	all_text.append(line['text'].replace('\n', ''))

		
		#data = {'text':all_text}
		#df = pd.DataFrame(data)

		#print(df)

		df.to_excel('output.xlsx', index = True)

