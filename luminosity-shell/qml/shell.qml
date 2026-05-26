// US5 / OS3 - Luminosity-schil (Kenji)
// De grafische schil van Luminosity OS, gebouwd met Quickshell (QML) op Hyprland.
// Toont een invoerbalk (gewone taal), statuswidgets, een bevestigingskaart met
// Uitvoeren/Annuleren-knoppen, een resultaatregel en een logboekpaneel (US8).
//
// De schil voert zelf NIETS uit. Hij praat met de Python-engine via de
// JSON-CLI (optie A uit het ontwerp):
//   stap 1 (voorbereiden):  python3 -m luminosity_engine.cli --json "<invoer>"
//   stap 2 (uitvoeren):     python3 -m luminosity_engine.cli --run --json "<invoer>"
//   annuleren:              python3 -m luminosity_engine.cli --cancel --json "<invoer>"
//   logboek:                python3 -m luminosity_engine.cli --logboek
// Alle logica (vertaling, veiligheid, logging) blijft in de engine.

import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io

ShellRoot {
    PanelWindow {
        id: paneel
        anchors { top: true; left: true; right: true; bottom: true }
        color: "#11131a"

        // --- Toestand van de schil ---
        property string invoer: ""
        property string titel: ""
        property string commando: ""
        property string uitleg: ""
        property string veiligheidstekst: ""
        property bool   magUitvoeren: false
        property bool   extraWaarschuwing: false
        property bool   heeftBevestiging: false
        property string resultaat: ""
        property bool   bezig: false
        property var    logregels: []

        // Helper: bouwt het engine-commando met de juiste vlaggen.
        function engineArgs(extra) {
            var a = ["-m", "luminosity_engine.cli", "--json"];
            for (var i = 0; i < extra.length; i++) a.push(extra[i]);
            a.push(paneel.invoer);
            return ["python3"].concat(a);
        }

        // Stap 1: bereid een opdracht voor (voert niets uit).
        Process {
            id: voorbereiden
            stdout: StdioCollector {
                onStreamFinished: paneel.verwerkAntwoord(this.text)
            }
            onRunningChanged: if (!running) paneel.bezig = false
        }

        // Stap 2: voer uit OF annuleer (krijgt --run of --cancel mee).
        Process {
            id: uitvoeren
            stdout: StdioCollector {
                onStreamFinished: paneel.verwerkAntwoord(this.text)
            }
            onRunningChanged: if (!running) { paneel.bezig = false; paneel.verversLogboek() }
        }

        // Leest het logboek voor het logboekpaneel (US8).
        Process {
            id: logboek
            command: ["python3", "-m", "luminosity_engine.cli", "--logboek"]
            stdout: StdioCollector {
                onStreamFinished: {
                    try { paneel.logregels = JSON.parse(this.text); } catch (e) { }
                }
            }
        }

        // Verwerkt het JSON-antwoord van de engine en vult de UI-velden.
        function verwerkAntwoord(tekst) {
            try {
                var data = JSON.parse(tekst);
                var b = data.bevestiging;
                paneel.titel = b.titel;
                paneel.commando = b.commando;
                paneel.uitleg = b.uitleg;
                paneel.veiligheidstekst = b.veiligheidstekst;
                paneel.magUitvoeren = b.mag_uitvoeren;
                paneel.extraWaarschuwing = b.extra_waarschuwing;
                paneel.heeftBevestiging = true;
                paneel.resultaat = data.resultaat ? data.resultaat.uitvoer : "";
            } catch (e) {
                paneel.uitleg = "Kon het antwoord van de engine niet lezen.";
            }
        }

        function start(tekst) {
            paneel.invoer = tekst;
            paneel.resultaat = "";
            paneel.heeftBevestiging = false;
            paneel.bezig = true;
            voorbereiden.command = engineArgs([]);
            voorbereiden.running = true;
        }
        function bevestig() {
            paneel.bezig = true;
            uitvoeren.command = engineArgs(["--run"]);
            uitvoeren.running = true;
        }
        function annuleer() {
            paneel.bezig = true;
            uitvoeren.command = engineArgs(["--cancel"]);
            uitvoeren.running = true;
        }
        function verversLogboek() { logboek.running = true; }

        Component.onCompleted: verversLogboek()

        ColumnLayout {
            anchors.centerIn: parent
            width: parent.width * 0.6
            spacing: 18

            // Topbalk met titel + statuswidgets (US7)
            RowLayout {
                Layout.fillWidth: true
                Text { text: "☀ Luminosity"; color: "white"; font.pixelSize: 20 }
                Item { Layout.fillWidth: true }
                Text {
                    text: paneel.bezig ? "● bezig…" : "● klaar"
                    color: paneel.bezig ? "#e0b341" : "#5bd17a"; font.pixelSize: 14
                }
                Text { text: "  🔋  📶  🕐"; color: "#9aa0b4"; font.pixelSize: 16 }
            }

            Text {
                text: "Hoi! Wat wil je doen?"
                color: "#e8e8f0"; font.pixelSize: 24
            }

            // Invoerbalk (gewone taal)
            Rectangle {
                Layout.fillWidth: true
                height: 56; radius: 12; color: "#1b1e27"; border.color: "#3a3f55"
                TextInput {
                    id: invoerveld
                    anchors.fill: parent; anchors.margins: 16
                    color: "white"; font.pixelSize: 18
                    verticalAlignment: TextInput.AlignVCenter
                    onAccepted: if (text.length > 0) paneel.start(text)
                }
            }

            // Bevestigingskaart (US2) met commando, uitleg en veiligheidsmelding
            Rectangle {
                Layout.fillWidth: true
                visible: paneel.heeftBevestiging
                radius: 14; color: "#1b1e27"; border.color: "#3a3f55"
                implicitHeight: kaartkolom.implicitHeight + 32
                ColumnLayout {
                    id: kaartkolom
                    anchors.fill: parent; anchors.margins: 16
                    spacing: 8
                    Text { text: paneel.titel; color: "white"; font.pixelSize: 18; font.bold: true }
                    Text {
                        visible: paneel.commando.length > 0
                        text: "$ " + paneel.commando
                        color: "#8ad0ff"; font.family: "monospace"; font.pixelSize: 14
                        Layout.fillWidth: true; wrapMode: Text.WrapAnywhere
                    }
                    Text {
                        text: paneel.uitleg; color: "#e8e8f0"; font.pixelSize: 15
                        Layout.fillWidth: true; wrapMode: Text.WordWrap
                    }
                    Text {
                        visible: paneel.veiligheidstekst.length > 0
                        text: paneel.veiligheidstekst
                        color: paneel.magUitvoeren ? "#e0b341" : "#ff6b6b"
                        font.pixelSize: 14; Layout.fillWidth: true; wrapMode: Text.WordWrap
                    }

                    // Uitvoeren / Annuleren-knoppen
                    RowLayout {
                        spacing: 12
                        visible: paneel.magUitvoeren && paneel.resultaat.length === 0

                        Rectangle {
                            width: 140; height: 40; radius: 8
                            color: paneel.extraWaarschuwing ? "#a8631f" : "#2f7d4f"
                            Text {
                                anchors.centerIn: parent; color: "white"; font.pixelSize: 15
                                text: paneel.extraWaarschuwing ? "Toch uitvoeren" : "Uitvoeren"
                            }
                            MouseArea { anchors.fill: parent; onClicked: paneel.bevestig() }
                        }
                        Rectangle {
                            width: 120; height: 40; radius: 8; color: "#3a3f55"
                            Text { anchors.centerIn: parent; text: "Annuleren"; color: "white"; font.pixelSize: 15 }
                            MouseArea { anchors.fill: parent; onClicked: paneel.annuleer() }
                        }
                    }
                }
            }

            // Resultaat-/uitvoervenster (engine output rendering)
            Rectangle {
                Layout.fillWidth: true
                visible: paneel.resultaat.length > 0
                radius: 12; color: "#0e1726"; border.color: "#26405f"
                implicitHeight: resultaattekst.implicitHeight + 24
                Text {
                    id: resultaattekst
                    anchors.fill: parent; anchors.margins: 12
                    text: paneel.resultaat
                    color: "#cfe8ff"; font.family: "monospace"; font.pixelSize: 13
                    wrapMode: Text.WrapAnywhere
                }
            }

            // Logboekpaneel (US8) — laatste opdrachten met status
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 180
                radius: 12; color: "#15171f"; border.color: "#2a2e3c"
                ColumnLayout {
                    anchors.fill: parent; anchors.margins: 12; spacing: 6
                    Text { text: "Logboek"; color: "#9aa0b4"; font.pixelSize: 14; font.bold: true }
                    ListView {
                        Layout.fillWidth: true; Layout.fillHeight: true
                        clip: true
                        model: paneel.logregels
                        delegate: RowLayout {
                            width: ListView.view.width; spacing: 10
                            Text {
                                text: {
                                    var s = modelData.status;
                                    return s === "geslaagd" ? "✓" : s === "geannuleerd" ? "⊘"
                                         : s === "geblokkeerd" ? "⛔" : "✗";
                                }
                                color: modelData.status === "geslaagd" ? "#5bd17a"
                                     : modelData.status === "geannuleerd" ? "#9aa0b4" : "#ff6b6b"
                                font.pixelSize: 13
                            }
                            Text {
                                text: modelData.invoertekst; color: "#e8e8f0"; font.pixelSize: 13
                                Layout.fillWidth: true; elide: Text.ElideRight
                            }
                            Text { text: modelData.tijdstip.split("T")[1]; color: "#6b7080"; font.pixelSize: 12 }
                        }
                    }
                }
            }
        }
    }
}
