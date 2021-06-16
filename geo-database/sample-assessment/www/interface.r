ui <- dashboardPage(
  dashboardHeader(
    title = "Quality Control"
  ),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Quality Control Samples", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("Widgets", tabName = "widgets", icon = icon("th"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(
        tabName = "dashboard",
        fluidRow(
          box(
            title = "Input Parameters",
            width = 3,
            solidHeader = TRUE,
            status = "primary",
            fileInput("tb_file", "Choose Tibble File", accept = ".rds"),
            selectInput("select", "Select band", choices = list("NDVI"= 'NDVI'), selected = 1),
            hr(),
            fluidRow(column(10, verbatimTextOutput("bands")))
          ),
          tabBox(
            width = 9,
            tabPanel(
              div("Assess Quality"),
              wellPanel(
                class="som_grid",
                checked=NA,
                h3("SOM Grid"),
                plotOutput("som_plot")
              )
            ),
            tabPanel(
              div("Data Table"),
              wellPanel(
                class="som_grid",
                checked=NA,
                h3("Data Tibble File"),
                hr(),
                dataTableOutput("render_tb"),
              )
            )
          ),
          box(
            h3("Time Series Plot"),
            plotlyOutput("ts_plot")
          )
        )
      ),
      tabItem(
        tabName = "widgets",
        h2("Widgets tab content")
      )
    )
  )
)

