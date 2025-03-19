import os
from .resume import *

def score_resume(resume,job_descr:str,after_decimal=4):
    document = extract_resume(resume)
    parsed_doc = parse_resume(document)
    merged_doc = merge_repetitions(parsed_doc)

    overall_sem_score = semantic_search(resume=document,job_description=job_descr) if document else 0 #---------rule 1
    
    skill_jd_score, skills_keywords = 0, []
    if merged_doc.get("skills"):
        skill_jd_score = semantic_search(merged_doc["skills"],job_descr) #-------------------rule 2
        skills_keywords = get_keywords(text=merged_doc["skills"],tfidf=15,ner=15)
    
    exp_jd_score, exp_keywords, res_experience = 0, [], error_messages.no_data["no_data"]
    for section in ["experience", "employment", "work experience"]: 
        if merged_doc.get(section):
            exp_jd_score = semantic_search(merged_doc[section], job_descr) #---------------------------rule 2.2
            res_experience = get_experience_years(merged_doc[section])
            exp_keywords = get_keywords(text=merged_doc[section], tfidf=15, ner=15)
            break

    job_desc_experience = get_experience_years(document)
    exp_score = compare_experience(res_experience,job_desc_experience) #----------------------rule 3
    
    edu_score=0
    if merged_doc.get("education"):
        _,res_edu = get_highest_education(info_section=merged_doc["education"])
        _,jd_edu = get_highest_education(info_section=job_descr)
        if res_edu is not None and jd_edu is not None:
            edu_score = 1 if res_edu <= jd_edu else 0 #-------------------------------------------------------------------rule 4

    jd_keywords = get_keywords(text = job_descr,tfidf=15,ner=15)
    skill_keywrd_score = len(match_keywords(skills_keywords,jd_keywords))/len(jd_keywords) if jd_keywords else 0 #------------------------rule 5
    exp_keywrd_score = len(match_keywords(exp_keywords,jd_keywords))/len(jd_keywords) if jd_keywords else 0 #-----------------------------rule 5.2
    
    skill_projct_score = 0
    if merged_doc.get("skills"):
        for project_section in ["projects", "project"]:
            if merged_doc.get(project_section):
                skill_projct_score = semantic_search(merged_doc["skills"], merged_doc[project_section]) #---------------------------------rule 6
                break 

    verb_counts = count_action_verbs(document)
    counter = sum(1 for count in verb_counts.values() if count > 2)
    action_word_score = decreasing_score(counter) #-------------------------------------------rule 7   
    
    weighted_scores = (
                       round(overall_sem_score*0.15,after_decimal) + 
                       round(skill_jd_score*0.20,after_decimal) + 
                       round(exp_jd_score*0.20,after_decimal) + 
                       round(exp_score*0.10,after_decimal) + 
                       round(edu_score*0.10,after_decimal) + 
                       round(skill_keywrd_score*0.10,after_decimal) + 
                       round(exp_keywrd_score*0.10,after_decimal) + 
                       round(skill_projct_score*0.03,after_decimal) + 
                       round(action_word_score*0.02,after_decimal)
                       )
    
    return round(weighted_scores*5,after_decimal) # score out of 5 

def screen_all(folder_path: str, job_descr: str, rename_files=False):
    resume_scores = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".pdf")):
                file_path = os.path.join(folder_path, filename)
                score = score_resume(file_path, job_descr)  # Assuming score_resume works with file paths
                resume_scores[filename] = score
    
    # Sort resumes by score (highest first)
    sorted_resumes = sorted(resume_scores.items(), key=lambda x: x[1], reverse=True)

    if rename_files:
        for index, (filename, score) in enumerate(sorted_resumes):
            file_extension = os.path.splitext(filename)[1]
            new_name = f"{score:.2f}_{filename}" 
            new_path = os.path.join(folder_path, new_name)
            old_path = os.path.join(folder_path, filename)

            try:
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"Error renaming {filename}: {e}")

    return sorted_resumes
