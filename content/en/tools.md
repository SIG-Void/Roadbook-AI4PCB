To change a pin connection, edit the schematic and update the board. To check drill alignment, overlay the drill file and board outline.

## Open and edit the original project

- [KiCad](https://www.kicad.org/discover/) — Open the project file and select a connector in the schematic. Find the same reference in the board editor. Keep the project rules and libraries with the design for later checks. KiCad runs locally and is open source.
- [LibrePCB](https://librepcb.org/docs/user-manual/project-editor/output-jobs/) — Output Jobs define the artwork, drill data, and assembly files to generate. The editor and CLI can use the same settings for repeat releases. [CLI reference](https://librepcb.org/docs/cli/open-project/)
- [EasyEDA Pro](https://prodocs.easyeda.com/en/quick-start.html) — Edit the schematic and board in one project. Export Gerbers, a bill of materials, and placement coordinates. Match the references in the last two files before assembly. [Fabrication export](https://prodocs.easyeda.com/en/pcb/export-pcb-fabrication-file-gerber/index.html) · [Placement export](https://prodocs.easyeda.com/en/pcb/export-pick-and-place-file/)
- [Altium Designer](https://www.altium.com/documentation/altium-designer/preparing-for-manufacture/output-jobs) — Look for the project file and its `.OutJob` file. The latter specifies design sources, outputs, and validation reports. Check which board and assembly variant it selects before rebuilding a release.
- [Cadence Allegro X](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/allegro-x-design-platform.html) — In an Allegro project, inspect the spacing, electrical, and physical constraints that a net inherits. Confirm the rule set before comparing layouts. [Constraint hierarchy](https://community.cadence.com/cadence_blogs_8/b/pcb/posts/leverage-object-hierarchy-for-effective-constraint-management)

## Describe a circuit and test its behavior

- [SKiDL](https://github.com/devbisme/skidl) — Declare parts, pins, and nets in Python, then export a netlist. For a repeated circuit, inspect a supply net and a signal net across two channels.
- [atopile](https://github.com/atopile/atopile) — Describe reusable circuits in `.ato` modules. The build checks connections and constraints and updates a KiCad board. Keep the modules for subsequent edits.
- [ngspice](https://ngspice.sourceforge.io/) — Put the netlist, device models, and analysis directives in one input file. For an RC filter, read gain and phase from an AC sweep and step response from a transient analysis.
- [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/LTspice-simulator.html) — Draw a circuit, run the simulation with vendor device models, and select a node in the waveform viewer. Record the model, source settings, and output node when comparing simulators.
- [Siemens HyperLynx SI](https://www.siemens.com/en-us/products/pcb/hyperlynx/signal-integrity/) analyzes signal integrity. Post-layout analysis uses the routed interconnect and stackup. A digital interface may also require models of its driver and receiver. Read the models, data rate, and topology alongside each result.

## Place parts, route copper, and check the enclosure

- [Cypress](https://github.com/NVlabs/Cypress) — This analytical placer computes component positions from a board outline, parts, and nets. Hold fixed parts constant across methods. Compare overlaps and wirelength before testing whether the layouts can be routed.
- [Freerouting](https://github.com/freerouting/freerouting) — Export a Specctra DSN design, route it, then import the SES session into the board editor. Check the new copper against the original project rules.
- [PCBWorld](https://github.com/LGAI-Research/PCBWorld) — A policy acts through the KiCad router on a fixed placement. Use this environment to inspect individual actions or train a policy. [Training and reproduction](training.md)
- [KiCad StepUp](https://www.kicad.org/external-tools/stepup/) — Exchange board outlines and 3D models between FreeCAD and KiCad. Compare holes, edge connectors, and tall parts with the enclosure. Check the dimensions separately for parts without 3D models.

## Check and release manufacturing files

- [KiCad CLI](https://docs.kicad.org/10.0/en/cli/cli.html) — Run `sch erc` on a schematic and `pcb drc` on a board. Set `--exit-code-violations` when a job must fail on reported violations. [Worked board check](design-checks.md)
- [KiCad IPC API](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/index.html) — Use the API to read or edit objects in the editor. KiCad 9 and 10 require a running GUI for this API. The CLI can check or export files on disk.
- [KiBot](https://kibot.readthedocs.io/en/master/) — Put checks, exports, and packaging steps in a configuration file. Commit it alongside the design so another installation can generate the same set of outputs.
- [Ucamco Reference Gerber Viewer](https://www.ucamco.com/en/gerber/reference-gerber-viewer) — Open the Gerber and drill files intended for release. Overlay the outline, outer copper, and drill layers. Inspect the holes in a through-hole connector.
- [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) — Generate an interactive assembly drawing. Select a BOM group to locate its references on either side.
- [PcbDraw](https://github.com/yaqwsx/PcbDraw) — Render a KiCad board as SVG. Use Populate to show the parts to fit at each stage of hand assembly.

Follow the [board design review](design-review.md) to match the requirements to the design files and exported manufacturing data.
