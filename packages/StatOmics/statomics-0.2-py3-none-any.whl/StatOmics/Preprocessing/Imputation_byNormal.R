# Imputation by Normal Distribution
imputation_with_normal <- function(data, width = 0.3, down_shift = 1.8) {
  # Separate numeric and non-numeric columns
  numeric_cols <- data %>% select(where(is.numeric))
  non_numeric_cols <- data %>% select(where(~ !is.numeric(.)))
  
  # Convert numeric data to matrix
  mt_x <- as.matrix(numeric_cols)
  
  # Identify NA indices
  na_indices <- is.na(mt_x)
  
  # Calculate median and standard deviation for each row
  # median_values <- rowMedians(mt_x, na.rm = TRUE)
  mean_values <- rowMeans(mt_x, na.rm = TRUE)
  sd_values <- rowSds(mt_x, na.rm = TRUE)
  
  # Calculate parameters for imputation
  shrink_sd <- width * sd_values
  downshift_mean <- mean_values - down_shift * sd_values
  
  # Create a copy of the original matrix for imputation
  imputed_mt_x <- mt_x
  
  # Impute values
  for (i in 1:nrow(mt_x)) {
    na_in_row <- which(na_indices[i, ])
    if (length(na_in_row) > 0) {
      imputed_values <- rnorm(length(na_in_row), 
                              mean = downshift_mean[i], 
                              sd = shrink_sd[i])
      imputed_mt_x[i, na_in_row] <- imputed_values
    }
  }
  
  # Convert imputed matrix back to data frame
  imputed_numeric <- as.data.frame(imputed_mt_x)
  names(imputed_numeric) <- names(numeric_cols)
  
  # Combine imputed numeric data with non-numeric columns
  imputed_data <- bind_cols(non_numeric_cols, imputed_numeric)
  
  return(imputed_data)
}