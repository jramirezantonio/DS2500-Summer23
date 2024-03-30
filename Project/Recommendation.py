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
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
            "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", 
            "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", 
            "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", 
            "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
            "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", 
            "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", 
            "against", "between", "into", "through", "during", "before", "after", "above", 
            "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", 
            "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", 
            "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", 
            "will", "just", "don", "should", "now", "may", "use", "uses"]

responses = ["Hello! How can I help you today?",
            "What's on your mind?",
            "I'm here to assist you. What do you need?",
            "How can I assist you?",
            "What can I help you with?",
            ]
DS = 'DSCourses.txt'
MATH = 'MATHCourses.txt'

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
# import UserInfo
import re
from tkinter import ttk
from tkinter import *
import random

def sort_data(filename):
    courses = {}
    major = ""
    for char in filename:
        if char.islower():
            major = major[:-1]
            major.strip()
            break
        else:
            major = major + char

    with open(filename, 'r', encoding="utf8") as infile:
        for paragraph in infile:
            data = paragraph.strip().split('\n')
            if '' not in data:
                if data[0].startswith(major):
                    course_dict = {}
                    course_title = data[0].split(".")[0]
                    course_dict['title'] = data[0]
                    courses[course_title] = course_dict
                    courses[course_title]['prerequisites'] = ""
                    courses[course_title]['corequisites'] = ""
                    courses[course_title]['attributes'] = ""
                    courses[course_title]['description'] = ""
                elif data[0].startswith('Prerequisite(s):'):
                    courses[course_title]['prerequisites'] = data[0][17:]
                elif data[0].startswith('Corequisite(s):'):
                    courses[course_title]['corequisites'] = data[0][16:]
                elif data[0].startswith('Attribute(s):'):
                    courses[course_title]['attributes'] = data[0][14:]
                else:
                    courses[course_title]['description'] = data[0]
        clean_attributes(courses)
        clean_prereqs(courses)
        return courses

def clean_attributes(courses):
    for course in courses.keys():
        abbrv_attributes = []
        attributes = courses[course]['attributes'].split(", ")
        for attribute in attributes:
            if attribute == "NUpath Analyzing/Using Data":
                abbrv_attributes.append("ad")
            elif attribute == "NUpath Capstone Experience":
                abbrv_attributes.append("ce")
            elif attribute == "NUpath Creative Express/Innov":
                abbrv_attributes.append("ei")
            elif attribute == "NUpath Interpreting Culture":
                abbrv_attributes.append("ic")
            elif attribute == "NUpath Difference/Diversity":
                abbrv_attributes.append("dd")
            elif attribute == "NUpath Ethical Reasoning":
                abbrv_attributes.append("er")
            elif attribute == "NUpath Formal/Quant Reasoning":
                abbrv_attributes.append("fq")
            elif attribute == "NUpath Integration Experience":
                abbrv_attributes.append("ex")
            elif attribute == "NUpath Natural/Designed World":
                abbrv_attributes.append("nd")
            elif attribute == "NUpath Societies/Institutions":
                abbrv_attributes.append("si")
            elif attribute == "NUpath Writing Intensive":
                abbrv_attributes.append("wi")
        courses[course]['attributes'] = abbrv_attributes
    return courses

def clean_prereqs(courses):
    for course in courses:
        prereq = courses[course]['prerequisites']
        temp_prereq = re.sub(r'\(may be taken concurrently\)?', '', prereq)
        temp_prereq = re.sub(r' with a minimum grade of [A-D][+-] ?', '', temp_prereq)
        temp_prereq = re.sub(r'or', ' or', temp_prereq)
        temp_prereq = re.sub(r';', ' and', temp_prereq)
        temp_prereq = re.sub(r'  ', ' ', temp_prereq)
        courses[course]['prerequisites'] = temp_prereq.strip()
    return courses
        
def make_word_list(paragraph):
    """
    Function: Creates a list of words from speeches
    Parameters: speeches, list of strings
    Returns: List of lists of strings
    """
    paragraph = paragraph.strip() # Removing leading/trailing whitespace
    paragraph = re.sub('\[.*\]', '', paragraph) # Remove character heading
    paragraph = re.sub('[^\w\s]', '', paragraph) # Remove punctuation
    paragraph = paragraph.lower() # Convert to lower case
    word_list = word_tokenize(paragraph)
    return word_list

def remove_stop_words(stop_words, paragraph):
    """
    Function: Removes common stop words
    Parameters: stop_words, list of strings of common stop words, speeches, list of strings
    Returns: List of lists of strings
    """
    word_list = make_word_list(paragraph)
    for i in range(len(word_list)-1, -1, -1):
        if word_list[i] in stop_words:
            del word_list[i]
    return word_list

# Convert a list of words to a word vector (code from class)
def vectorize(words, unique):
    return [1 if word in words else 0 for word in unique]

