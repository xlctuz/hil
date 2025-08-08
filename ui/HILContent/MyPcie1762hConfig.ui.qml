import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pcie1762hConfig
    width: 1800
    height: 800
    z: 0

    property var pcie1762h: null

    ColumnLayout {
        id: columnLayout4
        anchors.fill: parent

        Pane {
            id: pane5
            width: 200
            height: 50
            Layout.fillHeight: false
            Layout.fillWidth: true

            RowLayout {
                id: rowLayout7
                anchors.fill: parent
                Layout.maximumHeight: 100
                Layout.minimumHeight: 100
                Layout.fillWidth: true

                Item {
                    id: item1
                    width: 200
                    height: 0
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }
                Button {
                    id: button
                    text: qsTr("重置")
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
                Button {
                    id: button1
                    text: qsTr("测试")
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }
        }

        ScrollView {
            id: scrollView
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayout3
                width: scrollView.width - 10
                spacing: 20
                GroupBox {
                    id: doConfig
                    height: 400
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                    Layout.fillHeight: false
                    Layout.fillWidth: true
                    title: qsTr("DO配置")

                    Flow {
                        id: flow2
                        anchors.fill: parent
                        spacing: 5

                        Repeater {
                            id: repeater
                            Layout.fillHeight: false
                            Layout.fillWidth: false
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            model: 16

                            GroupBox {
                                id: groupBox
                                width: 200
                                height: 200
                                spacing: 2
                                title: qsTr(`${15 - index}`)

                                ColumnLayout {
                                    id: columnLayout
                                    anchors.fill: parent
                                    spacing: 0

                                    RowLayout {
                                        id: rowLayout1
                                        width: 100

                                        TextField {
                                            id: textField
                                            Layout.fillWidth: true
                                            placeholderText: qsTr("通道名称")
                                            text: pcie1762h?.doChannels[15 - index]?.name
                                                || ""
                                        }

                                        Connections {
                                            target: textField
                                            function onEditingFinished() {
                                                configViewModel.setDoChannelName(
                                                    15 - index, text)
                                            }
                                        }
                                    }
                                    RowLayout {
                                        id: rowLayout
                                        width: 100
                                        spacing: 5
                                        layoutDirection: Qt.LeftToRight
                                        uniformCellSizes: false

                                        RadioButton {
                                            id: radioButton
                                            text: qsTr("高")
                                            display: AbstractButton.TextOnly
                                            checked: pcie1762h?.doChannels[15 - index]?.status === "high"
                                        }

                                        RadioButton {
                                            id: radioButton1
                                            text: qsTr("低")
                                            display: AbstractButton.TextUnderIcon
                                            checked: pcie1762h?.doChannels[15 - index]?.status === "low"
                                        }

                                        RadioButton {
                                            id: radioButton2
                                            text: qsTr("X")
                                            display: AbstractButton.TextUnderIcon
                                            checked: pcie1762h?.doChannels[15 - index]?.status === "na"
                                        }

                                        Connections {
                                            target: radioButton
                                            function onCheckedChanged() {
                                                if (radioButton.checked) {
                                                    configViewModel.setDoChannelStatus(15 - index, "high")
                                                }
                                            }
                                        }
                                        Connections {
                                            target: radioButton1
                                            function onCheckedChanged() {
                                                if (radioButton1.checked) {
                                                    configViewModel.setDoChannelStatus(15 - index, "low")
                                                }
                                            }
                                        }
                                        Connections {
                                            target: radioButton2
                                            function onCheckedChanged() {
                                                if (radioButton2.checked) {
                                                    configViewModel.setDoChannelStatus(15 - index, "na")
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                GroupBox {
                    id: doEcho
                    height: 200
                    title: qsTr("DO回显")

                    Flow {
                        id: flow1
                        anchors.fill: parent
                        spacing: 5

                        Repeater {
                            id: repeater1
                            model: 16
                            ColumnLayout {
                                id: columnLayout1
                                width: 100
                                height: 100
                                spacing: 10
                                Label {
                                    id: label2
                                    text: `${15 - index}`
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                Rectangle {
                                    id: rectangle
                                    width: 30
                                    height: 30
                                    color: "#44ac34"
                                    radius: 15
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                    Layout.fillHeight: false
                                    Layout.fillWidth: false

                                    Label {
                                        id: label
                                        color: "#f5f5f5"
                                        text: qsTr("高")
                                        anchors.fill: parent
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                    }
                                }
                            }
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }
                    }
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                }

                GroupBox {
                    id: diEcho
                    height: 200
                    title: qsTr("DI")

                    Flow {
                        id: flow3
                        anchors.fill: parent
                        spacing: 5

                        Repeater {
                            id: repeater2
                            model: 16
                            ColumnLayout {
                                id: columnLayout2
                                width: 100
                                height: 100
                                spacing: 10
                                Label {
                                    id: label3
                                    text: `${15 - index}`
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    Layout.minimumWidth: 50
                                    Layout.maximumWidth: 50
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                Rectangle {
                                    id: rectangle1
                                    width: 30
                                    height: 30
                                    color: "#44ac34"
                                    radius: 15
                                    Label {
                                        id: label1
                                        color: "#f5f5f5"
                                        text: qsTr("高")
                                        anchors.fill: parent
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                    }
                                    Layout.fillWidth: false
                                    Layout.fillHeight: false
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }
                            }
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }
                    }
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                }
            }
        }
    }
}
