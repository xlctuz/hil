import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

ColumnLayout {
    id: mainView
    width: 1500
    height: 800
    visible: true
    property var mainViewModel: backend?.mainViewModel
    property alias tabBarChannel: tabBar1

    RowLayout {
        id: rowLayout1
        width: 100
        height: 100
        z: 1
        Layout.maximumHeight: 80
        Layout.minimumHeight: 80

        Item {
            id: item3
            width: 200
            height: 200
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Connections {
            target: tabBar1
            function onCurrentIndexChanged() {
                console.log(`channel index changed ${target.currentIndex}`)
                mainViewModel.selectChannel(target.currentIndex)
            }
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

    RowLayout {
        id: rowLayout3
        spacing: 0
        Layout.fillHeight: true
        Layout.fillWidth: true
        z: 0

        Pane {
            id: pane2
            width: 200
            height: 200
            z: 1
            Layout.fillWidth: false
            leftPadding: 0
            Layout.maximumWidth: 250
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
                    anchors.leftMargin: 12
                    anchors.topMargin: 0
                    model: mainViewModel?.projectsModel
                    showFooter: false
                    projectModel: mainViewModel
                }
            }
        }

        MyMainProjView {
            id: projectDetail
            Layout.fillHeight: true
            Layout.fillWidth: true
            currentProj: mainViewModel?.currentProject
        }
    }

    Connections {
        target: mainView
        Component.onCompleted: function () {
            mainViewModel.selectChannel(0)
        }
    }
}
