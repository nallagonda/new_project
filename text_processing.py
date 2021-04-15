import spacy
import pandas as pd
import en_core_web_sm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load('en_core_web_sm')

def get_top_n_words(corpus, n=None,stopwords=None):
    if stopwords is not None:
        for word in stopwords:
            nlp.Defaults.stop_words.add(word)
    vec = CountVectorizer(stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]

def compatibility_matrix(resume,jd):
    #print(resume,jd)
    top_words_jd = get_top_n_words(jd.split("\n"))
    print("Job Description top key words:")
    print(top_words_jd)
    top_words_resume = get_top_n_words(resume.split("\n"))
    print("Resume top key words:")
    print(top_words_resume)
    dfJD = pd.DataFrame(top_words_jd, columns = ['Text' , 'count'])
    dfResume = pd.DataFrame(top_words_resume, columns = ['Text' , 'count'])
    dfJD = dfJD.groupby('Text').sum()['count'].sort_values(ascending=False)
    dfResume = dfResume.groupby('Text').sum()['count'].sort_values(ascending=False)
    merged_inner = pd.merge(left=dfResume, right=dfJD, left_on='Text', right_on='Text').fillna(0)
    merged_left_resume = pd.merge(how='left',left=dfResume, right=dfJD, left_on='Text', right_on='Text').fillna(0)
    merged_left_resume = merged_left_resume[merged_left_resume['count_y']==0.0]
    merged_right_jd = pd.merge(how='right',left=dfResume, right=dfJD, left_on='Text', right_on='Text').fillna(0)
    merged_right_jd = merged_right_jd[merged_right_jd['count_x']==0.0]
    print(merged_inner)
    print(merged_left_resume)
    print(merged_right_jd)
    #print(dfResume)
    return merged_inner,merged_left_resume,merged_right_jd

