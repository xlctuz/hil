import QtQuick 6.2
import QtQuick.Controls 6.2
import QtQuick.Layouts 6.3

Page {
    id: root
    title: qsTr("RM550 Configuration")
    property var rm550ConfigViewModel: null

    GridLayout {
        anchors.fill: parent
        anchors.margins: 10
        columns: 2

        RowLayout {
            Layout.columnSpan: 2
            Layout.alignment: Qt.AlignRight
            spacing: 10

            Button {
                text: qsTr("Apply")
                enabled: rm550ConfigViewModel || false
                Connections {
                    function onClicked() {
                        rm550ConfigViewModel.apply_resistance(
                                    parseFloat(resistanceField.text))
                    }
                }
            }

            Button {
                text: qsTr("Save")
                highlighted: true
                enabled: rm550ConfigViewModel || false
                Connections {
                    function onClicked() {
                        rm550ConfigViewModel.port = portField.text
                        rm550ConfigViewModel.baudrate = parseInt(baudrateField.text)
                        rm550ConfigViewModel.initialResistance = parseFloat(resistanceField.text)
                        rm550ConfigViewModel.save_data()
                    }
                }
            }
        }

        Label {
            text: qsTr("Serial Port:")
            Layout.alignment: Qt.AlignRight
        }
        TextField {
            id: portField
            text: rm550ConfigViewModel ? rm550ConfigViewModel.port : ""
            placeholderText: qsTr("e.g., COM3")
            Layout.fillWidth: true
            Connections {
                function onEditingFinished() {
                    if (rm550ConfigViewModel)
                        rm550ConfigViewModel.port = portField.text
                }
            }
        }

        Label {
            text: qsTr("Baudrate:")
            Layout.alignment: Qt.AlignRight
        }
        TextField {
            id: baudrateField
            text: rm550ConfigViewModel?.baudrate?.toString() || ""
            placeholderText: qsTr("e.g., 115200")
            validator: IntValidator {
                bottom: 9600
                top: 921600
            }
            Layout.fillWidth: true
            Connections {
                function onEditingFinished() {
                    if (rm550ConfigViewModel)
                        rm550ConfigViewModel.baudrate = parseInt(baudrateField.text)
                }
            }
        }

        Label {
            text: qsTr("Resistance (Ω):")
            Layout.alignment: Qt.AlignRight
        }
        TextField {
            id: resistanceField
            text: rm550ConfigViewModel?.initialResistance?.toFixed(3) || ""
            placeholderText: qsTr("e.g., 100.0")
            validator: DoubleValidator {
                bottom: 0
                top: 1000000
                decimals: 3
                notation: DoubleValidator.StandardNotation
            }
            Layout.fillWidth: true
        }

        // Spacer
        Item {
            Layout.columnSpan: 2
            Layout.fillHeight: true
        }

    }
}