# Vector functions
def mag(v):
    """ magnitude of a vector """
    return sum([i **2 for i in v]) ** 0.5

def dot(u,v):
    """ dot product of two vectors """
    return sum([ui * vi for ui, vi in zip(u,v)])
    
def cosine_similarity(u, v):
    cos_theta = dot(u,v)/(mag(u)*mag(v))
    return cos_theta

def recommend_courses(clean_course_descriptions, user_input):
    """
    Creates a list of recommended courses based on the user input using cosine similarity
    Parameters: clean_course_descriptions - list of course descriptions with a sub list per course containing the
                descriptions with stop words removed
                user_input - string input from the user, to be cleaned in the function
    Returns: a list
    """
    unique = list(set(val for st in clean_course_descriptions.values() for val in st))
    clean_user_input = remove_stop_words(stop_words, user_input)
    user_with_syn = get_synonyms(clean_user_input)
    u = vectorize(user_with_syn, unique)
    recommended_courses = []
    most_sim = 0
    for course in clean_course_descriptions.keys():
        v = vectorize(clean_course_descriptions[course], unique)
        cos_sim = cosine_similarity(u, v)
        if cos_sim > 0:
            most_sim = cos_sim
            recommended_courses.append(course)
    return recommended_courses

def recommendation(user_input, attr_required=False, attr_list=[], prereq_required=False, prereq_list=[],
                   coreq_required=False, coreq_list=[]):
    courses = sort_data(DS)
    clean_course_descriptions = {}
    for key in courses.keys():
        clean_course_descriptions[key] = remove_stop_words(stop_words, courses[key]['description'])
    recommended_courses = []
    if user_input == "":
        for course in courses.keys():
            recommended_courses.append(course)
    else:
        recommended_courses = recommend_courses(clean_course_descriptions, user_input)
    recommended_courses = course_by_attribute(courses, attr_required, attr_list, recommended_courses)
    recommended_courses = course_by_prereq(courses, prereq_required, prereq_list, recommended_courses)
    recommended_courses = course_by_coreq(courses, coreq_required, coreq_list, recommended_courses)
    return recommended_courses

def course_by_attribute(courses, attr_required, attr_list, recommended_courses):
    """
    Checks if the desired attributes are in a recommened class, if they are not the class is not recommended
    Parameters: courses - dictionary of all courses from the northeastern course page
                attr_required - boolean for if the user wants to consider attributes
                attr_list - list of desired attributes
                recommended_courses - courses recommended by our algorithm
    Returns: a list
    """
    if attr_required:
        for course in reversed(recommended_courses):
            check = all(item in courses[course]['attributes'] for item in attr_list)
            if not check:
                del(recommended_courses[recommended_courses.index(course)])
    return recommended_courses

def course_by_prereq(courses, prereq_required, prereq_list, recommended_courses):
    """
    Checks if the user has completed the proper prerequisites to take a recommended course, if they have not the class
    is not recommended
    Parameters: courses - dictionary of all courses from the northeastern course page
                prereq_required - boolean for if the user wants to consider prerequisites
                prereq_list - list of completed courses
                recommended_courses - courses recommended by our algorithm
    Returns: a list
    """
    if prereq_required:
        for course in reversed(recommended_courses):
            prereq_bool = courses[course]['prerequisites'].replace("or", "|").replace("and", "&")
            pattern = r"\b[A-Za-z]+\s\d+\b"
            course_ids = re.findall(pattern, prereq_bool)
            for id in course_ids:
                if id in prereq_list:
                    prereq_bool = prereq_bool.replace(id, "True")
                else:
                    prereq_bool = prereq_bool.replace(id, "False")         
            try:
                check = bool(eval(prereq_bool))
            except (SyntaxError, NameError): # Empty string no prereqs
                check = True
            if not check:
                del(recommended_courses[recommended_courses.index(course)])
    return recommended_courses

def course_by_coreq(courses, coreq_required, coreq_list, recommended_courses):
    """
    Checks if the user has completed the proper corequisites to take a recommended course, if they have not the
     class is not recommended
    Parameters: courses - dictionary of all courses from the northeastern course page
                coreq_required - boolean for if the user wants to consider corequisites
                coreq_list - list of concurrent courses
                recommended_courses - courses recommended by our algorithm
    Returns: a list
    """
    if coreq_required:
        for course in reversed(recommended_courses):
            check = all(item in courses[course]['corequisites'] for item in coreq_list)
            if not check:
                del(recommended_courses[recommended_courses.index(course)])
    return recommended_courses

def get_synonyms(words):
    synonym_list = []
    for word in words:
        wordnet_synset = wn.synsets(word)
        for synset in wordnet_synset:
            for syn_words in synset.lemma_names():
                synonym_list.append(syn_words.lower())
    synonym_set = set(synonym_list + words)
    return list(synonym_set)