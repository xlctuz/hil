import QtCharts
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ChartView {
    id: line

    property alias series : series
    property color lineColor : "blue"
    property var chartData: []

    onChartDataChanged: {
        series.clear();
        axisY.max = 0; // Reset max for auto-scaling
        for (var i = 0; i < chartData.length; ++i) {
            series.append(i, chartData[i]);
        }
    }

    width: 300
    height: 200
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
    Layout.fillHeight: false
    Layout.rowSpan: 2
    titleColor: "#000000"
    plotAreaColor: "#f4f4f4"
    dropShadowEnabled: true
    Layout.fillWidth: true
    backgroundColor: "#f4f4f4"
    legend.visible: false

    ValueAxis {
        id: axisX
        min: 0
        max: 60 // Fixed max for the number of data points
    }

    ValueAxis {
        id: axisY
        min: 0
        max: 1 // Initial max, will be auto-scaled
    }
    LineSeries {
        id: series
        name: "LineSeries"
        axisX: axisX
        axisY: axisY
        color: lineColor
    }

    Connections {
        target: series
        function onPointAdded(index) {
            var point = series.at(index)
            // A simple auto-scaling for the Y-axis
            if (axisY.max < point.y) {
                axisY.max = point.y * 1.2 // Add a little buffer
            }
        }
    }
}
