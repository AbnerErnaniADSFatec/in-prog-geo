library(shiny)
library(ggplot2)
library(dplyr)

modis <- read.csv("./data/MOD13Q1-1.2019.11.01.csv", stringsAsFactors = FALSE, sep = ";")

ui <- fluidPage(
  titlePanel("MOD13Q1-1 2019 11 01 data"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("search_input", "Search", -10000, 10000, c(-10000,10000), pre = "Value "),
      radioButtons(
        "typeInput",
        "Select bands",
        choices = c("ndvi", "evi", "nir", "red"),
        selected = "ndvi"
      )
    ),
    mainPanel(
      plotOutput("coolplot"),
      br(), br(),
      tableOutput("results")
    )
  )
)

server <- function(input, output) {
  output$coolplot <- renderPlot({
      ggplot(modis, aes(x=timeline, y=ndvi, group=1)) + geom_line() + geom_point()
    })
}

shinyApp(ui = ui, server = server)
