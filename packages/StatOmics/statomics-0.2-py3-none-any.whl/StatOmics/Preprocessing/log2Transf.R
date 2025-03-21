## Log2 Transformation
transformation_log2 <- function(data){
  transformed_data <- mutate_if(data, is.numeric, log2)
  
  return(transformed_data)
}