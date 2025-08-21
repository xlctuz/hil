import QtQuick 6.7
import QtQuick.Controls 6.7

Rectangle {
    id: rectangle1
    width: 30
    height: 30
    color: "#44ac34"
    radius: 15
    state: "NA"

    Label {
        id: label1
        color: "#f5f5f5"
        text: qsTr("高")
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    states: [
        State {
            name: "HIGH"
            PropertyChanges {
                target: label1
                text: qsTr("高")
            }
            PropertyChanges {
                target: rectangle1
                color: "#44ac34"
            }
        },
        State {
            name: "LOW"
            PropertyChanges {
                target: label1
                text: qsTr("低")
            }
            PropertyChanges {
                target: rectangle1
                color: "#e51b20"
            }
        },
        State {
            name: "NA"
            PropertyChanges {
                target: label1
                text: qsTr("NA")
            }
            PropertyChanges {
                target: rectangle1
                color: "#d9d9d9"
            }
        }
    ]
}
