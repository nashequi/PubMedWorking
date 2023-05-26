import os
import xmltodict
import pandas as pd
from tqdm import tqdm

# Set the directory containing your XML files
xml_directory = "/Users/deanshamess/Desktop/PubMed/May25DL"

# Create empty lists to store the extracted information
pmid_list = []
title_list = []
abstract_list = []
cited_pmid_list = []

# Get the total number of XML files for progress tracking
total_files = len([file for file in os.listdir(xml_directory) if file.endswith(".xml")])

# Iterate through each XML file in the directory, parse the XML, and extract the relevant information
for file_name in tqdm(os.listdir(xml_directory), desc="Processing XML files", total=total_files):
    if file_name.endswith(".xml"):
        file_path = os.path.join(xml_directory, file_name)
        with open(file_path, "r") as xml_file:
            data = xmltodict.parse(xml_file.read())
            pubmed_article = data["PubmedArticleSet"]["PubmedArticle"]
            for article in pubmed_article:
                pmid = article["MedlineCitation"]["PMID"]["#text"]
                title = article["MedlineCitation"]["Article"]["ArticleTitle"]
                abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
                
                # Check if the article has cited references
                if "CitationList" in article["MedlineCitation"]:
                    cited_articles = article["MedlineCitation"]["CitationList"]["Citation"]
                    cited_pmids = [cited_article.get("PMID", "") for cited_article in cited_articles]
                else:
                    cited_articles = []
                    cited_pmids = []
                
                pmid_list.append(pmid)
                title_list.append(title)
                abstract_list.append(abstract)
                cited_pmid_list.append(cited_pmids)

# Create a DataFrame with the extracted information
df = pd.DataFrame({
    "PMID": pmid_list,
    "Title": title_list,
    "Abstract": abstract_list,
    "Cited PubMed IDs": cited_pmid_list
})

# Save the DataFrame as a CSV file
df.to_csv("combined_data.csv", index=False)

