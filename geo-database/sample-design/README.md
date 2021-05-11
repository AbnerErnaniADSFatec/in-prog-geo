docker run --rm -it --name sample-design \
    -v ${PWD}/:/home/rstudio/sample-design \
    -p 3838:3838 \
    -p 8787:8787 \
    -e ADD=shiny \
    -e DISABLE_AUTH=true \
    rocker/rstudio:devel

docker  run -d --name sample-design \
    -v ${PWD}/:/home/rstudio/sample-design \
    -p 3838:3838 \
    -p 8787:8787 \
    -e ADD=shiny \
    -e DISABLE_AUTH=true \
    rocker/rstudio:devel

docker exec -ti <CONTAINER_ID> bash