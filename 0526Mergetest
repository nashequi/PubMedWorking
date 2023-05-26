#packages
library(xml2)
library(dplyr)


#Function to extract from a single XML
extract_xml_info <- function(file_path) {
  xml <- read_xml(file_path)
  
  # Extract PubMed ID
  pmid_node <- xml_find_first(xml, "//ArticleId[@IdType='pubmed']")
  pmid <- if (!is.null(pmid_node)) {
    xml_text(pmid_node)
  } else {
    NA
  }
  
  # Extract article title
  title_node <- xml_find_first(xml, "//ArticleTitle")
  title <- if (!is.null(title_node)) {
    xml_text(title_node)
  } else {
    NA
  }
  
  # Extract cited articles
  citations <- xml_find_all(xml, "//PubmedArticleSet/PubmedArticle/PubmedData/ReferenceList/Reference/ArticleId[@IdType='pubmed']")
  cited_pmids <- if (length(citations) > 0) {
    xml_text(citations)
  } else {
    NA
  }
  
  # Create a dataframe
  data.frame(PMID = pmid, Title = title, Cited_PMIDs = cited_pmids, stringsAsFactors = FALSE)
}


#Empty df to store info
combined_df <- data.frame(PMID = character(),
                          Title = character(),
                          Cited_PMIDs = character(),
                          stringsAsFactors = FALSE)


#iterate over XMLs and add to the df
xml_files <- list.files("/Users/deanshamess/Desktop/PubMed/Raw", pattern = "*.xml", full.names = TRUE)

for (file in xml_files) {
  df <- extract_xml_info(file)
  combined_df <- bind_rows(combined_df, df)
}


# Replace "output.csv" with the desired file path and name
output_file <- "/Users/deanshamess/Desktop/PubMed/mergetest.csv"

# Export the dataframe as a CSV file
write.csv(combined_df, file = output_file, row.names = FALSE)
