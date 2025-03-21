# A more generalized filter function by percentage
filter_missing_byPct <- function(data, threshold = 0.7, filter_mode = "either", group_info = NULL) {
  
  if (!filter_mode %in% c("either", "all")) {
    stop("filter_mode must be either 'either' or 'all'")
  }
  
  character_cols <- data %>% select(where(is.character))
  
  numeric_data <- data %>% select(where(is.numeric))
  
  numeric_data %>%
    mutate(across(everything(), ~ as.numeric(as.character(.))))
  
  if (!is.null(group_info)) {
    
    if (length(group_info) != ncol(numeric_data)) {
      stop("Length of group_info must match the number of numeric columns")
    }
    groups <- as.character(group_info)
  } else {
    
    groups <- sub("_.*", "", colnames(numeric_data))
  }
  
  unique_groups <- unique(groups)
  
  group_cols <- split(names(numeric_data), groups)
  
  # Calculate proportion of non-NA values per group for each row
  prop_list <- lapply(group_cols, function(cols) {
    rowSums(!is.na(numeric_data[, cols, drop = FALSE])) / length(cols)
  })
  prop_df <- as.data.frame(prop_list)
  
  # Different mode
  if (filter_mode == "either") {
    keep <- rowSums(prop_df >= threshold) >= 1
  } else { # "all"
    keep <- rowSums(prop_df >= threshold) == length(unique_groups)
  }
  
  # Filter data and get indexes
  filtered_data <- numeric_data[keep, ]
  filtered_out_indexes <- which(!keep)
  
  # Bind back gene and protein info
  character_cols <- character_cols[!(rownames(character_cols) %in% filtered_out_indexes), , drop = FALSE]
  filtered_data <- cbind(character_cols, filtered_data)
  
  return(list(
    filtered_data = filtered_data,
    filtered_out_indexes = filtered_out_indexes,
    group_info = groups
  ))
}