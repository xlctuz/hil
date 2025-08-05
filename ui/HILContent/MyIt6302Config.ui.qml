import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts
import QtCharts
import HIL

Pane {
    id: it6302Config
    width: 1800
    height: 800
    z: 0

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        Pane {
            id: pane
            width: 200
            height: 50
            Layout.fillWidth: true

            RowLayout {
                id: rowLayout
                anchors.fill: parent

                Item {
                    id: item1
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }

                Button {
                    id: button
                    text: qsTr("重置")
                }

                Button {
                    id: button1
                    text: qsTr("测试")
                    checkable: true
                }
            }
        }
        ScrollView {
            id: scrollView
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayout2
                width: scrollView.width - 10
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.topMargin: 0
                anchors.bottomMargin: 0

                PowerSupplyChannel {
                    id: groupBox
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    title: qsTr("通道1")
                    voltagePlaceholder: qsTr("电压(0-30Volt)")
                }

                PowerSupplyChannel {
                    id: groupBox1
                    title: qsTr("通道2")
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    voltagePlaceholder: qsTr("电压(0-30Volt)")
                }

                PowerSupplyChannel {
                    id: groupBox2
                    title: qsTr("通道3")
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    voltagePlaceholder: qsTr("电压(0-5Volt)")
                }
            }
        }
    }
}
