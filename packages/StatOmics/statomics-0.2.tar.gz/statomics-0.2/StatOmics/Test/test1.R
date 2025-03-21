# test1.R

# Function to count the number of characters in an input string
count_chars <- function(input_string) {
  input_string <- as.character(input_string)
  return(nchar(input_string))
}


# Function that returns "hi"
say_hi <- function() {
  return("hi")
}