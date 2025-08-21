import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: pane1
    width: 1500
    height: 1000
    property var currentProj: null
    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        RowLayout {
            id: rowLayout2
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true

            TabBar {
                id: tabBar3
                currentIndex: swipeView.currentIndex
                TabButton {
                    id: tabButton8
                    width: 180
                    text: qsTr("电源")
                }

                TabButton {
                    id: tabButton9
                    width: 180
                    text: qsTr("DIO")
                }

                TabButton {
                    id: tabButton10
                    width: 180
                    text: qsTr("AO(PCI-1720U)")
                }
                Layout.preferredWidth: 900
                Layout.fillWidth: true
            }
            Item {
                id: item1
                width: 200
                Layout.fillHeight: false
                Layout.fillWidth: true
            }
            Button {
                id: button
                text: qsTr("启用")
                checked: false
                checkable: true
                state: ""
                enabled: currentProj
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }

            Connections {
                target: button
                function onClicked() {
                    if (currentProj && !currentProj.is_started) {
                        currentProj.start()
                        target.checked = true
                    }
                    else if (currentProj) {
                        currentProj.stop()
                        target.checked = false
                    }
                }
            }
        }

        SwipeView {
            id: swipeView
            width: 200
            height: 200
            z: -1
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillHeight: true
            Layout.fillWidth: true
            orientation: Qt.Horizontal
            currentIndex: tabBar3.currentIndex

            MyMainPowerSupply {
                id: powerSupply
                channels: backend?.mainViewModel?.currentProject?.powerSupply?.configuredChannels
            }
            MyMainDIO {
                id: dio
            }
        }
    }
}