import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: mainAoPane
    width: 1500
    height: 1000

    property var aoModel: null

    ScrollView {
        anchors.fill: parent
        clip: true

        Flow {
            width: parent.width
            spacing: 10
            padding: 10

            Repeater {
                model: aoModel ? aoModel.configuredChannels : []

                GroupBox {
                    title: modelData.name || `Channel ${modelData.index}`
                    width: 250
                    height: 100

                    Label {
                        text: `${modelData.voltage.toFixed(2)} V`
                        font.pixelSize: 24
                        anchors.centerIn: parent
                    }
                }
            }
        }
    }
}
