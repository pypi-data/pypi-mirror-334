import re
import json
import textstat

def count_approximate_words_and_non_words(text):
    # Conta palavras
    words = re.findall(r'\b\w+\b', text)

    # Conta "não-palavras" (qualquer sequência de caracteres que não seja uma palavra, excluindo espaços)
    non_words = re.findall(r'[^\w\s]+', text)

    return len(words), len(non_words)

def count_approximate_words_non_words_and_tokens(text):
    words,non_words = count_approximate_words_and_non_words(text)

    return words, non_words, int(0.75*(words+non_words))


def generate_word_token_json(text):
    # Contar palavras e tokens
    word_count, no_word_count, token_count = count_approximate_words_non_words_and_tokens(text)
    
    # Criar o dicionário com as contagens
    result = {
        'approximate_word_count': word_count,
        'approximate_no_word_count': no_word_count,
        'approximate_token_count': token_count,
        'character_count': len(text)
    }
    
    # Converter o dicionário para string JSON
    result_json = json.dumps(result, indent=4)
    
    return result_json


def analyze_readability(text: str):
    results = {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "Automated Readability Index (ARI)": textstat.automated_readability_index(text),
        "Coleman-Liau Index": textstat.coleman_liau_index(text),
    }
    
    explanations = {
        "Flesch Reading Ease": f"A score of {results['Flesch Reading Ease']:.2f} means: \n"
                               "- 90-100: Very easy to read (e.g., children's books).\n"
                               "- 60-70: Standard readability (e.g., newspaper articles).\n"
                               "- 0-30: Very difficult to read (e.g., academic papers).",
        
        "Flesch-Kincaid Grade Level": f"A score of {results['Flesch-Kincaid Grade Level']:.2f} suggests the text is suitable for a student in grade {results['Flesch-Kincaid Grade Level']:.2f} out of 16 in the U.S. education system (primary to undergraduate level). Higher scores indicate more complex text.",
        
        "Gunning Fog Index": f"A Gunning Fog Index of {results['Gunning Fog Index']:.2f} suggests that a person needs about {results['Gunning Fog Index']:.2f} years of formal education to easily comprehend the text. In the U.S., this corresponds to a grade level where 12 years represent high school completion.",
        
        "Automated Readability Index (ARI)": f"An ARI score of {results['Automated Readability Index (ARI)']:.2f} suggests the text is suitable for a student in grade {results['Automated Readability Index (ARI)']:.2f} out of 16 in the U.S. system. Higher scores indicate a more complex text, while scores below 5 suggest elementary-level material.",
        
        "Coleman-Liau Index": f"A Coleman-Liau Index score of {results['Coleman-Liau Index']:.2f} approximates the required education level for comprehension. In the U.S. system, a score of 12 represents high school completion (out of 16 years for undergraduate education)."
    }
    
    OUT=""
    for key in results:
        OUT+=key+": "+str(results[key])+"\n"
        OUT+=explanations[key]+"\n"
        OUT+="\n"
    
    return OUT, results
