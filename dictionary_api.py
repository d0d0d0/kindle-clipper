import  requests
import json

API_KEY = 'api_key'
API_ID = 'api_id'

LANGUAGE = 'en-gb'
URL = 'https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/%s'  

MINUTE_LIMIT = 60

def search_word(word):

	definitions = []

	r = requests.get(URL %(word.lower()), headers = {'app_id' : API_ID, 'app_key' : API_KEY})

	if r.status_code == 200:
		resp = r.json()

		for result in resp["results"]:
			for lex in result["lexicalEntries"]:
				for entry in lex["entries"]:
					for sense in entry["senses"]:
						if "definitions" in sense:
							for definition in sense["definitions"]:
								definitions.append(definition)

	lean_definitions = definitions[:3] if len(definitions) >= 3 else definitions
	definition_str = '; '.join(lean_definitions)

	return definition_str

