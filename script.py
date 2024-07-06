import sys
!{sys.executable} -m pip install rdflib
!{sys.executable} -m pip install nltk
!{sys.executable} -m pip install SPARQLWrapper
from rdflib import Graph
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Download NLTK data (stopwords and punkt)
nltk.download('stopwords')
nltk.download('punkt')
# Load the RDF graph
graph = Graph()
graph.parse("./car-defects-ontology.rdf")

# Define a function to execute SPARQL queries
def execute_query(graph, query):
    result = graph.query(query)
    for row in result:
        print(row)

# Function to extract keywords from symptom description
def extract_keywords(description):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(description)
    filtered_words = [w for w in word_tokens if w.isalnum() and not w in stop_words]
    return filtered_words

# Function to generate a SPARQL query based on keywords
def generate_sparql_query(keywords):
    # Constructing the filter conditions using CONTAINS and LCASE
    filter_conditions = ' '.join([f'FILTER (CONTAINS(LCASE(?symptomTitle), "{keyword.lower()}"))' for keyword in keywords])
    # Constructing the SPARQL query with variable defect
    query = f"""
        PREFIX car: <http://www.example.com/car#>
        
        SELECT ?symptomTitle ?symptomDescription ?defectName
        WHERE {{
          # Filter by symptom title with CONTAINS and LCASE for case-insensitive matching
          {filter_conditions}
        
          # Search only against symptomTitle
          ?symptom car:symptomTitle ?symptomTitle .
          
          # Link symptom to defect through isSymptomOf
          ?symptom car:isSymptomOf ?defect .
          
          # Retrieve defect name
          ?defect car:defectName ?defectName .
          ?symptom car:symptomDescription ?symptomDescription
        }}
    """
    return query

# Example symptom description
symptom_description = "Clunk sound"

# Extract keywords from the symptom description
keywords = extract_keywords(symptom_description)

# Generate the SPARQL query
query = generate_sparql_query(keywords)

# Execute the query
execute_query(graph, query)
