from langdetect import detect, DetectorFactory, LangDetectException
import langid
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from time import sleep


def connection_db():
    # Connexion à MongoDB avec vérification
    try:
        mongo_client = MongoClient(
            'mongodb://root:root@mongo:27018/?compressors=disabled&gssapiServiceName=mongodb', serverSelectionTimeoutMS=5000)
        mongo_client.server_info()  # Vérification de la connexion
        print("Connexion à MongoDB réussie.")
        mongo_db = mongo_client['comments_db']
        mongo_collection = mongo_db['comments']
        return mongo_collection
    except ServerSelectionTimeoutError as e:
        print("Erreur de connexion à MongoDB :", e)
        exit(1)


def data_process(data):
    # List to collect comment data
    comment_data = []
    try:
        for i, record in enumerate(data):
            # print(record)
            # sleep(5)
            try:
                # Process YouTube comments
                for item in record["items"]:
                    comment_snippet = item['snippet']['topLevelComment']['snippet']
                    comment_text = clean_unicode_escape(comment_snippet['textOriginal'])
                    comment_data.append({
                        "source": item['snippet']['topLevelComment']["kind"].split('#')[0],
                        "textOriginal": comment_text,
                        "likeCount": comment_snippet.get('likeCount', 0),
                        "channelId": comment_snippet.get('channelId', ''),
                        "publishedAt": comment_snippet.get('publishedAt', '')
                    })
            except KeyError:
                # Process New York Times abstracts
                for item2 in record["docs"]:
                    comment_data.append({
                        "source": "nytime",
                        "textOriginal": item2.get('textOriginal', ''),
                        "likeCount": None,
                        "channelId": None,
                        "publishedAt": item2.get('publishedAt', '')
                    })
        print("data processing done successfully! : ", len(comment_data))

        return comment_data
    except Exception as e:
        print("An error ocured during processing ", e)

# Fonction pour écrire dans MongoDB

import re

def clean_unicode_escape(text):
    # Replace all unicode escape sequences like \u003c with their corresponding characters
    cleaned_text = re.sub(r'\\u[0-9a-fA-F]{4}', lambda match: chr(int(match.group()[2:], 16)), text)
    
    # You can extend this step if you want to remove specific characters like '<' or '>'
    # For now, we just remove characters like '<' or '>'
    cleaned_text = cleaned_text.replace('<', '').replace('>', '')
    
    return cleaned_text

# Fix seed for langdetect to ensure consistent results
DetectorFactory.seed = 0

def write_to_mongo(mongo_collection, comments):
    for comment in comments:
        text = comment.get("textOriginal", "").strip()  # Assure that "textOriginal" exists and is not empty
        if not text:
            print("Skipping empty or invalid comment:", comment)
            continue

        try:
            # Detect language using both langid and langdetect
            language1, confidence = langid.classify(text)
            language2 = detect(text)
        except LangDetectException as e:
            print("Language detection failed for comment: ",text,". Error: ",str(e))
            continue

        # Check if the comment is in English based on the detected language
        if language1 == 'en' or language2 == 'en':
            try:
                mongo_collection.insert_one(comment)
                print("Comment added successfully!")
            except Exception as db_error:
                print("Failed to insert comment into MongoDB. Error: ",str(db_error))
        else:
            print("Non-English comment skipped:", text)

