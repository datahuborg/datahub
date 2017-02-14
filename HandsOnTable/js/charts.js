var charts = function(account_name, datahub_client, conn) {
    var chart_client = {};

    var repo_name = ""; 
    var table_name = "";
    var full_name = "";
    var table_schema = null;
    var column_names = [];

    var create_selector = function(label, options) {
        var form_group = $("<div>").attr("class", "form-group");
        form_group.append("<label>"+label+"</label>");
        var selector = $("<select>");
        selector.attr("class", "form-control");
        options.forEach(function(o) {
            var input = $("<option>")
                .attr("value", o)
                .text(o);
            selector.append(input);
        });
        form_group.append(selector);
        return form_group;
    }

    chart_client.setTableInfo = function(new_repo, new_table) {
        repo_name = new_repo;
        table_name = new_table;
        full_name = account_name + "." + repo_name + "." + table_name;
    }

    var updateSchema = function() {
        table_schema = datahub_client.get_schema(conn, full_name).tuples.map(function(tuple) {return tuple.cells; });
        column_names = table_schema.map(function(cell) { return cell[0]; });
    }

    var showPieMenu = function() {
        $("#chartXCol").find("label").text("Column for categories");
        $("#chartYCol").find("label").text("Column for values");
        $("#chart_options").show();
    }

    var showScatterMenu = function() {
        $("#chartXCol").find("label").text("x values");
        $("#chartYCol").find("label").text("y values");
        $("#chart_options").show();
    }
 
    chart_client.openModal = function() {
        updateSchema();
        $("#chartModal").find(".modal-dialog").addClass("modal-lg");
        var modalTitle = $("#chartModal").find(".modal-title").text("Create a chart");
        var modalBody = $("#chartModal").find(".modal-body").html("");

        modalBody.append("<p>Note: You can only create charts on existing columns. " +
            "If you would like to chart counts or averages, please add a column or table with " +
            "the appropriate values first.</p>");
        $("#chartModal").find(".go_button").show().unbind("click");
        $("#exportSVGButton").hide();
        var selector = create_selector("Chart type", ["(Select chart type)", "Pie chart", "Bar chart", "Scatterplot"]);
        selector.change(function() { 
            var val = selector.find(":selected").first().attr("value");
            $("#chart_options").hide();
            switch(val) {
                case "Pie chart":
                case "Bar chart":
                    showPieMenu();
                    break;
                case "Scatterplot":
                    showScatterMenu();
                    break;
            }
        });
        modalBody.append(selector);

        var chart_form = $("<form id='chart_options'></form>");
        chart_form.append(create_selector("", column_names).attr("id", "chartXCol"));
        chart_form.append(create_selector("", column_names).attr("id", "chartYCol"));
        modalBody.append(chart_form);
        chart_form.hide();

        var makeChart = function(e) {
            var val = selector.find(":selected").first().attr("value");
            if (val != "Pie chart" && val != "Bar chart" && val != "Scatterplot") {
                e.preventDefault();
                return;
            }    
            var xcol = $("#chartXCol").find("select").prop("selectedIndex");
            var ycol = $("#chartYCol").find("select").prop("selectedIndex");
            var x_name = column_names[xcol];
            var y_name = column_names[ycol];
            var result = datahub_client.execute_sql(conn, 'select '+x_name+', '+y_name+' from '+full_name);
            var cdata = result.tuples.map(function (tuple) { return {"xval": tuple.cells[0], "yval": tuple.cells[1]}; });
            modalBody.html("<svg class='chart'></svg>");
            modalTitle.text(val);
            $("#chartModal").find(".go_button").hide();
            $("#exportSVGButton").show().click(function() {
                saveSvgAsPng(document.getElementsByClassName('chart')[0], "chart.png");
            });
            switch(val) {
                case "Pie chart":
                    makePieChart(cdata, column_names[xcol], column_names[ycol]);
                    break;
                case "Bar chart":
                    makeBarChart(cdata, column_names[xcol], column_names[ycol]);
                    break;
                case "Scatterplot":
                    makeScatterPlot(cdata, column_names[xcol], column_names[ycol]);
                    break;
                default:
                    console.log("chart type unknown");
            }
        }
        $("#chartModal").find(".go_button").click(makeChart);
        $("#chartModal").find(".close_button").click(function() {
            $("#chartModal").find(".modal-dialog").removeClass("modal-lg");
            modalBody.html("");
            modalTitle.text("");
            $("#exportSVGButton").hide();
            $("#chartModal").find(".go_button").show().unbind("click", makeChart);
        });
    }

    var makePieChart = function(data, xname, yname) {
        var margin = {top: 30, right: 70, bottom: 30, left: 70},
            chart_width = 500 - margin.left - margin.right,
            chart_height = 420 - margin.top - margin.bottom,
            radius = chart_width / 2;

        var chart = d3.select(".chart")
            .data([data])
            .attr("width", chart_width + margin.left + margin.right)
            .attr("height", chart_height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + (margin.left+radius) + "," + (margin.top+radius) + ")");

        var color = d3.scale.category20c();
        var arc = d3.svg.arc()
            .outerRadius(radius);
        var pie = d3.layout.pie()
            .value(function(d) { return Math.max(0, d.yval); });

        var arcs = chart.selectAll(".slice")
            .data(pie)
          .enter().append("g")
        .attr("class", "slice");

        arcs.append("path")
            .attr("fill", function(d, i) { return color(i); })
            .attr("d", arc);

        arcs.append("text")
            .attr("transform", function(d) {
                d.innerRadius = radius;
                d.outerRadius = radius;
                return "translate(" + arc.centroid(d) + ")";
            })
            .attr("text-anchor", "middle")
            .text(function(d, i) { return data[i].xval; });
    };

    var makeBarChart = function(data, xname, yname) {
        var margin = {top: 50, right: 30, bottom: 60, left: 50},
            chart_width = 800 - margin.left - margin.right,
            chart_height = 500 - margin.top - margin.bottom;
        var ymin = Math.min(0, d3.min(data, function(d) {return +d.yval; }));
        var y = d3.scale.linear()
            .domain([ymin, d3.max(data, function(d) {return +d.yval; })])
            .range([chart_height, 0]);
        var x = d3.scale.ordinal()
            .domain(data.map(function(d) { return d.xval; }))
            .rangeRoundBands([0, chart_width], .1);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var chart = d3.select(".chart")
            .attr("width", chart_width + margin.left + margin.right)
            .attr("height", chart_height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var bar = chart.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("x", function(d) { return x(d.xval); })
            .attr("y", function(d) { return Math.min(y(0), y(d.yval)); })
            .attr("height", function(d) { return Math.abs(y(0) - y(d.yval)); })
            .attr("width", x.rangeBand());
 
        chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + y(0) + ")")
            .call(xAxis)
          .append("text")
            .attr("x", chart_width / 2)
            .attr("y", 45)
            .text(xname);

        chart.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("text-anchor", "middle")
            .attr("y", -15)
            .text(yname);

   }

    var makeScatterPlot = function(data, xname, yname) {
        var margin = {top: 40, right: 50, bottom: 50, left: 50},
            chart_width = 800 - margin.left - margin.right,
            chart_height = 500 - margin.top - margin.bottom;

        var ymin = Math.min(0, d3.min(data, function(d) {return +d.yval; }));
        var xmin = Math.min(0, d3.min(data, function(d) {return +d.xval; }));
        var y = d3.scale.linear()
            .domain([ymin, d3.max(data, function(d) {return +d.yval; })])
            .range([chart_height, 0]);
        var x = d3.scale.linear()
            .domain([xmin, d3.max(data, function(d) {return +d.xval; })])
            .range([0, chart_width]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var chart = d3.select(".chart")
            .attr("width", chart_width + margin.left + margin.right)
                .attr("height", chart_height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + y(0) + ")")
            .call(xAxis)
          .append("text")
            .attr("x", chart_width)
            .attr("y", 35)
            .attr("text-anchor", "middle")
            .text(xname);

        chart.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + x(0) + ",0)")
            .call(yAxis)
          .append("text")
            .attr("text-anchor", "middle")
            .attr("y", -15)
            .text(yname);

        chart.selectAll(".circle")
            .data(data)
          .enter().append("circle")
            .attr("cx", function(d) {return x(d.xval); })
            .attr("cy", function(d) {return y(d.yval); })
            .attr("r", 6)
        }
        return chart_client;
    };
