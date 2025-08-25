import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

GroupBox {
    id: groupBox1
    width: 1000
    height: 200

    property string titleText: "通道"
    property var channel: null // This will hold the channel view model

    title: titleText

    GridLayout {
        id: gridLayout1
        anchors.fill: parent
        rows: 2
        columns: 8
        rowSpacing: 5
        columnSpacing: 30
        flow: GridLayout.TopToBottom
        uniformCellHeights: true
        uniformCellWidths: false

        Label {
            text: qsTr("设置电压")
        }

        Label {
            text: qsTr("设置电流上限")
        }

        Label {
            id: labelVoltage
            text: channel ? channel.voltage.toFixed(2) + " V" : "N/A"
        }

        Label {
            id: labelCurrentLimit
            text: channel ? channel.current.toFixed(2) + " A" : "N/A"
        }

        Label {
            id: voltageLabel
            width: 80
            text: qsTr("电压: ") + (channel ? channel.measuredVoltage.toFixed(2) : "0.00")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: voltageChartView
            lineColor: "#e51b20"
            chartData: channel ? channel.voltageData : []
        }

        Label {
            id: currentLabel
            width: 80
            text: qsTr("电流: ") + (channel ? channel.measuredCurrent.toFixed(2) : "0.00")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: currentChartView
            lineColor: "#42a4de"
            chartData: channel ? channel.currentData : []
        }

        Label {
            id: powerLabel
            width: 80
            text: qsTr("功率: ") + (channel ? channel.power.toFixed(2) : "0.00")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyChartView {
            id: powerChartView
            lineColor: "#fcc016"
            chartData: channel ? channel.powerData : []
        }
    }
}
