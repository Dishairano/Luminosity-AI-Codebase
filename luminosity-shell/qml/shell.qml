// US5 / OS3 - Luminosity-schil (Kenji)
// De grafische schil van Luminosity OS, gebouwd met Quickshell (QML) op Hyprland.
// Toont een invoerbalk (gewone taal), een bevestigingskaart en een logboek.
// De schil voert zelf niets uit: hij roept de Python-engine aan via de CLI
// (optie A uit het ontwerp) en toont het antwoord.

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io

ShellRoot {
    PanelWindow {
        id: paneel
        anchors { top: true; left: true; right: true; bottom: true }
        color: "#11131a"

        property string invoer: ""
        property string titel: ""
        property string commando: ""
        property string uitleg: ""

        // Roept de engine aan: python -m luminosity_engine.cli "<invoer>"
        Process {
            id: engine
            command: ["python3", "-m", "luminosity_engine.cli", paneel.invoer]
            stdout: StdioCollector {
                onStreamFinished: paneel.uitleg = this.text
            }
        }

        ColumnLayout {
            anchors.centerIn: parent
            width: parent.width * 0.6
            spacing: 20

            // Topbalk met titel + statuswidgets (US7 — door Kenji uit te breiden)
            RowLayout {
                Layout.fillWidth: true
                Text { text: "☀ Luminosity"; color: "white"; font.pixelSize: 20 }
                Item { Layout.fillWidth: true }
                Text { text: "🔋  📶  🕐"; color: "#9aa0b4"; font.pixelSize: 16 }
            }

            Text {
                text: "Hoi! Wat wil je doen?"
                color: "#e8e8f0"; font.pixelSize: 24
            }

            // Invoerbalk (gewone taal)
            Rectangle {
                Layout.fillWidth: true
                height: 56; radius: 12; color: "#1b1e27"
                border.color: "#3a3f55"
                TextInput {
                    id: invoerveld
                    anchors.fill: parent
                    anchors.margins: 16
                    color: "white"; font.pixelSize: 18
                    verticalAlignment: TextInput.AlignVCenter
                    onAccepted: {
                        paneel.invoer = text
                        engine.running = true   // start de engine met deze opdracht
                    }
                }
            }

            // Bevestigingskaart (US2) — toont wat de engine teruggaf
            Rectangle {
                Layout.fillWidth: true
                visible: paneel.uitleg.length > 0
                radius: 14; color: "#1b1e27"; border.color: "#3a3f55"
                implicitHeight: kaarttekst.implicitHeight + 32
                Text {
                    id: kaarttekst
                    anchors.fill: parent; anchors.margins: 16
                    text: paneel.uitleg
                    color: "#e8e8f0"; font.pixelSize: 15; wrapMode: Text.WordWrap
                }
            }

            // TODO (Kenji): Uitvoeren/Annuleren-knoppen, statuswidgets (US7)
            // en het logboekpaneel (US8) toevoegen.
        }
    }
}
