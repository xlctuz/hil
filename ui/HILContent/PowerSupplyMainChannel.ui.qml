import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

GroupBox {
    id: groupBox1
    width: 1000
    height: 200
    title: qsTr("通道1")

    GridLayout {
        id: gridLayout1
        x: 229
        y: 465
        anchors.fill: parent
        uniformCellWidths: false
        uniformCellHeights: true
        rows: 2
        rowSpacing: 5
        flow: GridLayout.TopToBottom
        Label {
            id: label4
            text: qsTr("设置电压")
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            Layout.rowSpan: 1
            Layout.fillWidth: false
            Layout.fillHeight: false
        }

        Label {
            id: label5
            text: qsTr("设置电流上限")
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            Layout.rowSpan: 1
            Layout.fillWidth: false
            Layout.fillHeight: false
        }

        Label {
            id: labelVoltage
            text: qsTr("Label")
        }

        Label {
            id: labelCurrentLimit
            text: qsTr("Label")
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

        columns: 8
        columnSpacing: 30
    }
}
