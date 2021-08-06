options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('GGally', version = '2.0.0')
devtools::install_version('kableExtra', version = '1.3.2')
devtools::install_version('lmerTest', version = '3.1-3')
devtools::install_version('corrplot', version = '0.90')
devtools::install_version('RColorBrewer', version = '1.1-2')
