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

                Connections {
                    target: button
                    function onClicked () {
                        if (pcie1762h) {
                            pcie1762h.reset()
                        }
                    }
                }

                Connections {
                    target: button1
                    function onClicked () {
                        if (pcie1762h) {
                            pcie1762h.test()
                        }
                    }
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
                                spacing: 2
                                title: qsTr(`${15 - index}`)

                                ColumnLayout {
                                    id: columnLayout
                                    anchors.fill: parent
                                    spacing: 0

                                    RowLayout {
                                        id: rowLayout1
                                        width: 80

                                        TextField {
                                            id: textField
                                            Layout.fillWidth: true
                                            placeholderText: qsTr("通道名称")
                                            text: pcie1762h?.doChannels[15 - index]?.name
                                                || ""
                                        }

                                        RadioButton {
                                            id: radioButton
                                            text: qsTr("高")
                                            display: AbstractButton.IconOnly
                                            checked: pcie1762h?.doChannels[15 - index]?.status
                                                === "high"
                                        }

                                        RadioButton {
                                            id: radioButton1
                                            text: qsTr("低")
                                            display: AbstractButton.TextBesideIcon
                                            checked: pcie1762h?.doChannels[15 - index]?.status
                                                === "low"
                                        }

                                        RadioButton {
                                            id: radioButton2
                                            text: qsTr("X")
                                            display: AbstractButton.TextBesideIcon
                                            checked: pcie1762h?.doChannels[15 - index]?.status
                                                === "na"
                                        }

                                        Connections {
                                            target: textField
                                            function onEditingFinished() {
                                                if (pcie1762h) {
                                                    pcie1762h.setDoChannelName(15 - index, textField.text)
                                                }
                                            }
                                        }
                                    }
                                    RowLayout {
                                        id: rowLayout
                                        width: 80
                                        spacing: 5
                                        layoutDirection: Qt.LeftToRight
                                        uniformCellSizes: false

                                        Connections {
                                            target: radioButton
                                            function onCheckedChanged() {
                                                if (radioButton.checked) {
                                                    if (pcie1762h) {
                                                        console.log(pcie1762h)
                                                        pcie1762h.setDoChannelStatus(15 - index, "high")
                                                    }
                                                }
                                            }
                                        }
                                        Connections {
                                            target: radioButton1
                                            function onCheckedChanged() {
                                                if (radioButton1.checked) {
                                                    if (pcie1762h) {
                                                        pcie1762h.setDoChannelStatus(15 - index, "low")
                                                    }
                                                }
                                            }
                                        }
                                        Connections {
                                            target: radioButton2
                                            function onCheckedChanged() {
                                                if (radioButton2.checked) {
                                                    if (pcie1762h) {
                                                        pcie1762h.setDoChannelStatus(15 - index, "na")
                                                    }
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
                        spacing: 20

                        Repeater {
                            id: repeater1
                            model: 16
                            ColumnLayout {
                                id: columnLayout1
                                spacing: 10
                                Label {
                                    id: label2
                                    text: `${15 - index}`
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                MyDIOIndicator {
                                    id: rectangle2
                                    Layout.fillWidth: false
                                    Layout.fillHeight: false
                                    state: pcie1762h?.doEchos?.[15-index].status || "na"
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
                        spacing: 20

                        Repeater {
                            id: repeater2
                            model: 16
                            ColumnLayout {
                                id: columnLayout2
                                spacing: 10
                                Label {
                                    id: label3
                                    text: `${15 - index}`
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                MyDIOIndicator {
                                    id: rectangle1
                                    Layout.fillHeight: false
                                    Layout.fillWidth: false
                                    state: pcie1762h?.diEchos?.[15-index].status || "na"
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

/*##^##
  Designer {
  D{i:0}D{i:20;invisible:true}D{i:29}
  }
  ##^##*/
