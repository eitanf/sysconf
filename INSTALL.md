This document lists the preparation and installation of all the prerequisits for building sysconf documents. Alternatively, if you just want to run a prepackaged container with all the latest source, data, and papers, run:
`docker run -ti eitanf/sysconf:latest`.

If you do want to go through the full install on a local machine, follow these steps:

# Ubuntu 20.04.3-LTS

Assuming a fresh Ubuntu install (minimum recommended available disk size: 12GB), follow these steps:

## 1. Install build tools and prerequisite libraries

```
sudo apt-get update
sudo apt-get upgrade
sudo apt install g++ git python3-pip
sudo apt install libcurl4-openssl-dev libfontconfig1-dev libgdal-dev \
    libgeos-dev libpoppler-cpp-dev libssl-dev \
    libudunits2-dev libxml2-dev \
    libharfbuzz-dev libfribidi-dev
```

## 2. Install R & pandoc

Make sure the installed version of R is at least 4.3.

```
sudo apt install pandoc pandoc-citeproc r-base-core \
    texlive-latex-recommended texlive-latex-extra
```


## 3. Clone `sysconf` repository

```
git clone https://github.com/eitanf/sysconf
cd sysconf
```

## 4. Set environment variables

```
export SYSCONF_HOME=$(pwd)
export R=Rscript
```

## 5. Install R dependencies

From the shell, run:

```
Rscript deps.R
```

Answer `yes` to the questions on local installation.

## 6. Test it out

Run `cd pubs; make`. You should get no error messages except from `diversity-survey`.

## Troubleshooting

You [may](https://github.com/r-dbi/RPostgres/issues/110) need to set the `TAR` variable if `/bin/gtar` is not present:

```
export TAR="/bin/tar"
```


# MacOS 10.15 (Catalina)


## 1. Install build tools and prerequisite libraries

```
brew install imagemagick freetype gdal git libgit2 poppler proj udunits2
```

## 2. Install R & pandoc

```
brew install R pandoc mactex
```

And close/restart the terminal. Then, repeat steps 3--6 above.


