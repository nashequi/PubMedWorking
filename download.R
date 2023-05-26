library(RCurl)

# Create a local directory to store the downloaded files
setwd("/Users/deanshamess/Desktop/PubMed/May25DL/")

# Function to download files
download_files <- function(url) {
  # Retrieve the directory listing
  listing <- getURL(url, ftp.use.epsv = FALSE, dirlistonly = TRUE)
  
  # Split the listing into individual file names
  file_names <- strsplit(listing, "\r?\n", perl = TRUE)[[1]]
  
  # Filter out directories and parent directory links
  file_links <- file_names[!grepl("/$", file_names) & !grepl("\\.\\./", file_names)]
  
  # Download files
  for (file_link in file_links) {
    file_url <- paste0(url, file_link)
    file_name <- basename(file_link)
    cat("Downloading:", file_name, "\n")
    
    # Retry download with increased timeout duration
    success <- FALSE
    while (!success) {
      tryCatch({
        download.file(file_url, destfile = file_name, timeout = 120)
        success <- TRUE
      }, error = function(e) {
        cat("Error:", conditionMessage(e), "\n")
        cat("Retrying:", file_name, "\n")
      })
    }
    
    cat("Downloaded:", file_name, "\n")
  }
}

# URL of the directory containing the files
directory_url <- "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"



# Call the function to download the files
download_files(directory_url)
