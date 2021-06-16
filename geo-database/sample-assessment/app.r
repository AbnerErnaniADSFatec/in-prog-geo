library(shiny)
library(shinythemes)
library(shinycssloaders)
library(shinydashboard)
library(sits)
library(ggplot2)
library(plotly)
library(sf)

source("www/interface.r")

source("www/server.r")

shinyApp(ui = ui, server = server)
