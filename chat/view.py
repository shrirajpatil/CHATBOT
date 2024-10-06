from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment
import tempfile
import speech_recognition as sr
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from googletrans import Translator
from transformers import pipeline
from nltk.stem import PorterStemmer
porter_stemmer = PorterStemmer()
nlp = spacy.load("en_core_web_sm")
nlp_hindi = spacy.load("xx_ent_wiki_sm")
@csrf_exempt

def homepage(request):
    if request.method == 'POST':
        if 'audio' in request.FILES:
            try:
                lang=request.POST.get('lang')
                audio_file = request.FILES.get('audio')

                if audio_file:
                    # Save the audio file to a temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    temp_file.write(audio_file.read())
                    temp_file.close()

                    # Convert the audio file to PCM WAV format
                    converted_temp_file = convert_audio_to_wav(temp_file.name)
                    recognized_text = recognize_speech(converted_temp_file,lang)
                    if recognized_text=='Speech Recognition could not understand the audio':
                        response="Sorry! I couldn't get you."
                        return JsonResponse({'success': True, 'text': recognized_text, 'response': response}, status=200)
                    query=translate_to_english(recognized_text,lang)
                    backend_response = process_query_and_get_response(query)
                    response=translate(backend_response,lang)

                    # Delete the temporary files
                    os.remove(temp_file.name)
                    os.remove(converted_temp_file)

                    return JsonResponse({'success': True, 'text': recognized_text, 'response': response}, status=200)
                else:
                    return JsonResponse({'error': 'No audio file provided'}, status=400)

            except Exception as e:
                return print(e)
        elif 'text' in request.POST:
            try:
                user_text = request.POST['text']

                # Process the text query and get a response
                backend_response = process_query_and_get_response(user_text)

                if "No relevant information found." in backend_response:
                    return JsonResponse({'status': True, 'text': user_text, 'response': backend_response}, status=200)
                else:
                    return JsonResponse({'status': True, 'text': user_text, 'response': backend_response}, status=200)

            except Exception as e:
                return print(e)

        

    return render(request, 'chat.html')

def homepage1(request):
    if request.method == 'POST':
        if 'audio' in request.FILES:
            try:
                lang=request.POST.get('lang')
                audio_file = request.FILES.get('audio')

                if audio_file:
                    # Save the audio file to a temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                    temp_file.write(audio_file.read())
                    temp_file.close()

                    # Convert the audio file to PCM WAV format
                    converted_temp_file = convert_audio_to_wav(temp_file.name)
                    recognized_text = recognize_speech(converted_temp_file,lang)
                    query=translate_to_english(recognized_text,lang)
                    
                    
                    qa_pipeline = pipeline("question-answering",model="bert-large-uncased-whole-word-masking-finetuned-squad")
                    file_path = "chat/space_data_bert.txt"  # Replace with the actual path to your text file
                    with open(file_path, "r", encoding="utf-8") as file:
                        passage = file.read()
                    answer1 = qa_pipeline({"context": passage, "question": query})
                    answer1=answer1['answer']
                    print(answer1)
                    response=translate(answer1,lang)
                    

                    # Delete the temporary files
                    os.remove(temp_file.name)
                    os.remove(converted_temp_file)

                    return JsonResponse({'success': True, 'text': recognized_text, 'response': response}, status=200)
                else:
                    return JsonResponse({'error': 'No audio file provided'}, status=400)

            except Exception as e:
                return print(e)
        elif 'text' in request.POST:
            try:
                user_text = request.POST['text']

                # Process the text query and get a response
                qa_pipeline = pipeline("question-answering",model="bert-large-uncased-whole-word-masking-finetuned-squad")
                file_path = "chat/space_data_bert.txt"  # Replace with the actual path to your text file
                with open(file_path, "r", encoding="utf-8") as file:
                    passage = file.read()
                answer1 = qa_pipeline({"context": passage, "question": user_text})
                answer1=answer1['answer']
                backend_response=answer1
              
                if "No relevant information found." in backend_response:
                    return JsonResponse({'status': True, 'text': user_text, 'response': backend_response}, status=200)
                else:
                    return JsonResponse({'status': True, 'text': user_text, 'response': backend_response}, status=200)

            except Exception as e:
                return print(e)

        

    return render(request, 'chat.html')






