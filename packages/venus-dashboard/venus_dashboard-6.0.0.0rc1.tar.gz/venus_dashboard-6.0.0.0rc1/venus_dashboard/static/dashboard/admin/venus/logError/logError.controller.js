(function () {
  'use strict';

  angular
      .module('horizon.dashboard.admin.venus')
      .controller('LogErrorController', LogErrorController);

  LogErrorController.$inject = ['$scope', 'venusSrv'];

  function LogErrorController($scope, venusSrv) {
    $scope.STATIC_URL = STATIC_URL;
    $scope.model = {
      start_time: new Date(),
      end_time: new Date()
    };
    $scope.total = 0;
    $scope.chart1 = {
      'componentList': [],
      'chartData': []
    };
    $scope.chart2 = {
      'componentList': [],
      'chartData': []
    };
    $scope.chart3 = {
      'componentList': [],
      'chartData': []
    };
    $scope.getData = function() {
      $scope.getChart1();
      $scope.getChart2();
      $scope.getChart3();
    };
      $scope.getChart1 = function () {
      var config1 = {
        start_time: $scope.model.start_time.getTime() / 1000,
        end_time: $scope.model.end_time.getTime() / 1000,
        type: 'error_stats'
      };
      venusSrv.getError(config1).then(function (res) {
        $scope.chart1.componentList = [];
        if (res.data.data.stats.length>0) {
          res.data.data.stats.forEach(i => {
            let keyArray1 = i.key.split('/');
            i.keyValue = keyArray1[3];
            $scope.chart1.componentList.push(keyArray1[3])
          });
          //
          var obj1 = document.getElementById("selectPicker1");
          obj1.innerHTML = '';
          for (var i=0;i<$scope.chart1.componentList.length;i++) {
            obj1.add(new Option($scope.chart1.componentList[i],$scope.chart1.componentList[i]));
          }
          $scope.chart1.chartData = res.data.data && res.data.data.stats[0].count;
        }
        $scope.updateChart('svg1', $scope.chart1.chartData);
        document.getElementById('selectPicker1').addEventListener('change', function (){
          let checkOption = $("#selectPicker1").val();
          let checkChart = res.data.data && res.data.data.stats.find(item => item.keyValue == checkOption);
          $scope.updateChart('svg1', checkChart.count);
        });
      });
    };
    $scope.getChart2 = function () {
      var config2 = {
        start_time: $scope.model.start_time.getTime() / 1000,
        end_time: $scope.model.end_time.getTime() / 1000,
        type: 'rabbitmq_error_stats'
      };
      venusSrv.getError(config2).then(function (res) {
        $scope.chart2.componentList = [];
        if (res.data.data.stats.length>0) {
          res.data.data.stats.forEach(i => {
            let keyArray2 = i.key.split('/');
            $scope.chart2.componentList.push(keyArray2[3])
          });
          //
          var obj2 = document.getElementById("selectPicker2");
          obj2.innerHTML = '';
          for (var j=0;i<$scope.chart2.componentList.length;i++) {
            obj2.add(new Option($scope.chart2.componentList[j], $scope.chart2.componentList[j]));
          }
          $scope.chart2.chartData = res.data.data && res.data.data.stats[0].count;
        }
        $scope.updateChart('svg2', $scope.chart2.chartData);
        document.getElementById('selectPicker2').addEventListener('change', function (){
          let checkOption = $("#selectPicker2").val();
          let checkChart = res.data.data && res.data.data.stats.find(item => item.keyValue == checkOption);
          $scope.updateChart('svg2', checkChart.count);
        });
      });
    };
    $scope.getChart3 = function () {
      var config3 = {
        start_time: $scope.model.start_time.getTime() / 1000,
        end_time: $scope.model.end_time.getTime() / 1000,
        type: 'mysql_error_stats'
      };
      venusSrv.getError(config3).then(function (res) {
        $scope.chart3.componentList = [];
        if (res.data.data.stats.length>0) {
          res.data.data.stats.forEach(i => {
            let keyArray3 = i.key.split('/');
            $scope.chart3.componentList.push(keyArray3[3])
          });
          //
          var obj3 = document.getElementById("selectPicker3");
          obj3.innerHTML = '';
          for (var k=0;i<$scope.chart3.componentList.length;i++) {
            obj3.add(new Option($scope.chart3.componentList[k], $scope.chart3.componentList[k]));
          }
          $scope.chart3.chartData = res.data.data && res.data.data.stats[0].count;
        }
        $scope.updateChart('svg3', $scope.chart3.chartData);
        document.getElementById('selectPicker3').addEventListener('change', function (){
          let checkOption = $("#selectPicker3").val();
          let checkChart = res.data.data && res.data.data.stats.find(item => item.keyValue == checkOption);
          $scope.updateChart('svg3', checkChart.count);
        });
      });
    };
    $scope.updateChart = function (val, chartData) {
      var data = chartData;

      var padding = {
        top: 50,
        right: 50,
        bottom: 50,
        left: 100
      };

      var barGap = 2;

      var svg = d3.select('#'+val);

      var width = svg.node().getBoundingClientRect().width - padding.left - padding.right,
          height = svg.node().getBoundingClientRect().height - padding.top - padding.bottom,
          barHotZoneWidth = data.length != 0 ? width / data.length : 0,
          barHotZoneHighlight = '#ddd',
          barWidth = barHotZoneWidth - barGap,
          barBgColor = '#007ede';

      var xScale = d3.scale.linear()
          .domain([0, data.length])
          .range([0, width]);

      var yScale = d3.scale.linear()
          .domain(d3.extent(data, d => d.doc_count))
          .range([height, 0]);

      var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom');

      var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient('left');

      svg.select('#xAxis')
          .remove();

      svg.append('g')
          .attr('id', 'xAxis')
          .attr('transform', 'translate('+padding.left+', '+(height+padding.top)+')')
          .attr("class", "axis")
          .call(xAxis);

      svg.select('#yAxis')
          .remove();

      svg.append('g')
          .attr('id', 'yAxis')
          .attr('transform', 'translate('+padding.left+', '+padding.top+')')
          .attr("class", "axis")
          .call(yAxis);

      svg.select('#bar-container')
          .remove();

      var barContainer = svg.append('g')
          .attr('id', 'bar-container')
          .attr('transform', 'translate('+padding.left+', '+padding.top+')');

      var bars = barContainer.selectAll('g')
          .data(data);

      // enter
      var barG = bars.enter()
          .append('g');

      var barHotZone = barG.append('rect')
          .attr('class', 'hotzone')
          .attr('x', (d, i) => xScale(i))
          .attr('y', 0)
          .attr('width', barHotZoneWidth)
          .attr('height', height)
          .attr('fill', 'none')
          .attr('pointer-events', 'all');

      barG.append('rect')
          .attr('fill', barBgColor)
          .attr('x', (d, i) => xScale(i) + barGap / 2)
          .attr('y', (d) => yScale(d.doc_count))
          .attr('width', barWidth)
          .attr('height', (d) => height - yScale(d.doc_count));

      barG.append('text')
          .attr('x', (d, i) => xScale(i) + barHotZoneWidth / 2)
          .attr('y', (d) => yScale(d.doc_count) - 5)
          .attr('text-anchor', 'middle')
          .attr('font-size', 12)
          .text((d) => d.doc_count);

      barG.on('mouseenter', function () {
          d3.select(this).select('.hotzone').attr('fill', barHotZoneHighlight);
      }).on('mouseleave', function() {
          d3.select(this).select('.hotzone').attr('fill', 'none');
      });
    };

    function init() {
      var end_time = new Date();
      end_time.setMilliseconds(0);
      var start_time = new Date();
      start_time.setMilliseconds(0);
      start_time.setTime(end_time.getTime() - 24 * 60 * 60 * 1000);
      $scope.model.start_time = start_time;
      $scope.model.end_time = end_time;
      $scope.getData();
    };

    init();
  }

})();
