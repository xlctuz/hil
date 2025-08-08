import QtCharts
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

GroupBox {
    id: groupBox
    width: 1500
    height: 300
    layer.enabled: false
    title: qsTr("通道1")

    property string voltagePlaceholder: "value"
    property alias voltageField: textField1
    property alias currentField: textField2
    property alias voltageSeries: voltageChartView.series
    property alias currentSeries: currentChartView.series
    property alias powerSeries: powerChartView.series
    property alias voltageLabel: voltageLabel
    property alias currentLabel: currentLabel
    property alias powerLabel: powerLabel

    GridLayout {
        id: gridLayout
        anchors.fill: parent
        rowSpacing: 5
        uniformCellWidths: false
        uniformCellHeights: true
        flow: GridLayout.TopToBottom
        columnSpacing: 30
        rows: 2
        columns: 8

        Label {
            id: label4
            text: qsTr("设置电压")
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            Layout.rowSpan: 1
            Layout.fillHeight: false
            Layout.fillWidth: false
        }

        Label {
            id: label5
            text: qsTr("设置电流上限")
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            Layout.rowSpan: 1
            Layout.fillHeight: false
            Layout.fillWidth: false
        }

        TextField {
            id: textField1
            width: 150
            Layout.rowSpan: 1
            Layout.fillHeight: false
            Layout.fillWidth: false
            placeholderText: voltagePlaceholder
            validator: DoubleValidator {}
        }
        TextField {
            id: textField2
            width: 150
            Layout.rowSpan: 1
            Layout.fillHeight: false
            Layout.fillWidth: false
            placeholderText: qsTr("电流值(0-3A)")
            validator: DoubleValidator {}
        }

        Label {
            id: voltageLabel
            width: 80
            text: qsTr("电压: 233.33")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: voltageChartView
            lineColor: "#e51b20"
        }

        Label {
            id: currentLabel
            width: 80
            text: qsTr("电流: 222.11")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: currentChartView
            lineColor: "#42a4de"
        }

        Label {
            id: powerLabel
            width: 80
            text: qsTr("功率: 111.11")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: powerChartView
            lineColor: "#fcc016"
        }
    }
}
