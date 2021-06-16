point_to_shape_sp <- function (data.tb, name_file = "NULL") {
  group_shape <- dplyr::select(data.tb,
    longitude,
    latitude,
    start_date,
    end_date,
    label,
    id_sample,
    id_neuron,
    cluster,
    year
  )

  sp_data.tb.df <- as.data.frame(group_shape)

  points_SF <- as.data.frame(sp_data.tb.df)
  xy <- points_SF[, c(1, 2)]

  sp_data.df <- sp::SpatialPointsDataFrame(
    coords = xy,
    data = points_SF,
    proj4string = sp::CRS("+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0")
  )

  # rgdal::writeOGR(
  #   sp_data.df,
  #   dsn = '.',
  #   layer = name_file,
  #   driver = "ESRI Shapefile"
  # )
}

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

  output$render_tb <- renderDataTable({
    file <- input$tb_file
    ext <- tools::file_ext(file$datapath)
    req(file)
    validate(need(ext == "rds", "Please upload a RDS file..."))
    readRDS(file$datapath)
  })

  output$ts_plot <- renderPlotly({
    withProgress(message = 'Making plot', value = 0, {

      incProgress(1/4, detail = paste("Reading file", 1))
      file <- input$tb_file
      ext <- tools::file_ext(file$datapath)
      req(file)

      incProgress(1/4, detail = paste("Validating File", 2))
      validate(need(ext == "rds", "Please upload a RDS file..."))

      incProgress(1/4, detail = paste("Parsing RDS File", 3))
      input_data.tb <- readRDS(file$datapath)
      
      ggplotly(sits_select(input_data.tb, bands = input$select))

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