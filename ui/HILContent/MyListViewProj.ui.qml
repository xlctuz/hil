import QtQuick 6.7
import QtQuick.Controls 6.7

ListView {
    id: listViewProj
    property bool showFooter: true
    property var projectModel: null

    delegate: Row {
        id: row
        width: 150
        spacing: 5

        Button {
            id: btnProject
            width: 150
            height: 55
            text: model.name
            checked: model.checked
            checkable: true
        }

        Connections {
            target: btnProject
            function onClicked() {
                projectModel?.selectProject(index)
            }
        }
    }

    footer: MyAdd_Project {
        id: add_row
        visible: showFooter
    }
}

/*##^##
Designer {
    D{i:0;formeditorColor:"#00000c"}
}
##^##*/

