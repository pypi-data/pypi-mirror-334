## Levene's median test for variance check for each feature (can be used for more than two groups)
run_levene_tests <- function(data, group_info) {
  # get character columns (e.g., Protein and Genes)
  character_cols <- data %>% select(where(is.character))
  
  # get numeric data
  numeric_data <- data %>% select(where(is.numeric))
  
  # group_info is a logical vector with the same length as the number of numeric columns
  group_info <- unname(unlist(group_info))
  group_values <- unique(group_info)
  
  if (length(group_info) != ncol(numeric_data)) {
    stop("group_info must be a factor/logical vector with the same length as numeric columns.")
  }
  
  if (length(group_values) < 2) {
    stop("At least two groups!")
  }
  
  # reshape to long format
  long_sample <- data %>%
    pivot_longer(cols = colnames(numeric_data), 
                 names_to = "Sample", 
                 values_to = "Value") %>%
    mutate(Group = rep(group_info, nrow(data)))
  
  # print(head(long_sample))  # Check structure
  
  # Initialize results dataframe
  results <- data.frame(
    Protein = character(),
    statistic = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  # do Levene's test for each feature
  for (i in 1:nrow(data)) {
    protein <- data[i, 1]  # First column is the protein identifier
    
    each_test <- long_sample %>%
      filter(Protein == protein)  # Ensure proper filtering
    
    # Check if there are at least two groups with non-NA values
    valid_groups <- unique(na.omit(each_test$Group))
    if (length(valid_groups) < 2) {
      warning(paste("Skipping", protein, "- only one group present"))
      results <- rbind(results, data.frame(Protein = protein, statistic = NA, p_value = NA))
      next
    }
    
    # Perform Levene's test
    test <- tryCatch({
      leveneTest(Value ~ Group, data = each_test, center = median)
    }, error = function(e) {
      warning(paste("Error in Levene's test:", e$message))
      return(NULL)
    })
    
    if (!is.null(test)) {
      results <- rbind(results, data.frame(
        Protein = protein,
        statistic = test$`F value`[1],
        p_value = test$`Pr(>F)`[1]
      ))
    } else {
      results <- rbind(results, data.frame(
        Protein = protein,
        statistic = NA,
        p_value = NA
      ))
    }
  }
  
  final_results <- left_join(character_cols, results, by = "Protein")
  
  return(final_results)
}

# Test the function
# levenes_results <- run_levene_tests(norm_imputed_plasma, case_control_info)


