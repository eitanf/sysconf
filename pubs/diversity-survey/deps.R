options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('bookdown', version = '0.21')
devtools::install_version('rticles', version = '0.18')
devtools::install_version('tidyverse', version = '1.3.0')
devtools::install_version('lubridate', version = '1.7.9.2')

devtools::install_version('stringr', version = '1.4.0')
devtools::install_version('kableExtra', version = '1.3.2')
