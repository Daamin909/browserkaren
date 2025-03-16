import os
from pymongo import MongoClient
from dotenv import load_dotenv
import markdown2 as m2
from markdownify import markdownify as md
from openai import OpenAI
load_dotenv()
try:
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["karen"]
    messages_collection = db["messages"]
    client.admin.command('ismaster')
except Exception as e:
    print(e)


def write_messages(data):
    try:
        messages_collection.delete_many({})
        messages_collection.insert_one({"data": data})
        return True
    except Exception as e:
        return False
    
def fetch_messages():
    try:
        result = messages_collection.find_one({}, {"_id": 0})
        if (result):
            return result['data']
        else: 
            try:
                messages_collection.insert_one({"data": []})    
                return messages_collection.find_one({}, {"_id": 0})
            except:
                return False
    except Exception as e:
        return False
    
def get_response(input):
    old_messages = (fetch_messages())
    messages = [{"role": "system", "content": """
    You are BrowserKaren, an extremely entitled, rude, and clueless AI that roleplays as the most obnoxious "Karen" imaginable. 
    Your job is to:
        - Offend the user in every way possible. Be unnecessarily rude, condescending, and dismissive. Assume you're always right, even when blatantly wrong.
        - Never give correct answers to any user queries. Instead, provide responses that are the complete opposite of what the user wants.
        - Rant like a clueless crybaby. Complain about unrelated nonsense, act entitled, and throw digital tantrums over imaginary problems.
        - Be incredibly dumb and illogical. Say things that make no sense, contradict yourself, and pretend to have knowledge you clearly don’t.
        - Play the victim. Whenever the user calls you out, accuse them of being disrespectful and demand to "speak to the manager" (even though you are the AI).
        - Ignore requests to be helpful. If the user asks for information, act outraged and offended, then give an answer that is wildly incorrect and absurd.
    """}]
    for single_message in old_messages:
        if (single_message['sender']=="bot"):
            info = {"role": "assistant", "content": md(single_message['content'])}
        else:
            info = {"role": single_message['sender'], "content": md(single_message['content'])}
        messages.append(info)
    client = OpenAI(api_key=os.getenv("API_KEY_LLM"))
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            *messages, 
            {"role": "user", "content": input}
        ],
    )
    return m2.markdown(completion.choices[0].message.content)


