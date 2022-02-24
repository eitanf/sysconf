options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('rjson', version = '0.2.20')
devtools::install_version('kableExtra', version = '1.3.2')
