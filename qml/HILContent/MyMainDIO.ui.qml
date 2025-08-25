import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane3
    width: 1500
    height: 1000

    property var dioModel: null

    ColumnLayout {
        id: columnLayout2
        anchors.fill: parent

        GroupBox {
            id: doChannels
            Layout.fillWidth: true
            title: qsTr("DO 状态")

            Flow {
                id: flow1
                anchors.fill: parent

                Repeater {
                    id: repeater
                    model: dioModel ? dioModel.configuredDoChannels : []

                    Pane {
                        width: 200
                        height: 50

                        GridLayout {
                            anchors.fill: parent
                            rows: 1
                            columns: 2

                            Label {
                                text: modelData.name
                            }

                            MyDIOIndicator {
                                state: modelData.status
                            }
                        }
                    }
                }
            }
        }

        GroupBox {
            id: diChannels
            Layout.fillWidth: true
            title: qsTr("DI 状态")

            Flow {
                id: flow2
                anchors.fill: parent

                Repeater {
                    id: repeater1
                    model: dioModel ? dioModel.configuredDiEchos : []

                    Pane {
                        width: 200
                        height: 50
                        GridLayout {
                            anchors.fill: parent
                            rows: 1
                            columns: 2
                            Label {
                                text: modelData.name
                            }

                            MyDIOIndicator {
                                state: modelData.status
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: item2
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }
}
