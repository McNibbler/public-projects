# Convolution Simulator #
# Version 2.0 (Client)  #
#                       #
# February 2, 2018      #
# Thomas Kaunzinger     #
# XCerra Corp.          #
#########################

# Libraries
library(shiny)

# Wave Generation
sample.rate <- 2048
npts <- 512

# Time Axis
dt = 1/npts
t <- 0:(npts - 1) * dt

# Creating the sine waves
freq <- 20 # 5 peaks over 250ms
omega <- 2 * pi * freq

wave.1 <- c(integer(25),integer(3) + 10, integer(9), integer(3) + 10, integer(297), integer(3) + 5, integer(npts - 340))
#wave.1 <- c(integer(25),integer(3) + 10, integer(44), integer(3) + 10, integer(72), integer (3) + 10, integer(npts - 150))
wave.2 <- c(integer(25),integer(3) + 10, integer(9), integer(3) + 10, integer(75), sin(omega*t[115:(npts - 1)]))


################
# Generates UI #
################

ui <- fluidPage(
  
  # Title
  titlePanel("Convolution Simulator: C = X*Y"),
  
  # Slider to move sine wave along
  sidebarLayout(
    
    sidebarPanel(
      
      sliderInput("index", h3("Step Number:"),
                  min = 1, max = 2*npts - 1, value = 1, animate = animationOptions(interval = 250)),
      
      # Plots the reverse sliding graph for visualization
      plotOutput("slidingWave"),
      
      # Plots the original wave that's getting convoluted
      plotOutput("staticWave"),
      
      # Plots the original wave that's convoluting
      plotOutput("slidingOriginal")
      
    ),
    
    # Graphical output for the final convolution and visualizing plots
    mainPanel(
      
      plotOutput("convolution"),
      plotOutput("both"),
      plotOutput("area")
      
      
    )
  )
  
)