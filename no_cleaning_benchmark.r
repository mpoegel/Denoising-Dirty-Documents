# =============================================================================
# Establish a benchmark by not editing any of the images
#
# 06/03/2015
# Matt Poegel
# =============================================================================

require(png)

imageToDF <- function(image.file, id) {
  img <- readPNG(image.file)
  nrows <- dim(img)[1]
  ncols <- dim(img)[2]
  entries <- nrows * ncols
  pixel.values <- img
  dim(pixel.values) <- c(entries, 1)
  rows = ((1:entries-1)) %% (nrows) + 1
  cols = ((1:entries-1)) %/%  (nrows) + 1
  img.df = data.frame(id=rep(id, entries),
                      row=rows,
                      col=cols,
                      value=pixel.values)
}

test.files <- list.files(path='test', pattern='.png')
test.img.df <- data.frame()
header <- TRUE
out.file.name <- 'no_cleaning_benchmark.csv'

for (file in test.files) {
  img.df <- imageToDF(paste('test/', file, sep=''), gsub('.png', '', file))
  # test.img.df <- merge(test.img.df, img.df, all=TRUE)
  if (header) {
    write('id,value', file=out.file.name, sep=',')
    header <- FALSE
  }
  write.table(c(paste(img.df$id, '_', img.df$row, '_', img.df$col, sep=''), img.df$value), 
              out.file.name, col.names=FALSE, sep=',', quote=FALSE, append=TRUE)
  break;
}

