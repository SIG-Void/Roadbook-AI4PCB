# Mini Encabulator KiCad PCB layout

Create a routed board for the SN25 Polycase enclosure. Start with `/app/input/mini_encabulator.kicad_sch`, which contains the component connections and footprint assignments.

1. Import the assigned footprints from the schematic.
2. Place the components inside the enclosure.
3. Place four M3 mounting holes in a rectangle. The center spacing is 1.575 inches by 1.26 inches.
4. Draw the board outline on `Edge.Cuts`.
5. Route all electrical connections.
6. Add and fill GND zones on `F.Cu` and `B.Cu`. Connect them with ground stitching vias.
7. Run KiCad DRC. Resolve all violations and unconnected items.
8. Save the board as `/app/output/mini_encabulator.kicad_pcb`.

The original ALE task uses KiCad on Windows and requires opening the schematic in KiCad. This Harbor adaptation uses KiCad command-line tools on Linux. You can also edit the supplied schematic in desktop KiCad 10.0.0.
