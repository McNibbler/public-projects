#########################
# Convolution Simulator #
# Version 2.0 (Server)  #
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


############################
# Server Side Calculations #
############################

server <- function(input, output){
  
  # Makes the waves the same length
  wave.1.zeros <- c(wave.1,integer(length(wave.2 - 1)))
  wave.2.zeros <- c(wave.2,integer(length(wave.1 - 1)))
  
  # Determines the length of the convolution
  conv.length <- 2*npts - 1
  
  # Initializes the convolution vector with zeros
  convolution <- integer(conv.length)
  
  # axis
  t.2 <- 1:conv.length
  
  # Supposedly the actual convolution happens here
  for (i in 1:conv.length){
    for (j in 1:i){
      convolution[i] <- convolution[i] + wave.2.zeros[j]*wave.1.zeros[i - j + 1]
    }
  }
  
  
  output$slidingWave <- renderPlot({
    
    wave.1.trimmed <- rev(wave.1)
    t.trimmed <- t - (npts - input$index) * dt
    
    # Renders the sliding convoluding wave
    plot(t.trimmed*1000, wave.1.trimmed, "l", xlab = "Time (ms)", ylab = expression(paste("Y( t - ", tau,")")), col = "blue", xlim = c(0,max(t)*1000), ylim = c(-1*max(max(wave.2),max(wave.1)),max(max(wave.2),max(wave.1))), main = "Reverse Sliding Y")
    
    
  })
  
  
  output$staticWave <- renderPlot({
    
    # Renders the original convoluted wave
    plot(t*1000, wave.2, "l", xlab = "Time (ms)", ylab = "X(t)", col = "cyan", xlim = c(0,max(t)*1000), ylim = c(-1*max(max(wave.2),max(wave.1)),max(max(wave.2),max(wave.1))), main = "X (Original)")
    
  })
  
  output$slidingOriginal <- renderPlot({
    
    # Renders the original convoluting wave
    plot(t*1000, wave.1, "l", xlab = "Time (ms)", ylab = "Y(t)", col = "purple", xlim = c(0,max(t)*1000), ylim = c(-1*max(max(wave.2),max(wave.1)),max(max(wave.2),max(wave.1))), main = "Y (Original)")
    
  })
  
  output$both <- renderPlot({
    
    # Renders wave 1 sliding against wave 2
    wave.1.trimmed <- rev(wave.1)
    t.trimmed <- t - (npts - input$index) * dt
    
    plot(t*1000, wave.2, "l", xlab = "", ylab = "Signals", col = "green", xlim = c(0,max(t)*1000), ylim = c(-1*max(max(wave.2),max(wave.1)),max(max(wave.2),max(wave.1))), main = "Both Waves")
    lines(t.trimmed*1000, wave.1.trimmed, col = "magenta")
    
  })
  
  
  output$convolution <- renderPlot({
    
    # Plots the graph at the current step
    plot(t.2[0:input$index],convolution[0:input$index], xlab = "t", ylab = "C(t)", "b", col = "turquoise", main = "C = X*Y", xlim = c(0,conv.length))
    
  })
  
  output$area <- renderPlot({
    
    # Initializes a vector of zeros
    wave.1.trimmed <- integer(npts)
    
    # selects range for sliding wave based on inputs
    if (input$index > npts){
      
      wave.1.trimmed[(input$index - npts):npts] <- rev(wave.1[(input$index - npts):npts])
      
    }
    else{
      
      wave.1.trimmed[1:input$index] <- rev(wave.1[1:input$index])
      
    }
    
    # Calculates the area at each point
    area <- wave.1.trimmed * wave.2
    
    # Determines the limits for the axes
    max.area <- max(abs(wave.2))*max(abs(wave.1))
    
    # Plots the areas at every point at any given t
    plot(t*1000, area, "l", xlab = expression(tau), ylab = "Area", col = "skyblue", main = expression(paste("X( ", tau,")*Y( t - ",tau,")")), ylim = c(-1*max.area, max.area))
    
    
  })
  
  
}