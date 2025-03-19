import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from sentence_transformers import SentenceTransformer
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from datetime import datetime
from copy import deepcopy
#custom import
from . import error_messages

#Universal container/cacher for loading models and avoiding reloads
model_load_cache = {}

def get_name(resume_text:str)->str:
    name_pattern = re.findall(
        r'(?i)^(?:[A-Z][a-z\'-]+(?:\s[A-Z][a-z\'-]+)*)', resume_text, re.MULTILINE)
    name = name_pattern[0] if name_pattern else error_messages.no_sections["name"]
    return name
        
def get_phone_number(resume:str)->str:
    phone_pattern = re.findall(r'\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{3,4}', resume)
    if phone_pattern:
        phone_numbers = ", ".join(phone_pattern)  # Join multiple numbers as a string
    else:
        phone_numbers = error_messages.no_sections["phone"]
    return phone_numbers

def get_email(resume:str)->str:
    email_pattern = re.findall(r'[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+', resume)
    if email_pattern:
        email = phone_numbers = ", ".join(email_pattern)
    else:
        email = error_messages.no_sections["email"]
    return email

def get_experience(resume:str)->str:
    experience_pattern =  re.compile(
        r"(?i)(?:Experience|Work Experience|Employment|Professional Experience)\s*(.*?)(?=\n(?:Education|Skills|awards|employment|interests|summary|contributions|references|Projects|Project Work|Project|Certifications|$))"
        ,re.DOTALL)
    experience_search = experience_pattern.search(resume)
    experience = experience_search.group(1).strip() if experience_pattern else error_messages.no_sections["experience"]
    return experience

def get_skills(resume:str)->str:
    skills_pattern = re.compile(
        r"(?i)(?:Skills|Technical Skills|Relevant Skills)\s*(.*?)(?=\n(?:Experience|Work Experience|Professional Experience|Education|awards|employment|interests|summary|contributions|references|Projects|Project Work|Project|Certifications|$))",
        re.DOTALL
    )
    skills_search = skills_pattern.search(resume)
    skills = skills_search.group(1).strip() if skills_search else error_messages.no_sections["skills"]
    return skills

def get_education(resume:str)->str:
    education_pattern = re.compile(
        r"(?i)(?:Education|Academic Background|Qualifications)\s*(.*?)(?=\n(?:Experience|Work Experience|Professional Experience|Skills|awards|employment|interests|summary|contributions|references|Projects|Project Work|Project|Certifications|$))",
        re.DOTALL
    )
    education_search = education_pattern.search(resume)
    education = education_search.group(1).strip() if education_search else error_messages.no_sections["education"]
    return education

def get_projects(resume:str)->str:
    project_pattern = re.compile(
        r"(?i)(?:Project Work|Projects|Project)\s*(.*?)(?=\n(?:Experience|Work Experience|Professional Experience|Education|Skills|awards|employment|interests|summary|contributions|references|Certifications|$))",
        re.DOTALL
    )
    project_search = project_pattern.search(resume)
    project = project_search.group(1).strip() if project_search else error_messages.no_sections["projects"]
    return project

def get_custom_section(resume:str, section_name: str, variations: list):
    custom_pattern = re.compile(
        rf"(?i)\b(?:{'|'.join(map(re.escape, variations))})(?:\s*(?:and|&|/)\s*\w+)*\b\s*(.*?)(?=\n(?:"
        r"Experience|Work Experience|Professional Experience|Education|Skills|Projects|project work|project|"
        r"Employment|Interests|Summary|certificates|Contributions|References|Certifications|Awards|$))",
        re.DOTALL
    )
    match = custom_pattern.search(resume)
    return match.group(1).strip() if match else f"{section_name} section not found."

def get_experience_years(experience_section:str):
    year_pattern = r'\b(19\d{2}|20\d{2})\b'
    month_pattern = r'\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b'

    # Extract years and months
    years = sorted(set(map(int, re.findall(year_pattern, experience_section))))
    months = re.findall(month_pattern, experience_section, re.IGNORECASE)

    if not years:
        return error_messages.no_data["no_data"] #------------------------------fixed format of output
    
    start_year, end_year = years[0], years[-1]
    
    #determine range using months
    start_month = months[0] if months else "January"
    end_month = months[-1] if len(months) > 1 else "December"

    #month names to numbers
    month_map = {m[:3].lower(): i+1 for i, m in enumerate([
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ])}

    start_month_num = month_map[start_month[:3].lower()]
    end_month_num = month_map[end_month[:3].lower()]

    #experience duration
    start_date = datetime(start_year, start_month_num, 1)
    end_date = datetime(end_year, end_month_num, 1)
    delta = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    years_exp = delta // 12
    months_exp = delta % 12
    if years_exp < 0:
        years_exp = 0
    if months_exp < 0:
        months_exp = 0
    return f"{years_exp} year(s) and {months_exp} month(s)" #-------------------fixed format of output

