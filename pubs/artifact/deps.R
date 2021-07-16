options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('MASS', version = '7.3-51.5')
devtools::install_version('kableExtra', version = '1.3.2')
devtools::install_version('lmerTest', version = '3.1-3')
