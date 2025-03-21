# Mann-Whitney U-test (Two groups, two-sided)
# the smallest sample size of each of the two samples is n1=n2=3 for a one-sided test
# the smallest sample size of each of the two samples is n1=n2=4 for a two-sided test
run_mannWhitU_test <- function(data, group_info) {
  # get character columns (e.g., Protein and Genes)
  character_cols <- data %>% select(where(is.character))
  
  # get numeric data
  numeric_data <- data %>% select(where(is.numeric))
  
  # group_info is a logical vector with the same length as the number of numeric columns
  group_info <- unname(unlist(group_info))
  group_values <- unique(group_info)
  
  if (length(group_values) != 2) {
    stop("Only allow two groups!")
  }
  
  # reshape to long format
  long_sample <- data %>%
    pivot_longer(cols = colnames(numeric_data), 
                 names_to = "Sample", 
                 values_to = "Value") %>%
    mutate(Group = rep(group_info, nrow(data)))
  
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
    
    # Check if both groups have sufficient samples
    group_counts <- each_test %>% group_by(Group) %>% summarise(n = sum(!is.na(Value)))
    
    if (any(group_counts$n < 4)) {
      warning(paste("Skipping", protein, "- insufficient sample size (need at least", 4, "per group)"))
      results <- rbind(results, data.frame(Protein = protein, statistic = NA, p_value = NA))
      next
    }
    
    # Perform Mann-Whitney U-test
    test <- tryCatch({
      wilcox.test(Value ~ Group, data = each_test, alternative = "two.sided", exact = FALSE)
    }, error = function(e) {
      warning(paste("Error in Mann-Whitney U-test:", e$message))
      return(NULL)
    })
    
    if (!is.null(test)) {
      results <- rbind(results, data.frame(
        Protein = protein,
        statistic = test$statistic,
        p_value = test$p.value
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
# result <- run_mannWhitU_test(norm_imputed_plasma, case_control_info)
# sum(result$p_value < 0.05, na.rm = T)