def get_company_names(info_section:str, spacy_model = "en_core_web_md" ):
    if spacy_model not in model_load_cache:
        model_load_cache[spacy_model] = spacy.load(spacy_model)
    
    model = model_load_cache[spacy_model]
    doc = model(info_section)
    companies = []
    for entity in doc.ents:
        if entity.label_=="ORG" and entity.text.strip("● / + ") not in companies:
            companies.append((entity.text))
    if companies:
        return companies
    else:
        return error_messages.no_data["company_data"]

def get_highest_education(info_section: str):
    education_keywords = [
        "phd", "doctorate", "doctor of philosophy",
        "master", "msc", "ma", "mba", "m.tech", "m.e.",
        "bachelor", "bsc", "ba", "b.tech", "b.e.", "bba",
        "diploma", "associate"
    ]
    pattern = r'\b(' + '|'.join(re.escape(edu) for edu in education_keywords) + r')\b'
    matches = re.findall(pattern, info_section, re.IGNORECASE)
    if matches:
        highest_edu = min(matches, key=lambda x: education_keywords.index(x.lower()))
        return highest_edu, education_keywords.index(highest_edu.lower())
    else:
        return error_messages.no_data["education_data"],len(education_keywords)
    
def get_university_name(info_section: str, words_b4_keywords = 5,words_after_keywords=2,add_keywords:str = None ):
    
    if add_keywords == None:
        university_keywords = ["University", "Institute", "College", "School", "Academy", "Polytechnic"]
    else:
        university_keywords.append(add_keywords)
        
    pattern = (
        r'((?:\S+\s+){0,' + str(words_b4_keywords) + r'}'  # Up to 5 words before
        r'(?:' + '|'.join(university_keywords) + r')'  # University keyword
        r'(?:\s+\S+){0,' + str(words_after_keywords) + r'})'  # Up to 2 words after
    )
    matches = re.findall(pattern, info_section, re.IGNORECASE)
    if not matches:
        return error_messages.no_data["university_data"]
    return matches

