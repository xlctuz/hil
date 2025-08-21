// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import HIL
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: app
    width: Constants.width
    height: Constants.height

    visible: true
    title: "HIL"

    Screen01 {
        id: mainScreen
        anchors.fill: parent

    }


    Dialog {
        id: errorDialog
        title: "错误"
        standardButtons: Dialog.Ok
        modal: true
        anchors.centerIn: parent

        Label {
            id: errorMessageLabel
            text: ""
            wrapMode: Text.WordWrap
        }
    }

    /* Connections { */
    /*     target: backend?.configViewModel */
    /*     function onPowerSupplyTestFailed(message) { */
    /*         errorMessageLabel.text = message */
    /*         errorDialog.open() */
    /*         // Reset the test button state */
    /*         if (mainScreen.mainStack.currentItem === mainScreen.configView) { */
    /*             mainScreen.configView.it6302Config.btnTest.checked = false */
    /*         } */
    /*     } */
    /* } */
    
    // Add connection for power supply data updates
    /* Connections { */
    /*     target: backend?.configViewModel */
    /*     function onPowerSupplyDataUpdated(voltage, current, power) { */
    /*         // This signal is handled in MyIt6302Config.ui.qml */
    /*     } */
    /* } */
}
