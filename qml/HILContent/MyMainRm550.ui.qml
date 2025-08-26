import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: root
    property var rm550ViewModel: null


    RowLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 15

        Label {
            text: qsTr("RM550 Resistor")
            font.bold: true
            Layout.alignment: Qt.AlignVCenter
        }

        Label {
            text: rm550ViewModel ? rm550ViewModel.currentResistance + " Ω" : "N/A"
            font.pixelSize: 20
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        }

        Switch {
            id: enableSwitch
            text: qsTr("Output")
            checked: rm550ViewModel ? rm550ViewModel.isEnabled : false
            enabled: rm550ViewModel
            onClicked: {
                rm550ViewModel.toggle_output(checked)
            }
            Layout.alignment: Qt.AlignVCenter
        }
    }
}
