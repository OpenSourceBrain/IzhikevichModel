initOSBGeppetto("network", net1);
GEPPETTO.SceneController.addColorFunction(window.getRecordedMembranePotentials(), window.voltage_color);
window.setupColorbar(window.getRecordedMembranePotentials(), window.voltage_color, false, 'Voltage color scale', 'Membrane Potential (V)');
Project.getActiveExperiment().play({step: 10})
