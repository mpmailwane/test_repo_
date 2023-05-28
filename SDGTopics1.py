
import streamlit as st
import streamlit.components.v1 as components
# import pyLDAvis
# import pyLDAvis.gensim_models as gensimvis
# from gensim.models.ldamulticore import LdaMulticore
# from gensim.corpora import Dictionary
# import pickle

def display_pyldavis():
    # Path where LDA model, corpus, dictionary, topic visualization are saved  
    folder_path = r'C:\\Users\\Phoebe\\Desktop\\New_folder\\LDAModel Files\\'
    
    # Load the saved LDA model
    # lda_model = LdaMulticore.load(folder_path + 'saved_LDAmodel.model', mmap='r')
    
    # # Load the saved corpus    
    # with open(folder_path + 'saved_corpus.pkl', 'rb') as f:
    #     all_corpus = pickle.load(f)
        
    # # Load the saved dictionary
    # dictionary = Dictionary.load(folder_path + 'saved_dict.pkl')
    
    # load the saved topic visualization in html 
    with open(folder_path +'lda_image.html', 'r') as f:
        html_string = f.read()
        
    components.html(html_string, width=1300, height=800, scrolling=False)

def main():
    st.title("SDG Topic Analysis")

    # Display the pyLDAvis visualization
    display_pyldavis()

    
# Run the app
if __name__ == '__main__':
    main()