predictsp_poly <- function(vector_for_model, model, id, filename = NULL){
  library(mlr)
  library(sf)
  
  vector_for_model <- st_read(vector_for_model)
  data <- as.data.frame(vector_for_model)
  geom <- names(data) %in% "geom"
  data <- data[,!geom]
  
  out <- names(data) %in% id
  data <- data[,!out]
  prediction <- predict(model, newdata = data)
  jcintasr <- cbind(vector_for_model, prediction)
  return(jcintasr["response"])
  if(!is.null(filename)){
    st_write(jcintasr, filename)
  }
  
}
