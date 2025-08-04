import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pcie1762hConfig
    width: 1200
    height: 600
    z: 0

    ColumnLayout {
        id: columnLayout3
        anchors.fill: parent

        Pane {
            id: pane5
            width: 200
            height: 200
            Layout.fillWidth: true

            RowLayout {
                id: rowLayout7
                anchors.fill: parent
                Layout.maximumHeight: 100
                Layout.minimumHeight: 100
                Layout.fillWidth: true

                Button {
                    id: button1
                    text: qsTr("测试")
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }
        }
        GroupBox {
            id: groupBox3
            height: 200
            Layout.minimumHeight: 300
            Layout.maximumHeight: 300
            Layout.fillHeight: true
            Layout.fillWidth: true
            title: qsTr("DO配置")

            GridLayout {
                id: gridLayout3
                anchors.fill: parent
                uniformCellWidths: true
                uniformCellHeights: true
                rows: 2
                columns: 16

                Repeater {
                    id: repeater
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    model: 16

                    Label {
                        id: label1
                        x: 0
                        y: 298
                        text: `${16 - index}`
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                Repeater {
                    id: repeater1
                    model: 16

                    ComboBox {
                        id: comboBox
                        width: 50
                    }
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }
            }
        }
    }
}
