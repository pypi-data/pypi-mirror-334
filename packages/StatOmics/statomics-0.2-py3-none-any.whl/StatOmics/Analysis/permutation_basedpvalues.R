## Use existing package for SAM
install.packages("samr")
library(samr)
library(DT)
# The data must be logged2 transformed, delta assume to be 0.5
permuta_basedpval <- function(data, gene_col, nperm, filepath, reference_group = NULL) {
  
  # Check whether gene column exists
  if(!(gene_col %in% colnames(data))) {
    stop("Gene column '", gene_col, "' not found in data. Available columns: ", 
         paste(colnames(data), collapse=", "))
  }
  
  gene_names <- data[[gene_col]]
  
  # Group_info is indicated by column names (anything before the first '_' of numeric cols)
  numeric_data <- data %>% select(where(is.numeric))
  
  groups <- sub("_.*", "", colnames(numeric_data))
  unique_groups <- unique(groups)
  
  # Validate that we have exactly 2 groups for two-class analysis
  if(length(unique_groups) != 2) {
    stop("This function requires exactly 2 groups for analysis. Found: ", 
         paste(unique_groups, collapse = ", "))
  }
  
  # If reference_group is not provided, use the first group as reference
  if(is.null(reference_group)) {
    reference_group <- unique_groups[1]
    message("Using '", reference_group, "' as the reference group (coded as 1)")
  } else if(!(reference_group %in% unique_groups)) {
    stop("Reference group '", reference_group, "' not found in data. Available groups: ", 
         paste(unique_groups, collapse = ", "))
  }
  
  # Create response vector (y), 1 for reference group, 2 for the other group
  y <- ifelse(groups == reference_group, 1, 2)
  
  
  samr_data <- list(
    x = as.matrix(numeric_data),  # expression matrix
    y = y,                                  # response vector (1=Control, 2=Case)
    geneid = gene_names,                     # gene id
    genenames = gene_names,                  # gene names
    logged2 = TRUE                         
  )
  
  # Run SAM analysis
  sam_result <- samr(samr_data, 
                     resp.type = "Two class unpaired", 
                     nperms = nperm)
  
  # get pvalues, dscores
  samr.pvalues <- samr.pvalues.from.perms(sam_result$tt, sam_result$ttstar)
  samr_dscores <- sam_result$tt
  
  # Calculate fold changes
  samr.fold_changes <- rowMeans(numeric_data[, groups != reference_group]) - 
    rowMeans(numeric_data[, groups == reference_group])
  
  # Calculate mean differences
  # Data before log2, reverse the log2 transformation 
  raw_data <- 2 ^ numeric_data
  mean_diff <- rowMeans(raw_data[, groups != reference_group]) - 
    rowMeans(raw_data[, groups == reference_group])
  
  # Extract significant gene IDs
  siggenes.table <- samr.compute.siggenes.table(sam_result, del = 0.5, samr_data, delta.table)
  sig_genes_up <- siggenes.table$genes.up[, 2] # Second column contains gene names
  sig_genes_down <- siggenes.table$genes.lo[, 2]
  all_sig_genes <- c(sig_genes_up, sig_genes_down)
  
  if (length(all_sig_genes) == 0) {
    warning("No significant genes found.")
  } else {
    message("Number of significant genes: ", length(all_sig_genes))
  }
  
  # Create significance marker ("+" for significant, "" for non-significant)
  is_significant <- ifelse(gene_names %in% all_sig_genes, "+", "")
  
  samr_table <- data.frame(
    Gene_Name = samr_data$genenames,
    D_Score = samr_dscores,
    P_Value = samr.pvalues,
    log2Fold_Change = samr.fold_changes,
    Mean_Difference = mean_diff,
    SAMR_Significant = is_significant,
    stringsAsFactors = FALSE
  )
  
  writexl::write_xlsx(samr_table, path = filepath)
  
  
  return(samr_table)
  
  
}

# test the function
# results <- permuta_basedpval(norm_imputed_plasma, "Genes", 250,
#                         filepath = "~/Downloads/Alzheimer_samr_results.xlsx", reference_group = "Control")

