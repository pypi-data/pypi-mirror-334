# Normalization against a Single Reference
reference_normalization <- function(reference, data_to_norm) {
  # Initialize data frame
  normalized_data <- data.frame(row.names = rownames(data_to_norm))
  
  character_cols <- data_to_norm %>% select(where(is.character))
  
  numeric_columns <- sapply(data_to_norm, is.numeric)
  
  for (col in which(numeric_columns)) {
    col_name <- names(data_to_norm)[col]
    
    if(col_name %in% colnames(reference)) {
      normalized_data[, col_name] <- data_to_norm[, col_name] / reference[, col_name]
    } else {
      warning(paste("Column", col_name, "not found in reference data"))
    }
  }
  # Bind back gene and protein info
  cbind(character_cols, normalized_data)
  
  return(normalized_data)
}