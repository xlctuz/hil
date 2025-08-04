import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts

Pane {
    id: it6302Config
    z: 0
    
    ScrollView {
        id: scrollView
        anchors.fill: parent
        
        ColumnLayout {
            id: columnLayout2
            width: 500
            height: 600
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.topMargin: 0
            
            GroupBox {
                id: groupBox
                Layout.minimumHeight: 150
                Layout.minimumWidth: 300
                Layout.fillHeight: true
                Layout.fillWidth: true
                title: qsTr("通道1")
                
                GridLayout {
                    id: gridLayout
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    uniformCellWidths: true
                    uniformCellHeights: true
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    rows: 2
                    columns: 2
                    
                    Label {
                        id: label4
                        text: qsTr("设置电压")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillHeight: false
                        Layout.fillWidth: false
                    }
                    
                    TextField {
                        id: textField1
                        Layout.fillHeight: false
                        Layout.fillWidth: false
                        placeholderText: qsTr("电压值(Volt)")
                    }
                    
                    Label {
                        id: label5
                        text: qsTr("设置电流上限")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillHeight: false
                        Layout.fillWidth: false
                    }
                    
                    TextField {
                        id: textField2
                        Layout.fillHeight: false
                        Layout.fillWidth: false
                        placeholderText: qsTr("电流值(A)")
                    }
                }
            }
            
            GroupBox {
                id: groupBox1
                Layout.minimumHeight: 150
                Layout.minimumWidth: 300
                Layout.fillHeight: true
                Layout.fillWidth: true
                title: qsTr("通道2")
                
                GridLayout {
                    id: gridLayout1
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    uniformCellWidths: true
                    uniformCellHeights: true
                    rows: 2
                    Label {
                        id: label6
                        text: qsTr("设置电压")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    TextField {
                        id: textField3
                        placeholderText: qsTr("电压值(Volt)")
                    }
                    
                    Label {
                        id: label7
                        text: qsTr("设置电流上限")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    TextField {
                        id: textField4
                        placeholderText: qsTr("电流值(A)")
                    }
                    columns: 2
                }
            }
            
            GroupBox {
                id: groupBox2
                Layout.minimumHeight: 150
                Layout.minimumWidth: 300
                Layout.fillHeight: true
                Layout.fillWidth: true
                title: qsTr("通道3")
                
                GridLayout {
                    id: gridLayout2
                    anchors.fill: parent
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    uniformCellWidths: true
                    uniformCellHeights: true
                    rows: 2
                    Label {
                        id: label8
                        text: qsTr("<b>设置电压</b><br><font size=8pt>取值范围(0, 6)</font>")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        textFormat: Text.RichText
                        font.bold: false
                    }
                    
                    TextField {
                        id: textField5
                        placeholderText: qsTr("电压值(V)")
                    }
                    
                    Label {
                        id: label9
                        text: qsTr("设置电流上限")
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    TextField {
                        id: textField6
                        placeholderText: qsTr("电流值(A)")
                    }
                    columns: 2
                }
            }
        }
    }
}
