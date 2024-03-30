"""
Josue Antonio and Lenon Wong
Test Chatbot for DS2500 Project
"""

"""
Check for pre/corequisites 
Check for class ranges in course number
Credit hours
Match interests in titles/descriptions
Ask user for requirements they want to fill
"""

GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "what's up", "hey", "yo"]
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]
responses = ["Hello! How can I help you today?",
            "What's on your mind?",
            "I'm here to assist you. What do you need?",
            "How can I assist you?",
            "What can I help you with?",
            ]

DS = 'DSCourses.txt'
MATH = 'MATHCourses.txt'

import Recommendation as rec
from tkinter import *
import re

rec_path = False
prereq_path = False
coreq_path = False
attr_path = False
info_path = False
selection = True
end_response1 = False
end_response2 = False
attr_required = False
prereq_required = False
coreq_required = False
attr_list = []
prereq_list = []
coreq_list = []

root = Tk()
root.title("Chatbot")
root.geometry("450x500")
root.resizable(width=FALSE, height=FALSE)

# Create the chatbot's text area
text_area = Text(root, bd=0, bg="white", width=90, height=20)
text_area.pack()

# Create the user's input field
input_field = Entry(root)
input_field.pack()

win_open = True
def chatbot_response(user_input):
    global rec_path, attr_path, prereq_path, coreq_path, info_path, selection, end_response1, end_response2, \
        attr_required, prereq_required, coreq_required, attr_list, prereq_list, coreq_list, selection
    response = ""
    # Different paths based on the user selection
    if end_response1:
        if user_input.lower() == "y":
            response = ("Type 1 for a course recommendation\n" +
                        "Type 2 to set attributes\n" +
                        "Type 3 to set prerequisites\n" +
                        "Type 4 to set corerequisites\n" +
                        "Type 5 to get information about a class\n")
            end_response1 = False
            selection = True
        elif user_input.lower() == "n":
            global win_open
            win_open = False
            root.destroy()

    elif end_response2:
        if user_input.lower() == "y":
            response = "Here are my recommendations:"
            recs = rec.recommendation(user_input="", attr_list=attr_list, prereq_list=prereq_list,
                                      coreq_list=coreq_list, attr_required=attr_required,
                                      prereq_required=prereq_required, coreq_required=coreq_required)
            counter = 0
            for course in recs:
                response = response + " " + course
                counter += 1
                if counter == 3:
                    break
            response = response + "\nWould you like make another selection? (y/n)"
            end_response1 = True
            end_response2 = False
        elif user_input.lower() == "n":
            response = "\nWould you like make another selection? (y/n)"
            end_response1 = True
            end_response2 = False

    elif not selection:
        if rec_path:
            recs = rec.recommendation(user_input, attr_list=attr_list, prereq_list=prereq_list, coreq_list=coreq_list,
                                      attr_required=attr_required, prereq_required=prereq_required,
                                      coreq_required=coreq_required)
            response = "Here are my recommendations:"
            counter = 0
            for course in recs:
                response = response + " " + course
                counter += 1
                if counter == 3:
                    break
            if recs == []:
                reponse = "Sorry, there are no classes in this major that fit your interests"
            response = response + "\nWould you like make another selection? (y/n)"
            rec_path = False
            end_response1 = True
        elif attr_path:
            attr_list = user_input.split()
            for attr in reversed(attr_list):
                if attr not in ["nd", "ei", "ic", "fq", "si", "ad", "dd", "er", "wi", "ex", "ce"]:
                    del(attr_list[attr_list.index(attr)])
            response = "Would you me to make you a recommendation for courses? (y/n)"
            attr_required = True
            attr_path = False
            end_response2 = True
        elif prereq_path:
            pattern = r"\b[A-Za-z]+\s\d+\b"
            prereq_list = re.findall(pattern, user_input)
            response = "Would you me to make you a recommendation for courses? (y/n)"
            prereq_required = True
            prereq_path = False
            end_response2 = True
            # print(prereq_list)
        elif coreq_path:
            pattern = r"\b[A-Za-z]+\s\d+\b"
            coreq_list = re.findall(pattern, user_input)
            response = "Would you me to make you a recommendation for courses? (y/n)"
            coreq_required = True
            coreq_path = False
            end_response2 = True
        elif info_path:
            courses = rec.sort_data(DS)
            user_input = user_input.upper()
            if user_input in courses.keys():
                response = "Here's some information:"
                response += f"\n{courses[user_input]['title']}\n{courses[user_input]['description']}"
                response = response + "\nWould you like make another selection? (y/n)"
                rec_path = False
                end_response1 = True
            else:
                response = "This course doesn't exist!"
                end_response1 = True

    # Selecting different paths to give or receive information about classes
    elif selection:
        if user_input == "1":
            response = "What are you interested in?"
            rec_path = True
            selection = False
        elif user_input == "2":
            response = "What attributes would you like to add?"
            attr_path = True
            selection = False
        elif user_input == "3":
            response = "What prerequisites would you like to add?"
            prereq_path = True
            selection = False
        elif user_input == "4":
            response = "What corequisites would you like to add?"
            coreq_path = True
            selection = False
        elif user_input == "5":
            response = "What course would you like to learn about?"
            info_path = True
            selection = False
        else:
            response = ("Please respond with a valid number.\n" +
                        "Type 1 for a course recommendation\n" +
                        "Type 2 to set attributes\n" +
                        "Type 3 to set prerequisites\n" +
                        "Type 4 to set corequisites\n" +
                        "Type 5 to get information about a class\n")
    return response
    
