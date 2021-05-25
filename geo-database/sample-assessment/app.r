library(shiny)
library(shinythemes)
library(sparkline)
library(shinycssloaders)
library(sits)
library(dplyr)
library(ggplot2)
library(sf)

ui <- fluidPage(
  theme = shinytheme("cerulean"),
  tags$head(
    tags$link(href = "style.css", rel = "stylesheet")
  ),
  titlePanel(
    "Quality control samples - Assess Quality",
    windowTitle = "Quality control samples - Assess Quality"
  ),
  sidebarLayout(
    sidebarPanel(
      width = 3,
      fileInput("tb_file", "Choose Tibble File", accept = ".rds"),
      selectInput("select", "Select band", choices = list("NDVI"= 'NDVI'), selected = 1),
      hr(),
      fluidRow(column(10, verbatimTextOutput("render_tb"))),
      hr(),
      fluidRow(column(10, verbatimTextOutput("bands"))),
    ),
    mainPanel(
      width = 7,
      tabsetPanel(
        tabPanel(
          div("Medical History"),
          wellPanel(h3("Medical History and Tests Timeline")),
          plotOutput("ts_plot"),
          br(), br(),
          plotOutput("som_plot"),
        ),
        tabPanel(
          div("Medical History"),
          wellPanel(
            h3("Vets"),
            wellPanel(h3("Medical History and Tests Timeline")),
            plotOutput("ts_plot"),
            br(), br(),
            plotOutput("som_plot")
          )
        )
      )
    )
  )
)

server <- function(input, output) {
  output$value <- renderPrint({ input$select })
  output$bands <- renderPrint({
    file <- input$tb_file
    ext <- tools::file_ext(file$datapath)
    req(file)
    validate(need(ext == "rds", "Please upload a RDS file..."))
    input_data.tb <- readRDS(file$datapath)
    sits_bands(input_data.tb)
  })
  output$render_tb <- renderPrint({
    file <- input$tb_file
    ext <- tools::file_ext(file$datapath)
    req(file)
    validate(need(ext == "rds", "Please upload a RDS file..."))
    readRDS(file$datapath)
  })
  output$ts_plot <- renderPlot({
    file <- input$tb_file
    ext <- tools::file_ext(file$datapath)
    req(file)
    validate(need(ext == "rds", "Please upload a RDS file..."))
    input_data.tb <- readRDS(file$datapath)
    plot(sits_select(input_data.tb, bands = input$select))
  })
  output$som_plot <- renderPlot({
    file <- input$tb_file
    ext <- tools::file_ext(file$datapath)
    req(file)
    validate(need(ext == "rds", "Please upload a RDS file..."))
    input_data.tb <- readRDS(file$datapath)
    set.seed(777)
    clustering_CB4_workshop.lst <- sits::sits_som_map(
      input_data.tb,
      grid_xdim = 9,
      grid_ydim = 9,
      alpha = c(0.5, 0.01),
      distance = "euclidean",
      rlen = 100,
      som_radius = 1
    )
    plot(clustering_CB4_workshop.lst, type = "codes", whatmap = 5)
  })
}

shinyApp(ui = ui, server = server)
