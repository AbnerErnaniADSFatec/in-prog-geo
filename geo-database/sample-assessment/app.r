library(shiny)
library(shinythemes)
library(shinycssloaders)
library(sits)
library(ggplot2)
library(sf)

ui <- fluidPage(
  theme = shinytheme("cerulean"),
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "style.css"),
    tags$title("Quality control samples"),
    titlePanel(
      "Quality control samples",
      windowTitle = "Quality control samples - Assess Quality"
    ),
  ),
  tags$body(
    navbarPage(
      title="My Application",
      tabPanel("Component 1"),
      tabPanel("Component 2"),
      tabPanel("Component 3")
    ),
    sidebarLayout(
      sidebarPanel(
        width = 3,
        fileInput("tb_file", "Choose Tibble File", accept = ".rds"),
        selectInput("select", "Select band", choices = list("NDVI"= 'NDVI'), selected = 1),
        hr(),
        fluidRow(column(10, verbatimTextOutput("bands"))),
      ),
      mainPanel(
        class = "mainPanel",
        tabsetPanel(
          tabPanel(
            div("Assess Quality"),
            wellPanel(
              div(
                class="som_grid",
                checked=NA,
                h3("Time Series Plot"),
                plotOutput("ts_plot"),
                br(), br(),
                h3("SOM Grid"),
                plotOutput("som_plot")
              )
            )
          ),
          tabPanel(
            div("Data Table"),
            wellPanel(
              div(
                class="som_grid",
                checked=NA,
                h3("Data Tibble File"),
                hr(),
                fluidRow(column(10, verbatimTextOutput("render_tb"))),
              )
            )
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
    withProgress(message = 'Making plot', value = 0, {
      
      incProgress(1/4, detail = paste("Reading file", 1))
      file <- input$tb_file
      ext <- tools::file_ext(file$datapath)
      req(file)
      
      incProgress(1/4, detail = paste("Validating File", 2))
      validate(need(ext == "rds", "Please upload a RDS file..."))
      
      incProgress(1/4, detail = paste("Parsing RDS File", 3))
      input_data.tb <- readRDS(file$datapath)
      plot(sits_select(input_data.tb, bands = input$select))
      
      incProgress(1/4, detail = paste("Plotting File", 4))
    })
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
