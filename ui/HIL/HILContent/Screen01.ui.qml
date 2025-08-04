

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.7
import QtQuick.Controls 6.7
import HIL
import QtQuick.Layouts
import QtCharts
import QtQuick.Studio.DesignEffects

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Button {
        id: button
        text: qsTr("Press me")
        anchors.verticalCenter: parent.verticalCenter
        checkable: true
        anchors.horizontalCenter: parent.horizontalCenter

        Connections {
            target: button
            onClicked: animation.start()
        }
    }

    Text {
        id: label
        text: qsTr("Hello HIL")
        anchors.top: button.bottom
        font.family: Constants.font.family
        anchors.topMargin: 45
        anchors.horizontalCenter: parent.horizontalCenter

        SequentialAnimation {
            id: animation

            ColorAnimation {
                id: colorAnimation1
                target: rectangle
                property: "color"
                to: "#2294c6"
                from: Constants.backgroundColor
            }

            ColorAnimation {
                id: colorAnimation2
                target: rectangle
                property: "color"
                to: Constants.backgroundColor
                from: "#2294c6"
            }
        }
    }

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        RowLayout {
            id: rowLayout
            height: 60
            Layout.minimumHeight: 80
            Layout.maximumHeight: 80
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            spacing: 10

            TabBar {
                id: tabBar
                visible: true
                position: TabBar.Header
                Layout.maximumWidth: 180
                Layout.minimumWidth: 180
                spacing: 20
                Layout.fillWidth: false
                transformOrigin: Item.Center
                Layout.preferredWidth: -1
                Layout.margins: 0
                Layout.fillHeight: false
                font.bold: true
                font.pointSize: 20

                TabButton {
                    id: tabButton
                    x: 148
                    y: -24
                    text: qsTr("主页")

                    Connections {
                        target: tabButton
                        onClicked: {
                            if (mainStack.currentItem != mainView) {
                                mainStack.pop()
                            }
                        }
                    }
                }

                TabButton {
                    id: tabButton1
                    x: 148
                    y: -24
                    text: qsTr("配置")

                    Connections {
                        target: tabButton1
                        onClicked: {
                            if (mainStack.currentItem != configView) {
                                mainStack.push(configView)
                            }
                        }
                    }
                }
            }

            Item {
                id: item1
                width: 200
                height: 200
                Layout.fillHeight: true
                Layout.fillWidth: true
            }

            Image {
                id: image
                width: 150
                height: 70
                source: "../images/suresoft.png"
                Layout.rightMargin: 20
                sourceSize.height: 70
                sourceSize.width: 150
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                Layout.preferredWidth: -1
                Layout.fillWidth: false
                Layout.fillHeight: true
                fillMode: Image.PreserveAspectFit
            }
        }

        Page {
            id: page
            width: 200
            height: 200
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: mainView
                visible: true
                anchors.fill: parent

                RowLayout {
                    id: rowLayout1
                    width: 100
                    height: 100
                    Layout.maximumHeight: 80
                    Layout.minimumHeight: 80

                    Item {
                        id: item3
                        width: 200
                        height: 200
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                    TabBar {
                        id: tabBar1
                        width: 240
                        Layout.preferredWidth: 500
                        spacing: 10
                        font.bold: true
                        font.pointSize: 16

                        TabButton {
                            id: tabButton2
                            text: qsTr("通道1")
                        }

                        TabButton {
                            id: tabButton3
                            x: 0
                            y: 0
                            text: qsTr("通道2")
                        }

                        TabButton {
                            id: tabButton4
                            text: qsTr("通道3")
                        }
                    }

                    Item {
                        id: item2
                        width: 200
                        height: 200
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }

                Pane {
                    id: pane
                    width: 300
                    height: 200
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    RowLayout {
                        id: rowLayout3
                        anchors.fill: parent

                        Pane {
                            id: pane2
                            width: 300
                            height: 200
                            Layout.fillWidth: false
                            leftPadding: 0
                            Layout.maximumWidth: 300
                            Layout.minimumWidth: 200
                            Layout.fillHeight: true

                            ScrollView {
                                id: scrollView2
                                anchors.fill: parent

                                MyListViewProj {
                                    id: listViewProj
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    anchors.bottom: parent.bottom
                                    anchors.topMargin: 0
                                    model: ProjModel
                                }
                            }
                        }
                    }
                }
            }

            ColumnLayout {
                id: configView
                visible: true
                anchors.fill: parent
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
                        id: tabBar2
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
                            Layout.maximumWidth: 300
                            Layout.minimumWidth: 250

                            ScrollView {
                                id: scrollView1
                                anchors.fill: parent

                                MyListViewProj {
                                    id: myListViewProj
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    model: ProjModel
                                    footer: Row {
                                        id: row
                                        width: 200
                                        spacing: 5

                                        Button {
                                            id: btnProject
                                            width: 200
                                            height: 55
                                            text: "+"
                                        }
                                    }
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
                                    height: 100
                                    Layout.maximumHeight: 70
                                    Layout.minimumHeight: 70
                                    Layout.fillWidth: true

                                    TextField {
                                        id: textField
                                        Layout.preferredWidth: 200
                                        placeholderText: qsTr("项目名称")
                                    }

                                    Item {
                                        id: item6
                                        width: 200
                                        height: 200
                                        Layout.fillHeight: true
                                        Layout.fillWidth: true
                                    }
                                    Button {
                                        id: deleteProj
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
                                        }

                                        MyPcie1762hConfig {
                                            id: pcie1762hConfig
                                            height: swipeView.height
                                            width: swipeView.width
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
            StackView {
                id: mainStack
                anchors.fill: parent
                initialItem: mainView
            }
        }
    }
    states: [
        State {
            name: "clicked"
            when: button.checked

            PropertyChanges {
                target: label
                text: qsTr("Button Checked")
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0;formeditorColor:"#00000c"}D{i:17;invisible:true}D{i:85}D{i:88}
}
##^##*/

