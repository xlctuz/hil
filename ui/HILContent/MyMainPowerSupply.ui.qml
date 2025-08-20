import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane4

    property var channels: 3

    ColumnLayout {
        id: columnLayout1
        x: -12
        y: -12
        anchors.fill: parent

        Repeater {
            id: repeater
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            model: channels

            PowerSupplyMainChannel {
                id: powerMainChannel
                Layout.fillWidth: true
                x: 0
                y: 0
            }
        }
    }
}
