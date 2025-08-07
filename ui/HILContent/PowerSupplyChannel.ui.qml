import QtCharts
import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts
import QtCharts 2.9

GroupBox {
    id: groupBox
    width: 1500
    height: 300
    layer.enabled: false
    title: qsTr("通道1")

    property string voltagePlaceholder: "value"
    property alias voltageField: textField1
    property alias currentField: textField2

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
            id: label
            width: 80
            text: qsTr("电压: 233.33")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        ChartView {
            id: line
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
            LineSeries {
                name: "LineSeries"
                XYPoint {
                    x: 0
                    y: 2
                }

                XYPoint {
                    x: 1
                    y: 1.2
                }

                XYPoint {
                    x: 2
                    y: 3.3
                }

                XYPoint {
                    x: 5
                    y: 2.1
                }
            }
        }

        Label {
            id: label1
            width: 80
            text: qsTr("电流: 222.11")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        ChartView {
            id: line1
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
            LineSeries {
                name: "LineSeries"
                XYPoint {
                    x: 0
                    y: 2
                }

                XYPoint {
                    x: 1
                    y: 1.2
                }

                XYPoint {
                    x: 2
                    y: 3.3
                }

                XYPoint {
                    x: 5
                    y: 2.1
                }
            }
        }

        Label {
            id: label2
            width: 80
            text: qsTr("功率: 111.11")
            Layout.rowSpan: 2
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        ChartView {
            id: line2
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
            LineSeries {
                name: "LineSeries"
                XYPoint {
                    x: 0
                    y: 2
                }

                XYPoint {
                    x: 1
                    y: 1.2
                }

                XYPoint {
                    x: 2
                    y: 3.3
                }

                XYPoint {
                    x: 5
                    y: 2.1
                }
            }
        }
    }
}
