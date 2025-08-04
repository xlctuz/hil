// main.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// 应用程序的根组件，提供了窗口管理功能
ApplicationWindow {
    id: window
    width: 800
    height: 600
    visible: true
    title: "Hil App"

    // 在这里，你可以定义一个主题属性，以便 Python 端可以轻松切换
    // 这将链接到我们之前讨论的主题系统
    /* property Theme theme: MyTheme // 假设 MyTheme 是你的主题文件 */

    // 一个简单的布局，将所有内容垂直排列

    header: RowLayout {
        height: 100
        spacing: 10 // 設定元件之間的間距
        anchors.margins: 20
        Image {
            Layout.preferredWidth: 191
            Layout.preferredHeight: 69
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            source: "images/suresoft.png"
            fillMode: Image.PreserveAspectFit
        }
        TabBar {
            Layout.fillHeight: true
            TabButton {
                text: qsTr("主页")
            }
            TabButton {
                text: qsTr("配置")
            }
        }
    }

}
