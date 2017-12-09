svg = d3.select("#mapperViz"),
width = +svg.attr("width"),
height = +svg.attr("height");


var simulation = d3.forceSimulation()
  .force('charge', d3.forceManyBody().strength(-10))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force("link", d3.forceLink().id(function(d) { return d.id; }))
  


d3.json("mapperViz.json", function(error, network){
  if (error) throw error;

// Mapper parameters display //

  d3.select(".legend").selectAll("#lens")
    .data(network.lens)
    .enter().append("h3")
      .text(" Lens = " + network.lens[0]);
  
  d3.select(".legend").selectAll("#rcover")
    .data(network.rcover)
    .enter().append("h3")
      .text(" Range cover = " + network.rcover[0]);

  d3.select(".legend").append("h3")
    .text("Clusterer = DBSCAN")    
          

//Force Link Network//

  scaleRadius = d3.scaleLinear()  
      .domain([0, network.max_weight])
      .range([25,100]);

  scaleColor = d3.scaleLinear()
      .domain([0, network.rcover[0][0]])
      .range([1,0.2]);

  simulation
      .nodes(network.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(network.links);


  function updateLinks() {
    var u = d3.select('.links')
      .selectAll('line')
      .data(network.links)

    u.enter()
      .append('line')
      .merge(u)
      .attr('x1', function(d) {return d.source.x;})
      .attr('y1', function(d) {return d.source.y;})
      .attr('x2', function(d) {return d.target.x;})
      .attr('y2', function(d) {return d.target.y;})

    u.exit().remove()
  }

  function updateNodes() {
    u = d3.select('.nodes')
      .selectAll('circle')
      .data(network.nodes)

    u.enter()
      .append('circle')
      .merge(u)
      .attr('cx', function(d) {return d.x;})
      .attr('cy', function(d) {return d.y;})
      .attr('r',  function (d) {return Math.sqrt(scaleRadius(d.weight));})
      .attr('fill', function(d){ return d3.interpolateReds(scaleColor(d.group))})
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

    u.exit().remove()
  }

  function ticked() {
    updateLinks()
    updateNodes()
  }

  function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
 cv}
 



//Data --- scatter 

  var svg2 = d3.select("#scatterPlot");

  var data = network.scatter;

  var xScale = d3.scaleLinear().range([0,500]);
  var yScale = d3.scaleLinear().range([400,0]);


  xScale.domain(d3.extent(data, function (d){ return d.x; }));
  yScale.domain(d3.extent(data, function (d){ return d.y; }));

  

  var plot = svg2.select(".scatter").selectAll(".scatterDots")
          .data(data);
        plot.enter().append("circle")
          
          .attr("cx", function (d){ return xScale(d.x); })
          .attr("cy", function (d){ return yScale(d.y); })
          .attr("r", 2)
          .attr("fill", "steelblue");
          

        plot.exit().remove();
      
     })
