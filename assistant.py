import time
import re
import random
from openai import OpenAI
import logging
import datetime

log = logging.getLogger("assistant")

logging.basicConfig(filename = "assistant.log", level = logging.INFO)

client = OpenAI()

def process_run(thread_id, assistant_id):
    new_run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )

    phrases = ["Thinking", "Pondering", "Dotting the i's", "Achieving world peace"]

    while True:
        time.sleep(1)
        print(random.choice(phrases) + "...")
        run_check = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check

def log_run(run_status):
    if run_status in ["cancelled", "failed", "expired"]:
        log.error(str(datetime.datetime.now()) + " Run " + run_status + "\n")

def get_message(run_status):
    if run_status == "completed":
        thread_messages = client.beta.threads.messages.list(
            thread_id = thread.id
        )
        message = thread_messages.data[0].content[0].text.value

    if thread_messages.data[0].content[0].text.annotations:
     pattern = r'【\d+†source】'
     message = re.sub(pattern, '', message)
      
   
    if run_status in ["cancelled", "failed", "expired"]:
        message = "An error has occurred, please try again."
    
    return message

# assistant = client.beta.assistants.create(
#     name = "Study Buddy",
#     model = "gpt-3.5-turbo",
#     instructions = "You are a study partner for students who are newer to technology. When you answer prompts, do so with simple language suitable for someone learning fundamental concepts.",
#     tools=[]
# )


assistant = client.beta.assistants.retrieve(assistant_id = "asst_yBNm3208hoAUG7WyIHafZJQL")

# print(assistant)

# file = client.beta.vector_stores.files.create_and_poll(
#  vector_store_id="vs_ncgIdAPHVsn0s9b5L9ruIZqg",
#  file_id="file-qHsYraq9BiSrijt0y1noKeb7"
# )


# vector_store_files = client.beta.vector_stores.files.list(
#     vector_store_id="vs_ncgIdAPHVsn0s9b5L9ruIZqg"
# )
# print (vector_store_files )


# exit()
# exit()
thread = client.beta.threads.create()

user_input = ""

# while True:
#     if (user_input == ""):
#         user_input = input("Assistant: Hello there! Just so you know, you can type exit to end our chat. What's your name? ")



while True:
    if (user_input == ""):
        print("Assistant: Hello there! Just so you know, you can type exit to end our chat. What's your name? ")
        name = input("You: ")
        print("Assistant: Hey, " + name + "! How can I help you?")
        user_input = input("You: ")

# while True:
#     if (user_input == ""):
#         print("Assistant: Hello there! Just so you know, you can type exit to end our chat. What's your name? ")
    else:
        user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        exit()
    
    
    moderation_result = client.moderations.create(
        input = user_input
        )
    
    hate_threshold = 0.98
 
    while moderation_result.results[0].category_scores.hate > hate_threshold or moderation_result.results[0].flagged == True:
        print("Assistant: Sorry, your message violated our community guidelines. Please try a different prompt.")
 
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            exit()
 
        moderation_result = client.moderations.create(
            input = user_input
        )

    
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = user_input
    )

    run = process_run(thread.id, assistant.id)

    log_run(run.status)

    message = get_message(run.status)

    print("\nAssistant: " + message + "\n")