def get_keywords(text:str, tfidf=10,ner=10, ner_model="en_core_web_sm"):
    """Extracts keywords using both TF-IDF and Named Entity Recognition (NER)."""

    if not text.strip():  # to handle empty text
        return []
    
    # TF-IDF Extraction
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        tfidf_keywords = [word for word, _ in sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)][:tfidf]
    except ValueError:  # Catch TF-IDF errors for short/empty text
        tfidf_keywords = []

    # NER Extraction
    if ner_model not in model_load_cache:
        model_load_cache[ner_model] = spacy.load(ner_model)
    doc = model_load_cache[ner_model](text)
    ner_keywords = list({ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE", "NORP"]})[:ner]
    
    combined_keywords = set(tfidf_keywords).union(set(ner_keywords))
    return list(combined_keywords)

def match_keywords(list1:list,list2:list, ignore_case:bool = True):
    if ignore_case:
        list1, list2 = set(map(str.lower, list1)), set(map(str.lower, list2))
    else:
        list1, list2 = set(list1), set(list2)
    return list(list1.intersection(list2))

def extract_resume(resume):
    doc = pdfplumber.open(resume)
    text = doc.pages
    corpus =""
    for i in text:
        page_text = i.extract_text(x_tolerance = 2)
        if page_text:
            corpus += page_text + "\n"
    doc.close() 
    return corpus.strip()

def parse_resume(extracted_resume :str, extra_sections:list = None, regex_parse:bool = False, merge_repetition = False):
    sections = ["skills","references","project","projects","work experience","experience","employment", 
                "education" ,"interests", "contributions","contribution","awards",
                "summary","certifications"]
      
    if extra_sections:
        sections.extend(map(str.lower,extra_sections))
    
    group = {}

    if regex_parse == False:
        tokens = word_tokenize(extracted_resume)
        prev_token = "personal information"
        updater = ""
        section_counter = 1

        for token in tokens:
            token_lower = token.lower()
            
            if token_lower not in sections:
                updater = updater + " " + token
                group[prev_token] = updater.strip()
            else:
                if token_lower in group:
                    section_counter += 1
                    token_lower = token_lower+str(section_counter)
                
                group[token_lower] = ""
                updater = ""
                prev_token = token_lower
        
        if merge_repetition:
            for key in list(group):
                group = merge_repetitions(group, section=key)
    
    else:
        group.update({"name":get_name(extracted_resume),
                    "email":get_email(extracted_resume),
                    "phone":get_phone_number(extracted_resume),
                    "skills":get_skills(extracted_resume),
                    "experience":get_experience(extracted_resume),
                    "projects":get_projects(extracted_resume),
                    "education":get_education(extracted_resume)
                    })    
    return group
        
def check_repetitions(parsed_resume:dict,section:str):
    count = 0
    for key in parsed_resume.keys():
        if key.startswith(section.lower()):
            count += 1
    return count

def merge_repetitions(parsed_resume: dict, section: str = None) -> dict:
    new_parsed_data = deepcopy(parsed_resume)
    merged_data = {}
    keys_to_remove = set()

    keys = new_parsed_data.keys()
    if section:  
        # If section- only merge keys that start with the given section
        relevant_keys = [key for key in keys if key.startswith(section)]
    else:
        # If no section- consider all keys for merging
        relevant_keys = keys

    for key in relevant_keys:
        for other_key in relevant_keys:
            if key != other_key and key.startswith(other_key):
                merged_data.setdefault(other_key, []).extend(new_parsed_data[key])
                keys_to_remove.add(key)

    for key, values in merged_data.items():
        new_parsed_data[key] = "".join(values) 

    for key in keys_to_remove:
        new_parsed_data.pop(key, None)

    return new_parsed_data


def semantic_search(resume:str,job_description:str,sentence_transformer_model = "paraphrase-MiniLM-L3-v2"):
    if not resume or not job_description: 
        return 0

    try:
        if sentence_transformer_model not in model_load_cache: 
            model_load_cache[sentence_transformer_model] = SentenceTransformer(sentence_transformer_model)
        '''model_load_cache is the universal cacher for
            loading and storing models temporarily'''
        senc= model_load_cache[sentence_transformer_model].encode(resume)
        jenc = model_load_cache[sentence_transformer_model].encode(job_description)
        senc=np.reshape(senc,(1,-1))
        jenc=np.reshape(jenc,(1,-1))
        sim = model_load_cache[sentence_transformer_model].similarity(senc,jenc)
        val = sim.numpy().astype(float)
        set_range = (val + 1)/2 #normalizing 0-opp. meaning, 0.5-no similarity, 1-completely similar
        return set_range.item()
    
    except Exception as e:
        print(f"Error loading model or computing similarity: {e}. \n Kindly fix the error before recomputing as the score obtained is not valid !!")
        return 0
    
def count_action_verbs(text:str):
    if not text.strip():  # Handle empty input
        return {}

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    pos_tags = pos_tag(words)
    action_verbs = [word for word, tag in pos_tags if tag.startswith('VB') and word not in stop_words]
    verb_counts = {}
    for verb in action_verbs:
        if verb in verb_counts:
            verb_counts[verb] += 1
        else:
            verb_counts[verb] = 1  
    return verb_counts

def compare_experience(resume_experience_years: str, required_experience_years: str):
    if resume_experience_years == error_messages.no_data["no_data"] or required_experience_years == error_messages.no_data["no_data"]:
        return 0
    resume_experience_years = resume_experience_years.replace("year(s)", "").replace("month(s)", "").replace("and", "").strip()
    required_experience_years = required_experience_years.replace("year(s)", "").replace("month(s)", "").replace("and", "").strip()
    y1, m1 = map(int, resume_experience_years.split())
    y2, m2 = map(int, required_experience_years.split())
    #everything to months
    resume_months = y1 * 12 + m1
    required_months = y2 * 12 + m2

    return 0 if resume_months < required_months else 1

def decreasing_score(x,k=2):
    return 1 / (1 + np.exp(x - k))