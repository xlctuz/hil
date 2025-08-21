import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane3
    width: 1500
    height: 1000

    ColumnLayout {
        id: columnLayout2
        width: 100
        height: 100
        anchors.fill: parent

        GroupBox {
            id: doChannels
            width: 200
            height: 200
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true
            title: qsTr("DO回显")

            Flow {
                id: flow1
                anchors.fill: parent

                Repeater {
                    id: repeater
                    model: 5

                    Pane {
                        id: pane
                        width: 200
                        height: 200

                        GridLayout {
                            id: gridLayout
                            width: 100
                            height: 100
                            uniformCellWidths: true
                            uniformCellHeights: true
                            rows: 1
                            columns: 2

                            Label {
                                id: label
                                text: qsTr("Label")
                            }

                            MyDIOIndicator {
                                id: myDIOIndicator
                            }
                        }
                    }
                }
            }
        }

        GroupBox {
            id: diChannels
            width: 200
            height: 200
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true
            title: qsTr("DI")

            Flow {
                id: flow2
                anchors.fill: parent

                Repeater {
                    id: repeater1
                    model: 3
                }

                Pane {
                    id: pane1
                    width: 200
                    height: 200
                    GridLayout {
                        id: gridLayout2
                        width: 100
                        height: 100
                        uniformCellWidths: true
                        uniformCellHeights: true
                        rows: 1
                        columns: 2
                        Label {
                            id: label1
                            text: qsTr("Label")
                        }

                        MyDIOIndicator {
                            id: myDIOIndicator1
                        }
                    }
                }
            }
        }

        Item {
            id: item2
            width: 200
            height: 200
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }
}
