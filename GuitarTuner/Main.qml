import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Tuner App")

    property color bgColor: "#1e1e1e"
    property string note: "--"
    property real frequency: 0.0
    property real cents: 0

    Rectangle {
        anchors.fill: parent
        color: {
            return "#1e1e1e"
        }
    }

    Connections {
        target: worker
        function onTextChanged(n, f, c) {
            note = n
            frequency = f
            cents = c
        }
    }

    GridLayout {
        columns: 2
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 40

        Button {
            text: "Start"
            Layout.preferredWidth: 120
            Layout.preferredHeight: 40

            onClicked: worker.start()

            background: Rectangle {
                color: "#2d2d2d"
                radius: 10
                border.color: "#00ff99"
            }

            contentItem: Text {
                text: "Start"
                color: "#00ff99"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Button {
            text: "Stop"
            Layout.preferredWidth: 120
            Layout.preferredHeight: 40

            onClicked: worker.stop()

            background: Rectangle {
                color: "#2d2d2d"
                radius: 10
                border.color: "red"
            }

            contentItem: Text {
                text: "Stop"
                color: "red"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    Rectangle {
        anchors.centerIn: parent
        width: 320
        height: 280
        radius: 20
        color: "#111111"
        border.color: "#00ff99"
        border.width: 2

        Column {
            anchors.centerIn: parent
            spacing: 10

            Text {
                text: "FREQUENCY"
                color: "#666"
                font.pixelSize: 14
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: note
                font.pixelSize: 60
                font.bold: true

                color: {
                    if (note === "--") return "#666666"
                    if (Math.abs(cents) < 5) return "#00ff99"
                    if (cents < 0) return "#3399ff"
                    return "#ff3333"
                }

                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: frequency > 0 ? frequency.toFixed(2) + " Hz" : "--"
                color: "#888"
                font.pixelSize: 28
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: {
                    if (note === "--") return ""
                    if (Math.abs(cents) < 5) return "●"
                    if (Math.abs(cents) < 15) return cents < 0 ? "↑" : "↓"
                    if (Math.abs(cents) < 40) return cents < 0 ? "↑↑" : "↓↓"
                    return cents < 0 ? "↑↑↑" : "↓↓↓"
                }

                font.pixelSize: 70

                color: {
                    if (note === "--") return "#666"
                    if (Math.abs(cents) < 5) return "#00ff99"
                    if (cents < 0) return "#3399ff"
                    return "#ff3333"
                }

                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }
}