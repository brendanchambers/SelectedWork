var svg = d3.select("svg"),
width = +svg.attr("width"),
height = +svg.attr("height");
const littleRedButton = document.querySelector('.red-button');

//var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) {
        return d.screen_name; }))
    .force("charge", d3.forceManyBody().strength(() => -300))
    .force("center", d3.forceCenter(width / 2, height / 2));

fetch("data/my friend neighborhood_higher_cutoff.json")
    .then(response => response.json())
    .then(workerFunction)
    .catch(e => console.log(e));

function workerFunction(data) {
    //if (error) throw error;

    links = data.edges;
    nodes = data.vertices;    

    var link = svg.append("g")
          .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
          .attr("stroke-width", function(d) { return 3*d.weight; });

      var node = svg.append("g")
          .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
          .attr("r", d => {
             if (d.celebrity) {
                 return 20;
             } else return 10;            
          })
          .attr("fill", function(d) { 
              if (d.gulper) {
                  return "#c24";
              } else return "#0c7"; 
          })
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

      node.append("title")
          .text(function(d) { return d.id; });
    
    littleRedButton.addEventListener('click',fireRedButton);
    
     function fireRedButton() {         
         console.log('trimming celebrity nodes')
         newNodes = exitCelebrities(nodes);
         
         node = svg.selectAll("circle")
            .data(newNodes)
            .attr("r", d => {
             if (d.celebrity) {
                 return 20;
             } else return 10;            
          })
         .attr("fill", function(d) { 
              if (d.gulper) {
                  return "#c24";
              } else return "#0c7"; 
          })
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));
         
         node.exit().remove();
         
         
            


     }


      simulation
          .nodes(nodes)
          .on("tick", ticked);

      simulation.force("link")
          .links(links);

      function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
      }
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
}

function exitCelebrities(nodes) {
    // remove the celebrity nodes
    return nodes.filter(node => !node.celebrity);

}


