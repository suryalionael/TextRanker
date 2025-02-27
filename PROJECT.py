import os
import math

#FIRST FUNCTION
#Receiving input menu from user
def printMenu():
    while True:
        print("Menu:")
        print("1. Indexing")
        print("3. Exit")
        choice = input("Please enter 1 for indexing and 3 to exit: ")
        if choice in ["1", "3"]:
            return int(choice)
        else:
            print("Invalid input. Please try again.")

#SECOND FUNCTION
#reading all files in the dataset folder
def readFolderContent():
    folder = "/Users/lionaelsmac/Documents/code/BDP 100/PROJECT/dataset"
    if not os.path.exists(folder):
        print("The dataset folder does not exist.")
    
    files_content = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder, file_name), "r") as file:
                files_content.append(file.read())
    return files_content

#THIRD FUNCTION
#handling the indexing process starting with reading the files, cleaning the text, and generating the index
def indexing():
    contents = readFolderContent()
    termDocFreqFile = "termDocFreqFile.txt"
    if os.path.exists(termDocFreqFile):
        os.remove(termDocFreqFile)

    docID = 1
    for content in contents:
        clean_text = stopWordRemoval(punctuationRemoval(content))
        appendTermDocFreq(clean_text, termDocFreqFile, docID)
        docID += 1

    index = genIndex(termDocFreqFile)
    print("Indexing complete!, Read",len(contents),"Contents")
    return index, len(contents)

#FOURTH FUNCTION
#removing stop words in each file
def stopWordRemoval(text):
    with open("/Users/lionaelsmac/Documents/code/BDP 100/PROJECT/stopWords.txt", "r") as file:
        stopwords = set(file.read().splitlines())
    words = text.split()
    filtered_words = list(filter(lambda word: word.lower() not in stopwords, words))
    return " ".join(filtered_words)

#FIFTH FUNCTION
#removing punctuations in each file
def punctuationRemoval(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    return "".join([char for char in text if char not in punctuations])

#SIXTH FUNCTION
#Appends terms, document ID, and their frequencies to the term document frequency file.
def appendTermDocFreq(cleanText, termDocFreqFile, docID):
    term_freq = {}
    for word in cleanText.split():
        term_freq[word] = term_freq.get(word, 0) + 1

    with open(termDocFreqFile, "a") as file:
        for term, freq in term_freq.items():
            file.write(f"{term} {docID} {freq}\n")

#SEVENTH FUNCTATION
#Generates a global index mapping terms to documents and their frequencies.
def genIndex(termDocFreqFile):
    index = {}
    with open(termDocFreqFile, "r") as file:
        for line in file:
            term, docID, freq = line.strip().split()
            docID, freq = int(docID), int(freq)
            if term not in index:
                index[term] = {}
            index[term][docID] = freq
    return index

#EIGTH FUNCTION
#Seacrh documents that contains the query and ranks them based on TF-IDF scores.
def search(query, index, total_docs):
    query_terms = query.split()
    relevance_scores = {}

    for term in query_terms:
        if term in index:
            for doc_id, freq in index[term].items():
                tf = freq
                df = len(index[term])
                tf_idf = tf * math.log(total_docs / df)
                relevance_scores[doc_id] = relevance_scores.get(doc_id, 0) + tf_idf

    return dict(sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True))

def main():
    index = None
    total_docs = 0

    while True:
        choice = printMenu()
        if choice == 1:
            index, total_docs = indexing()
        elif choice == 3:
            print("Exiting the program.")
            break

        if index:
            query = input("Enter your search query: ")
            results = search(query, index, total_docs)
            if results:
                print("Search Results (Document ID: Score):")
                for doc_id, score in results.items():
                    print(f"Document {doc_id}: {score:.4f}")
            else:
                print("No results found.")

if __name__ == "__main__":
    main()
