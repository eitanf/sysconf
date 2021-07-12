options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('stringr', version = '1.4.0')
devtools::install_version('kableExtra', version = '1.3.2')