def send_message():
    # Get the user's input
    user_input = input_field.get()

    # Clear the input field
    input_field.delete(0, END)

    # Generate a response from the chatbot
    response = chatbot_response(user_input)

    # Display the response in the chatbot's text area
    text_area.insert(END, f"User: {user_input}\n")
    text_area.insert(END, f"Chatbot: {response}\n")
    text_area.yview(END)


if win_open:
    text_area.insert(END, f"Chatbot: Hello there!\n" +
                            "Type 1 for a course recommendation\n" +
                            "Type 2 to set attributes\n" +
                            "Type 3 to set prerequisites\n" +
                            "Type 4 to set corequisites\n" +
                            "Type 5 to get information about a class\n")
    # Create the send button
    send_button = Button(root, text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",
                         fg='#ffffff',
                         command=lambda: send_message())
    send_button.pack()
    quit_button = Button(root, text="Quit", width=12, height=5, bd=0, bg="#de3232", activebackground="#3c9d9b",
                         fg='#ffffff',
                         command=lambda: root.destroy())
    quit_button.pack()
    root.bind('<Return>', lambda x: send_message())
    text_area.place(x=6, y=6, height=386, width=440)
    send_button.place(x=6, y=401, height=45)
    quit_button.place(x=6, y=450, height=45)
    input_field.place(x=100, y=401, height=95, width=345)
    root.mainloop()

# Chatbot code
    # if attr_path:
    #     user_input = user_input.split()
    #     for attr in user_input:
    #         if attr not in ["nd", "ei", "ic", "fq", "si", "ad", "dd", "er", "wi", "ex", "ce"]:
    #             del(user_input[user_input.index(attr)])
    #     attr_list = user_input
    #     recs = recommendation(user_input = "", attr_list=attr_list, attr_required=True)
    #     response = "Here are my recommendations:"
    #     counter = 0
    #     for course in recs:
    #         response = response + " " + course
    #         counter += 1
    #         if counter == 3:
    #             break
    #     attr_path = False

    # for word in get_synonyms(["class", "recommend", "learn"]):
    #     if word in user_input.lower():
    #         recs = recommendation(user_input)
    #         response = "Here are my recommendations:"
    #         counter = 0
    #         for course in recs:
    #             response = response + " " + course
    #             counter += 1
    #             if counter == 3:
    #                 break
    #         return response
    
    # for word in get_synonyms(["attributes", "nupath"]):
    #     if word in user_input.lower():
    #         response = "What attributes do you need to fulfill?"
    #         attr_path = True            
    #         return response
    # else:
    #     return random.choice(responses)