import QtQuick 6.7
import QtQuick.Controls 6.7
import QtQuick.Layouts
import QtCharts
import HIL

Pane {
    id: it6302Config
    width: 1800
    height: 800
    z: 0
    property alias btnTest: button1
    property var configViewModel: backend?.configViewModel
    property var powerSupply: backend?.configViewModel?.currentProject?.powerSupply

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        Pane {
            id: pane
            width: 200
            height: 50
            Layout.fillWidth: true

            RowLayout {
                id: rowLayout
                anchors.fill: parent

                Label {
                    id: label
                    text: qsTr("通道:")
                }

                ComboBox {
                    id: comboBoxResource
                    model: configViewModel?.availableVisaResources
                    currentIndex: model.indexOf(powerSupply?.resource_name)
                }

                Label {
                    id: label1
                    text: qsTr("波特率:")
                }

                ComboBox {
                    id: comboBoxBaud
                    model: [9600, 19200, 38400, 57600, 115200]
                    currentIndex: model.indexOf(powerSupply?.baud_rate)
                }

                Item {
                    id: item1
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }

                Button {
                    id: button
                    text: qsTr("重置")
                }

                Connections {
                    target: button
                    function onClicked() {
                        configViewModel.resetPowerSupplySettings()
                    }
                }

                Button {
                    id: button1
                    text: qsTr("测试")
                    checkable: true
                }

                Connections {
                    target: button1
                    function onClicked() {
                        configViewModel.togglePowerSupplyTest(target.checked)
                    }
                }
            }
        }
        ScrollView {
            id: scrollView
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayout2
                width: scrollView.width - 10
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.topMargin: 0
                anchors.bottomMargin: 0

                PowerSupplyChannel {
                    id: ps_channel
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    title: qsTr("通道1")
                    voltagePlaceholder: qsTr("电压(0-30Volt)")
                    voltageField.text: powerSupply?.ch1?.voltage || ""
                    currentField.text: powerSupply?.ch1?.current || ""

                    Connections {
                        target: ps_channel.voltageField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyVoltage(0, parseFloat(target.text))
                        }
                    }
                    Connections {
                        target: ps_channel.currentField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyCurrent(0, parseFloat(target.text))
                        }
                    }

                }

                PowerSupplyChannel {
                    id: ps_channel1
                    title: qsTr("通道2")
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    voltagePlaceholder: qsTr("电压(0-30Volt)")
                    voltageField.text: powerSupply?.ch2?.voltage || ""
                    currentField.text: powerSupply?.ch2?.current || ""

                    Connections {
                        target: ps_channel1.voltageField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyVoltage(1, parseFloat(target.text))
                        }
                    }
                    Connections {
                        target: ps_channel1.currentField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyCurrent(1, parseFloat(target.text))
                        }
                    }
                }

                PowerSupplyChannel {
                    id: ps_channel2
                    title: qsTr("通道3")
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    voltagePlaceholder: qsTr("电压(0-5Volt)")
                    voltageField.text: powerSupply?.ch3?.voltage || ""
                    currentField.text: powerSupply?.ch3?.current || ""

                    Connections {
                        target: ps_channel2.voltageField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyVoltage(2, parseFloat(target.text))
                        }
                    }
                    Connections {
                        target: ps_channel2.currentField
                        function onEditingFinished() {
                            configViewModel.setPowerSupplyCurrent(2, parseFloat(target.text))
                        }
                    }
                }

                property int currentX: 0

                Connections {
                    target: backend?.configViewModel
                    function onPowerSupplyDataUpdated(voltage, current, power) {
                        console.log(`power supply data updated, ${voltage} - ${current} - ${power}`)
                        ps_channel.voltageSeries.append(columnLayout2.currentX, voltage[0]);
                        ps_channel.currentSeries.append(columnLayout2.currentX, current[0]);
                        ps_channel.powerSeries.append(columnLayout2.currentX, power[0]);

                        ps_channel1.voltageSeries.append(columnLayout2.currentX, voltage[1]);
                        ps_channel1.currentSeries.append(columnLayout2.currentX, current[1]);
                        ps_channel1.powerSeries.append(columnLayout2.currentX, power[1]);

                        ps_channel2.voltageSeries.append(columnLayout2.currentX, voltage[2]);
                        ps_channel2.currentSeries.append(columnLayout2.currentX, current[2]);
                        ps_channel2.powerSeries.append(columnLayout2.currentX, power[2]);

                        columnLayout2.currentX++;

                        ps_channel.voltageLabel.text = `电压: ${Util.formatData(voltage[0], 3, 6)}`
                        ps_channel.currentLabel.text = `电流: ${Util.formatData(current[0], 3, 6)}`
                        ps_channel.powerLabel.text = `功率: ${Util.formatData(power[0], 3, 6)}`

                        ps_channel1.voltageLabel.text = `电压: ${Util.formatData(voltage[1], 3, 6)}`
                        ps_channel1.currentLabel.text = `电流: ${Util.formatData(current[1], 3, 6)}`
                        ps_channel1.powerLabel.text = `功率: ${Util.formatData(power[1], 3, 6)}`

                        ps_channel2.voltageLabel.text = `电压: ${Util.formatData(voltage[2], 3, 6)}`
                        ps_channel2.currentLabel.text = `电流: ${Util.formatData(current[2], 3, 6)}`
                        ps_channel2.powerLabel.text = `功率: ${Util.formatData(power[2], 3, 6)}`
                    }
                }

            }
        }
    }


    Connections {
        target: comboBoxResource
        function onActivated(index) {
            console.log(`power supply config resource ${comboBoxResource.currentText}`)
            configViewModel.setPowerSupplyConfig(comboBoxResource.currentText, powerSupply.baud_rate)
        }
    }

    Connections {
        target: comboBoxBaud
        function onActivated(index) {
            console.log(`power supply config baud ${comboBoxBaud.currentText}`)
            configViewModel.setPowerSupplyConfig(powerSupply.resource_name, comboBoxBaud.currentText)
        }
    }

}
