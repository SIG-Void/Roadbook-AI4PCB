This is an English reading guide to the author’s [original Chinese article](../zh/workflow.md). The original includes the author’s examples, design trade-offs, and observations from work with AI tools.

## The two design files

A schematic describes the electrical connections between components. For a voltage regulator, it shows which supply feeds the input and which circuits draw power from the output.

A PCB file describes the physical board. It contains the board outline, component footprints, copper tracks, and vias. A via connects copper on different layers. The engineer brings the schematic connections into the board editor, then finds physical paths that satisfy the electrical and mechanical requirements.

The author treats the schematic as the start of PCB design. In the author’s experience, AI tools can help inspect connections and explain compiler messages. Placement and the choice between competing electrical and mechanical requirements still require engineering judgment.

## From requirements to a board

### Requirements and component selection

Identify the required functions, chips, interfaces, and electrical limits. Read the manufacturer’s datasheet for the exact part. Check its pinout, supply limits, register information, and package dimensions.

Check the footprint for the selected package. Parts from one family can have different pin counts or package dimensions. If the supplier provides a footprint, compare it with the package drawing.

### Circuit and schematic design

Start with the manufacturer’s reference circuit. Check the supply and interface requirements for each device. For analog circuits, consider component tolerances and matching. The choice of a resistor or capacitor can affect both circuit performance and the eventual placement.

The author describes using circuit simulation and, for some designs, a small prototype before transferring a circuit to the main board. Radio-frequency designs can also require measurement with a spectrum analyzer or a vector network analyzer.

### Check the schematic

Inspect the intended connections. Mark the pins that the design intentionally leaves open. Check symbol-to-footprint assignments before transferring the schematic to the PCB editor.

### Check the enclosure

Agree on the board outline, mounting points, connector positions, and available height. The author gives the example of a smartphone. Its camera and battery can leave an irregular space for the board. A footprint may fit inside the outline but still collide with a part above it.

### Place the components

Choose the position and orientation of each part in relation to its neighbors. Consider the electrical paths, part height, assembly space, and the location of connectors. If the available package gives a poor fit, revisit part selection.

The author identifies placement as a weak point in the AI tools examined. A tidy row of components can still produce a long or noisy electrical path.

### Route the board

Plan the power domains and the paths that carry high current. A design can require several rails, such as 5 V, 3.3 V, 1.8 V, and 1.2 V. Switching supplies can disturb sensitive circuits. The available board area and the required current paths affect the choice of placement.

Reserve space for sensitive analog and radio-frequency circuits early. When a datasheet asks for two parts to be close together, identify which electrical path the instruction protects. Recheck external connectors against the enclosure as the layout changes.

For manual routing, consider trace width, layer, direction changes, and via size and count. For high-speed signals, consult the requirements for each interface. Trace length and relative arrival time can matter. The original article gives examples of length tolerances in mils. Use the limits specified for the actual interface.

### Add copper zones

A copper zone can provide a wider current path than a narrow track. Assign each zone to its intended net. If a layer contains multiple supply voltages, inspect the zone boundaries, via connections, and the paths available to carry current.

### Run the final checks

Run the design rule check (DRC). Review missing connections and violations of the configured rules. Correct the reported problems, repeat the check, and review the resulting layout before ordering prototypes.

## Engineering judgment

The author gives an example of limited manufacturing margin. A trace close to the fabricator’s process limit can break during production. Initial tests can miss the break, leaving it to surface after component assembly. The [original article in Chinese](../zh/workflow.md) also describes how the author weighs these trade-offs when using AI tools.
