// set up constants used throughout script
const margin = {top: 80, right: 100, bottom: 40, left: 60}
const plotWidth = 800 - margin.left - margin.right
const plotHeight = 400 - margin.top - margin.bottom

const lineWidth = 3
const mediumText = 18
const bigText = 28

// set width and height of svg element (plot + margin)
svg.attr("width", plotWidth + margin.left + margin.right)
   .attr("height", plotHeight + margin.top + margin.bottom)
   
// create plot group and move it
let plotGroup = svg.append("g")
                   .attr("transform",
                         "translate(" + margin.left + "," + margin.top + ")")

// x-axis values to year range in data
// x-axis goes from 0 to width of plot
let xAxis = d3.scaleLinear()
    .domain(d3.extent(data, d => { return d.year; }))
    .range([ 0, plotWidth ]);
    
// y-axis values to cumulative caught range
// y-axis goes from height of plot to 0
let yAxis = d3.scaleLinear()
    .domain(d3.extent(data, d => { return d.cumulative_caught; }))
    .range([ plotHeight, 0]);
    
// add x-axis to plot
// move x axis to bottom of plot (height)
// format tick values as date (no comma in e.g. 2,001)
// set stroke width and font size
plotGroup.append("g")
   .attr("transform", "translate(0," + plotHeight + ")")
   .call(d3.axisBottom(xAxis).tickFormat(d3.format("d")))
   .attr("stroke-width", lineWidth)
   .attr("font-size", mediumText);

// add y-axis to plot
// set stroke width and font size
plotGroup.append("g")
    .call(d3.axisLeft(yAxis))
    .attr("stroke-width", lineWidth)
    .attr("font-size", mediumText);
    
// turns data into nested structure for multiple line chart
// d3.nest() no longer available in D3 v6 and above hence version set to 5
let nestedData = d3.nest()
    .key(d => { return d.character;})
    .entries(data);

let path = plotGroup.selectAll(".drawn_lines")
    .data(nestedData)
    .enter()
    .append("path")
    // set up class so only this path element can be removed
    .attr("class", "drawn_lines")
    .attr("fill", "none")
    // color of lines from hex codes in data
    .attr("stroke", d => {return d.values[0].color}) 
    .attr("stroke-width", lineWidth)
     // draw line according to data
    .attr("d", d => {
      return d3.line()
        .x(d => { return xAxis(d.year);})
        .y(d => { return yAxis(d.cumulative_caught);})
        (d.values)
    })
    
// create plot title
svg.append("text")
   .attr("text-anchor", "start")
   .attr("x", margin.left)
   .attr("y", margin.top/3)
   .text("Monsters caught by Mystery Inc. members")
   .attr("fill", "black")
   .attr("font-size", bigText)
   .attr("font-weight", "bold")