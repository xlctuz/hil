import QtQuick 6.7
import QtQuick.Controls 6.7

ListView {
    id: listViewProj
    delegate: Row {
        id: row
        width: 200
        spacing: 5

        Button {
            id: btnProject
            width: 200
            height: 55
            text: model.name
            checked: model.checked
            checkable: true
        }

        Connections {
            target: btnProject
            function onClicked() {
                configViewModel.selectProject(index)
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorColor:"#00000c"}
}
##^##*/

