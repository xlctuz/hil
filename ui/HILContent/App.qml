// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick 6.7
import HIL

Window {
    id: app
    width: Constants.width
    height: Constants.height

    visible: true
    title: "HIL"

    Screen01 {
        id: mainScreen
        anchors.fill: parent

        /* configView.Component.onCompleted: configViewModel.onConfigViewCompleted */
        /* tabBarChannel.onCurrentIndexChanged: function(currentIndex) { configViewModel.selectChannel(currentIndex) } */
    }

    function selectButton(model, index) {

        console.log(`model ${model.count}`)
        for (var i = 0; i < model.count; i++) {
            if (i !== index) {
                model.set(i, { "checked": false });
                console.log(`model checked ${model.get(i).checked}`)
            }
            else {
                model.set(i, {"checked": true});
            }
        }
    }

    Connections {
        target: mainScreen.configView
        Component.onCompleted: function() {configViewModel.selectChannel(0) }
    }

    Connections {
        target: mainScreen.configView.tabBarChannel
        function onCurrentIndexChanged() {
            console.log(`channel index changed ${target.currentIndex}`)
            configViewModel.selectChannel(target.currentIndex)
        }
    }
}
