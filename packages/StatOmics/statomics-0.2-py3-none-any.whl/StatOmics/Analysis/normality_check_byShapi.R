# Shapiro Test of Normality for each feature
normality_check_byShapi <- function(data) {
  
  # Make a copy of the data to avoid modifying the original
  df <- data
  
  # Function to run Shapiro test
  run_shapiro <- function(x) {
    # Remove NA values before testing
    x <- na.omit(x)
    
    if (length(unique(x)) > 1 && length(x) >= 3) {
      # Shapiro test requires at least 3 observations
      return(shapiro.test(x)$p.value)
    } else {
      return(NA)  # Return NA for insufficient data
    }
  }
  
  # Apply Shapiro test row-wise
  shapiro_results <- df %>%
    rowwise() %>%
    mutate(
      shapiro_p_value = run_shapiro(c_across(where(is.numeric)))
    ) %>%
    ungroup()
  
  # Create visualization
  p <- ggplot(shapiro_results, aes(x = seq_along(shapiro_p_value), y = shapiro_p_value, 
                                   color = shapiro_p_value > 0.05)) +
    geom_point(shape = 1, size = 0.5) +
    geom_hline(yintercept = 0.05, linetype = "dashed", color = "red") +
    scale_color_manual(values = c("red", "blue"), 
                       labels = c("p <= 0.05", "p > 0.05"),
                       name = "Shapiro-Wilk test") +
    labs(x = "Protein Index", 
         y = "Shapiro-Wilk test p-value", 
         title = "Scatter Plot of Shapiro-Wilk Test P-values for Proteins",
         subtitle = "Red line indicates p-value = 0.05") +
    theme_minimal() +
    theme(legend.position = "bottom")
  

  
  # Return a list with results and plot
  return(list(
    data = shapiro_results,
    plot = p,
    sumNonnorm = sum(shapiro_results$shapiro_p_value <= 0.05, na.rm = TRUE)
  ))
}

# Example usage:
# result <- normality_check_byShapi(norm_imputed_plasma)

# # View summary statistics
# print(result$sumNonnorm)

# # Display the plot
# print(result$plot)

# # Access the data with p-values
# head(result$data)


