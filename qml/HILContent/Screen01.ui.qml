/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import HIL
import QtQuick.Layouts
import QtQuick.Studio.DesignEffects

Rectangle {
    id: mainScreen
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor
    property alias mainStack: mainStack
    property alias configView: configView

    /* property alias btnCreateProject: configView.btnCreateProject */
    /* property alias btnDeleteProject: configView.btnDeleteProject */
    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        z: 1

        RowLayout {
            id: rowLayout
            height: 60
            z: 0
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
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

                    /* Connections { */
                    /*     target: tabButton */
                    /*     function onClicked() { */
                    /*         if (mainStack.currentItem != mainView) { */
                    /*             mainStack.pop() */
                    /*             if (backend && backend.mainViewModel) { */
                    /*                 backend.mainViewModel.selectChannel(mainView.tabBarChannel.currentIndex) */
                    /*             } */
                    /*         } */
                    /*     } */
                    /* } */
                }

                TabButton {
                    id: tabButton1
                    x: 148
                    y: -24
                    text: qsTr("配置")

                    /* Connections { */
                    /*     target: tabButton1 */
                    /*     function onClicked() { */
                    /*         if (mainStack.currentItem != configView) { */
                    /*             mainStack.push(configView) */
                    /*             if (backend && backend.configViewModel) { */
                    /*                 backend.configViewModel.selectChannel(configView.tabBarChannel.currentIndex) */
                    /*             } */
                    /*         } */
                    /*     } */
                    /* } */
                }

                Connections {
                    target: tabBar
                    function onCurrentIndexChanged() {
                        if (tabBar.currentIndex == 0) {
                            backend.mainViewModel.selectChannel(mainView.tabBarChannel.currentIndex)
                        }
                        else {
                            backend.configViewModel.selectChannel(configView.tabBarChannel.currentIndex)
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
    }

    Page {
        id: page
        anchors.fill: parent
        Layout.fillWidth: true
        Layout.fillHeight: true

        StackLayout {
            id: mainStack
            anchors.fill: parent
            /* initialItem: mainView */
            currentIndex: tabBar.currentIndex

            MyMainView {
                id: mainView
            }

            MyConfigView {
                id: configView
            }
        }
    }
}
