import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

ColumnLayout {
    id: configView
    visible: true
    property alias tabBarChannel: tabBarChannel
    property alias btnDeleteProject: btnDeleteProject
    property alias it6302Config: it6302Config
    RowLayout {
        id: rowLayout2
        width: 100
        height: 100
        Item {
            id: item4
            width: 200
            height: 200
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        TabBar {
            id: tabBarChannel
            width: 240
            spacing: 10
            font.pointSize: 16
            font.bold: true
            TabButton {
                id: tabButton5
                text: qsTr("通道1")
            }

            TabButton {
                id: tabButton6
                x: 0
                y: 0
                text: qsTr("通道2")
            }

            TabButton {
                id: tabButton7
                text: qsTr("通道3")
            }
            Layout.preferredWidth: 500
        }

        Item {
            id: item5
            width: 200
            height: 200
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        Layout.minimumHeight: 80
        Layout.maximumHeight: 80
    }

    Pane {
        id: pane1
        width: 200
        height: 200
        leftPadding: 0
        rightPadding: 12
        Layout.fillWidth: true
        Layout.fillHeight: true

        RowLayout {
            id: rowLayout4
            anchors.fill: parent
            spacing: 5

            Pane {
                id: pane3
                width: 200
                height: 200
                Layout.fillHeight: true
                Layout.maximumWidth: 250
                Layout.minimumWidth: 200

                ScrollView {
                    id: scrollView1
                    anchors.fill: parent

                    MyListViewProj {
                        id: myListViewProj
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.leftMargin: 0
                        anchors.topMargin: 0
                        model: configViewModel?.projectsModel
                    }
                }
            }

            Pane {
                id: pane4
                width: 200
                height: 200
                z: -1
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    id: columnLayout1
                    anchors.fill: parent

                    RowLayout {
                        id: rowLayout6
                        width: 100
                        Layout.fillHeight: false
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.fillWidth: true

                        TextField {
                            id: textFieldProjectName
                            Layout.preferredWidth: 200
                            placeholderText: qsTr("项目名称")
                            text: configViewModel?.currentProject.name || ""
                            readOnly: true
                        }

                        Item {
                            id: item6
                            width: 200
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                        }
                        Button {
                            id: btnDeleteProject
                            text: qsTr("删除")
                        }
                    }
                    RowLayout {
                        id: rowLayout5
                        width: 100
                        height: 100
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.fillWidth: true
                        Layout.maximumHeight: 50
                        Layout.minimumHeight: 50

                        TabBar {
                            id: tabBar3
                            Layout.fillWidth: true
                            Layout.preferredWidth: 900
                            currentIndex: swipeView.currentIndex

                            TabButton {
                                id: tabButton8
                                width: 180
                                text: qsTr("电源(IT6302)")
                            }
                            TabButton {
                                id: tabButton9
                                width: 180
                                text: qsTr("DIO(PCIE-1762H)")
                            }
                            TabButton {
                                id: tabButton10
                                width: 180
                                text: qsTr("AO(PCI-1720U)")
                            }

                            TabButton {
                                id: tabButton11
                                width: 180
                                text: qsTr("RM555")
                            }

                            TabButton {
                                id: tabButton12
                                width: 180
                                text: qsTr("中盛数字IO")
                            }
                        }
                        Item {
                            id: item7
                            width: 200
                            height: 200
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                        }
                    }
                    Pane {
                        id: pane6
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        SwipeView {
                            id: swipeView
                            anchors.fill: parent
                            z: 0
                            currentIndex: tabBar3.currentIndex
                            clip: false
                            wheelEnabled: true
                            focusPolicy: Qt.NoFocus
                            orientation: Qt.Horizontal
                            interactive: true
                            MyIt6302Config {
                                id: it6302Config
                                height: swipeView.height
                                width: swipeView.width
                                powerSupply: configViewModel?.currentProject?.powerSupply
                            }

                            MyPcie1762hConfig {
                                id: pcie1762hConfig
                                height: swipeView.height
                                width: swipeView.width
                                pcie1762h: configViewModel?.currentProject?.pcie1762h
                            }

                            MyPci1720uConfig {
                                id: pci1720uConfig
                                height: swipeView.height
                                width: swipeView.width
                            }
                        }
                    }
                }
            }
        }
    }
}