def convert_audio_to_wav(input_file_path):
    # Load the input audio file
    audio_data = AudioSegment.from_file(input_file_path)
    # Save the audio data as PCM WAV format
    output_file_path = input_file_path.replace('.wav', '_converted.wav')
    audio_data.export(output_file_path, format='wav')
    return output_file_path

def translate_to_english(text, lang):
    translator = Translator()

    try:
        # Translate the text to English
        translation = translator.translate(text, src=lang, dest='en')
        translated_text = translation.text
        return translated_text

    except Exception as e:
        print(f"Translation error: {e}")
        return text 
    # Return the original text in case of an error
def translate(text,lang):
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    return translation.text


def recognize_speech(audio_file_path,lang):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        if lang=='en':
            text = recognizer.recognize_google(audio_data)
        if lang=='hi':
            text = recognizer.recognize_google(audio_data,language='hi-IN')       
        if lang=='ta':
            text = recognizer.recognize_google(audio_data,language='ta-IN')
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {str(e)}"

def load_space_data(file_path):
    space_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                key, value = line.strip().split('|')
                space_data[key.lower()] = value
            except ValueError:
                a=1

    return space_data
    
def process_query_and_get_response(query):
    # Assuming you have a SpaceBotCLI instance
   

    # Load space data from a file (adjust the path as needed)
    space_database =load_space_data('chat/space_data.txt')

    # Find the most similar question
    best_match = find_most_similar_question(query, space_database.keys())
    
    if best_match is not None:
        return space_database[best_match]
    else:
        return "No relevant information found."

def find_nouns(doc):
    nouns_query = []

    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() not in STOP_WORDS:
            nouns_query.append(porter_stemmer.stem(token.text))
        elif token.pos_ == "PROPN" or token.ent_type_ == "ORG":
            nouns_query.append(token.text.lower())
        elif token.pos_ == "NUM":
            # Include numeric data
            nouns_query.append(token.text)
    return nouns_query
def find_most_similar_question(query, questions):
    # Process the query using spaCy
    doc_query = nlp(query)
    # Extract nouns from the query and filter out non-relevant words
    nouns_query = find_nouns(doc_query)
   
    print("Nouns in Query:", nouns_query)
    # Create a dictionary to store questions based on their stemmed nouns
    questions_dict = []

    for question in questions:
        # Process each question using spaCy
        doc_question = nlp(question)
        # Extract nouns from the question and filter out non-relevant words
        nouns_question = find_nouns(doc_question)
        # Calculate the number of matched nouns
       
        matched_nouns_count =0
        for x in nouns_question:
            if x in nouns_query:
                matched_nouns_count+=1
                
        
        # Append question and matched nouns count to the list
        questions_dict.append((question, matched_nouns_count))
        
    questions_dict.sort(key=lambda x: x[1], reverse=True)
    
    maxm = questions_dict[0][1]
    print(maxm)
# Create a list to store questions with the maximum matched nouns count
    final_questions = [question for question, matched_nouns_count in questions_dict if matched_nouns_count == maxm]

    x = 0.7
    closest_match = None
    
    print(final_questions)
    while x >= 0.1:
        
        for candidate_question in final_questions:
            similarity = calculate_semantic_similarity(query, candidate_question)
            if similarity >= x:
                closest_match = candidate_question
                break 
        x -= 0.1
    print(closest_match)
    return closest_match
def calculate_semantic_similarity(query, question):
    x=nlp(query).similarity(nlp(question))

    return nlp(query).similarity(nlp(question))
