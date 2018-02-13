####################################
# ATE csv/STDF Reader and Analyzer #
# Version 0.1                      #
#                                  #
# February 12, 2018                #
# Thomas Kaunzinger                #
# XCerra Corp.                     #
####################################

# Libraries
library(shiny)

# Imports the RADAR library because they don't actually have a proper R package
# DOWNLOAD RADAR HERE: https://sites.google.com/site/stdfradar/
my.dir <- getwd()

setwd("./RADAR Files/RADAR_package_0v6p8")
source("Radar.r")

# to change default values, uncomment and adjust the values accordingly:
#tclvalue(.Radar$.TkRadar.env$default_min_plots_per_page) <- 8
#tclvalue(.Radar$.TkRadar.env$default_use_csv_formulas) <- 1
#tclvalue(.Radar$.TkRadar.env$default_use_OOCalc_csv) <- 1
#tclvalue(.Radar$.TkRadar.env$default_add_normal_curve) <- 1

setwd(my.dir)
rm(my.dir)

TkRadar()


# Testing with this file
data.file <- file("./Data/super secret test data.std")