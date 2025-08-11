import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane4
    
    ColumnLayout {
        id: columnLayout1
        x: -12
        y: -12
        anchors.fill: parent
        
        Repeater {
            id: repeater
            model: 3
            
            PowerSupplyMainChannel {
                id: powerMainChannel
                Layout.fillWidth: true
                x: 0
                y: 0
            }
        }
    }
}
