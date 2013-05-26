"""Writes a strategy report to an html file"""

import plugins

import string


class HtmlStrategyEvaluator(plugins.IStrategyEvaluatorPlugin):
    """Takes in trades and outputs an html report using d3"""

    def setup(self, config):
        """Read output file name from the config file"""
        self._filename = config.get('Parameters', 'filename')

    def __call__(self, trades, x, y):
        template = """<!doctype html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Evaluation</title>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <script type="text/javascript" src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
    <style type="text/css">
body {font: 10px sans-serif;}

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path {display: none;}

.line {fill: none; stroke: steelblue; stroke-width: 1.5px;}
    </style>
  </head>
  <body>
    <ul>
      <li><a href="#payoff">Payoff</a></li>
      <li><a href="#roi">Return</a></li>
    </ul>
    <div id="payoff"></div>
    <div id="roi"></div>
    <script type="text/javascript">
var data = [
$data
];

var parseTime = d3.time.format("%I:%M:%S.%L%L").parse;

for (var i=0; i<data.length; ++i) data[i].t = parseTime(data[i].t);

var margin = {up: 20, right: 20, down: 30, left: 50},
  width = 960 - margin.left - margin.right,
  height = 500 - margin.up - margin.down;

var t = d3.time.scale()
  .domain(d3.extent(data, function(d) {return d.t;}))
  .range([0, width]);

var tAxis = d3.svg.axis().scale(t).orient("bottom");

var measures = {payoff: "Payoff ($$)", roi: "Return (%)"};

for (var m in measures) {
  var scale = d3.scale.linear()
    .domain(d3.extent(data, function(d) {return d[m];}))
    .range([height, 0]);

  var svg = d3.select("#" + m).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.up + margin.down)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.up + ")");

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(tAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(d3.svg.axis().scale(scale).orient("left"))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(measures[m]);

  svg.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", d3.svg.line().x(function(d) {return t(d.t);}).y(function(d) {return scale(d[m]);}));
}

$$("body").tabs();
    </script>
  </body>
</html>"""
        data = []
        buy = 0
        sell = 0
        selling = False
        for trade in trades:
            if trade['Record Type'] == 'TRADE':
                if trade['Buyer Broker ID'] == 'Algorithmic':
                    if selling:
                        payoff = sell - buy
                        data.append((trade['Time'], payoff, payoff/buy))
                        buy = 0
                        sell = 0
                        selling = False
                    buy += float(trade['Price']) * int(trade['Volume'])
                elif trade['Seller Broker ID'] == 'Algorithmic':
                    selling = True
                    sell += float(trade['Price']) * int(trade['Volume'])
        f = open(self._filename, 'w')
        record = '  {{t: "{0}", payoff: {1}, roi: {2}}},\n'
        records = (record.format(t, payoff, roi) for t, payoff, roi in data)
        report = string.Template(template)
        f.write(report.substitute(data=''.join(records)))
        f.close()
