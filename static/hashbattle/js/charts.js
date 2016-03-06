var randomScalingFactor = function() {
    return Math.round(Math.random() * 100);
};
var lineChartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
        label: "My First dataset",
        fillColor: "rgba(238,238,238,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "#eee",
        pointStrokeColor: "rgba(200,200,200,1)",
        pointHighlightFill: "rgba(3,169,244,1)",
        pointHighlightStroke: "rgba(3,169,244,1)",
        data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()]
    }]
};
window.onload = function() {

  $("#analyze-post").click(function(){
    $('textarea').each(function(){
      $(this).attr('readonly','readonly');
    });
    $("#chart").slideDown(function(){
      setTimeout(
        function() {
          var chartName = document.getElementById('chartName').getContext("2d");
          window.myLine = new Chart(chartName).Line(lineChartData, {
            showScale: true,
            pointDot : true,
            responsive: true,
            maintainAspectRatio: false,
            tooltipFontSize: 14.5,
            percentageInnerCutout : 50,
            tooltipCaretSize: 0,
          });;
        },
      500);
    }); 
  });
};


/*window.onload = function() {
  $(".network-container").click(function(){
    if( !$(this).hasClass("active") ) {
      
    } else {
      myLine.destroy()
    } 
  });
};

function drawChart(chartName) {
  setTimeout(
    function() {
      var chartName = document.getElementById(chartName).getContext("2d");
      window.myLine = new Chart(chartName).Line(lineChartData, {
        showScale: false,
        pointDot : false,
        responsive: true
      });;
    },
  350);

  return();
}; */