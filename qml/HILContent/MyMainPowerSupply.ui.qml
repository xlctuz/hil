import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane4

    property var powerSupplyModel: null

    ColumnLayout {
        id: columnLayout1
        anchors.fill: parent

        Repeater {
            id: repeater
            model: powerSupplyModel ? powerSupplyModel.configuredChannels : []

            PowerSupplyMainChannel {
                titleText: qsTr("通道" + (modelData.index + 1))
                channel: modelData
            }
        }
    }
}
