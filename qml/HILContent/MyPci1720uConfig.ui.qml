import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pci1720uConfig
    width: 1800
    height: 800

    property var pci1720u: null

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            // Buttons for Reset and Test
            Layout.fillWidth: true
            Item {
                Layout.fillWidth: true
            } // Spacer
            Button {
                id: btnReset
                text: qsTr("重置")
            }
            Button {
                id: btnTest
                text: qsTr("测试")
            }
            Connections {
                target: btnReset
                function onClicked() {}
            }
            Connections {
                target: btnTest
                function onClicked() {
                    if (pci1720u) {
                        pci1720u.test()
                    }
                }
            }
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Flow {
                width: parent.width
                spacing: 10
                padding: 10

                Repeater {
                    model: pci1720u ? pci1720u.channels : []

                    GroupBox {
                        title: `AO Channel ${model.index}`
                        width: 300

                        ColumnLayout {
                            spacing: 5

                            TextField {
                                id: nameField
                                text: modelData?.name || ""
                                placeholderText: qsTr("Channel Name")
                            }

                            TextField {
                                id: voltageField
                                text: modelData?.voltage?.toFixed(2) || "0.0"
                                placeholderText: qsTr("Voltage")
                                validator: DoubleValidator {}
                            }

                            Connections {
                                target: nameField
                                function onEditingFinished() {
                                    pci1720u.setChannelName(index, nameField.text)
                                }
                            }
                            Connections {
                                target: voltageField
                                function onEditingFinished() {
                                    pci1720u.setChannelVoltage(index, parseFloat(voltageField.text))
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
