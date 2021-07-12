options(Ncpus = parallel::detectCores())
install.packages('devtools')
library('devtools')

devtools::install_version('kableExtra', version = '1.3.2')
devtools::install_version('rnaturalearth', version = '0.1.0')
devtools::install_version('rnaturalearthdata', version = '0.1.0')
devtools::install_version('rgeos', version = '0.5-5')
