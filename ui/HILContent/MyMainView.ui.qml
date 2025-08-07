import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

ColumnLayout {
    id: mainView
    visible: true
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
