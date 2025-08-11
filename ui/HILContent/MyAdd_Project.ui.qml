import QtQuick 6.7
import QtQuick.Controls 6.7

Row {
    id: add_row
    width: 150
    spacing: 5
    
    Button {
        id: btnCreateProject
        width: 150
        height: 55
        text: "+"
    }
    
    Connections {
        target: btnCreateProject
        function onClicked() {
            var newName = "New Project " + (configViewModel.projectsModel.rowCount(
                                                ) + 1)
            configViewModel.addProject(newName)
        }
    }
}
