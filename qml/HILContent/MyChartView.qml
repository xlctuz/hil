import QtCharts
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ChartView {
    id: line

    property alias series : series
    property color lineColor : "blue"

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
        max: 0
    }

    ValueAxis {
        id: axisY
        min: 0
        max: 0
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
            if (axisY.max < point.y) {
                axisY.max = point.y << 2
            }

            if (series.count > 50) {
                series.removePoints(0, series.count - 50)
                series.axisX.min = series.at(0).x
            }
            series.axisX.max = series.at(series.count-1).x
        }
    }
}
