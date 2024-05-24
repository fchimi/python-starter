#--web true
#--param OPENAI_API_HOST $OPENAI_API_HOST
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--kind python:default

from chat import ChatBot

def main(args):
    key = args.get("OPENAI_API_KEY")
    host = args.get("OPENAI_API_HOST")    
    print(key, host)
    chat= ChatBot(args,key,host)
    print('ddddddddd')
    return chat.chat()
