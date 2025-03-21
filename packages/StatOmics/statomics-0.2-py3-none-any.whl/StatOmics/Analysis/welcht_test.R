## Welch's t-test and BH method
run_welcht_tests <- function(data, group_info) {
  # get character columns (e.g., Protein and Genes)
  character_cols <- data %>% select(where(is.character))
  
  # group_info is a logical vector with the same length as the number of numeric columns
  group_info <- unname(unlist(group_info))
  group_values <- unique(group_info)
  
  if (length(group_values) != 2) {
    stop("There must be exactly 2 groups for t-test. Found: ", paste(group_values, collapse = ", "))
  }
  
  numeric_cols <- sum(sapply(data, is.numeric))
  if (length(group_info) != numeric_cols) {
    stop(paste("group_info must be a logical vector with same length as numeric columns."))
  }
  
  # Create a logical vector for subsetting
  is_group1 <- group_info == group_values[1]
  
  # Separate data into group 1 and group 2 based on group_info
  numeric_data <- data %>% select(where(is.numeric))
  
  group1_data <- numeric_data[, is_group1, drop = FALSE]
  group2_data <- numeric_data[, !is_group1, drop = FALSE]
  
  # Initialize results dataframe
  results <- data.frame(
    Protein = character(),
    t_statistic = numeric(),
    p_value = numeric(),
    mean_difference = numeric(),
    log2_fold_change = numeric(),
    stringsAsFactors = FALSE
  )
  
  # do t test for each feature
  for (i in 1:nrow(data)) {
    protein <- data[i, 1]  # First column is the protein identifier
    
    # Extract values for group 1 and group 2
    group1_values <- as.numeric(group1_data[i, ])
    group2_values <- as.numeric(group2_data[i, ])
    
    # Perform t-test
    t_test_result <- tryCatch({
      test <- t.test(group2_values, group1_values, alternative = "two.sided", var.equal = FALSE)
      c(test$statistic, test$p.value, diff(test$estimate))
    }, error = function(e) {
      c(NA, NA, NA)
    })
    
    # Calculate log2-Fold
    log2_fc <- tryCatch({
      
      if (group_values[1] == "Control" || group_values[1] == "control") {
        
        result <- mean(as.numeric(unlist(group2_values))) / mean(as.numeric(unlist(group1_values)))
        
      } else {
        
        result <- mean(as.numeric(unlist(group1_values))) / mean(as.numeric(unlist(group2_values)))
        
      }
      
    }, error = function(e) {
      warning(paste("Error calculating log2FC for protein", protein, ":", e$message))
      NA
    })
    
    # Store the results
    results <- rbind(results, data.frame(
      Protein = protein,
      t_statistic = t_test_result[1],
      p_value = t_test_result[2],
      mean_difference = t_test_result[3],
      log2_fc = log2_fc
    ))
  }
  
  # q-values using Benjamini-Hochberg method
  results <- results %>%
    mutate(q_value = p.adjust(p_value, method = "BH"),
           fdr_significant = q_value < 0.05)  # Add a column to indicate significance at FDR threshold
  
  # bind character columns back
  final_results <- left_join(character_cols, results, by = "Protein")
  
  return(final_results)
}

# result <- run_welcht_tests(norm_imputed_plasma, case_control_info)
# view(result)

