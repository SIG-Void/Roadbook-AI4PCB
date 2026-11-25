A release review uses the component datasheet, the editable design, and the files that will go to the factory. Start at one component pin. Follow it into the layout, then inspect the exported layers and assembly records.

<h2 id="footprints">Check the datasheet against the footprint</h2>

**Match the pin numbers.** The onsemi BAT54SLT1G contains two series diodes in a SOT23 package. Pin 1 is the first anode. Pin 2 is the second cathode. Pin 3 joins the diodes. Read the net on each schematic pin, then select the three numbered pads in the footprint. A pad assigned to the wrong physical pin will carry the net to the wrong terminal. [BAT54SLT1G pin table](https://www.onsemi.com/pdf/datasheet/bat54slt1-d.pdf) · [KiCad SOT-23 footprint](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod)

**Measure the land pattern.** Check the exact part against its package drawing. For a process comparison, NXP shows separate SOT23 land patterns for reflow and wave soldering. Select the drawing for the assembly process. Check pad spacing and dimensions in the footprint editor. Inspect the assembly outline, silkscreen mark, and courtyard. Record the datasheet and library revisions. [Package drawing](https://www.nxp.com/docs/en/package-information/SOT23.pdf) · [KiCad footprint layers](https://gitlab.com/kicad/libraries/klc/-/tree/6e8cbad9556359879d2b91f904d6df82517d97d1/content/footprint/F5)

<h2 id="layout">Check placement and current paths</h2>

**Locate fixed features first.** Enclosure openings constrain connectors. Standoffs constrain mounting holes. Check the board outline and critical parts in the mechanical assembly. Verify plug clearance and screw access. Framework supplies electrical templates and mechanical files for the same expansion card. [Electrical templates](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Electrical/KiCad_templates) · [Mechanical files](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Mechanical)

**Follow the power loop.** In a buck converter, trace current in both switch states. Find the section with the largest change in current. Locate the input capacitor and switches on the board. Check the area enclosed by their connections. Analog Devices shows both switch states alongside physical layouts. [Application note AN-139](https://www.analog.com/en/resources/app-notes/an-139.html)

**Apply the rules for the actual interface.** Follow a differential pair from connector to receiver. Mark layer transitions and changes of reference plane. Check the spacing, impedance, and length requirements for that interface and stackup. After tuning, inspect the extra trace segments and their return path. [TI interface guidelines](https://www.ti.com/lit/an/spraar7j/spraar7j.pdf) · [KiCad differential routing](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#routing-differential-pairs)

<h2 id="fabrication">Review the files for fabrication and assembly</h2>

| Deliverable | Check the exported files | Example finding |
| --- | --- | --- |
| Outline, copper, and drills | Overlay the outline, outer copper, plated holes, and unplated holes in an independent viewer. Inspect a through-hole connector. | Shifted origin, missing drill file, or outline from another revision. |
| Bill of materials (BOM) | Select one reference from a group. Check its manufacturer part number, package, and assembly variant. | Wrong rating in the same package, or an unpopulated part in the order. |
| Component placement list (CPL) | On a polarized part, check the reference, units, side, orientation, and pin 1. | Mirrored coordinates, different origins, or a rotated part. |

Olimex provides the ESP32-PoE design in a directory marked M2. Its accompanying Gerber filenames say Rev_M. Those names alone do not identify the copper revision. Export the complete set from the selected project and record the revision and export settings. [M2 design](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2) · [Included Gerbers](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2/Gerbers) · [Ucamco viewer](https://www.ucamco.com/en/gerber/reference-gerber-viewer)

Match the BOM to the CPL by reference. Check that each part belongs in this assembly variant. Read [JLCPCB’s example](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad), then [change the origin on a two-sided board](assembly-origin.md) and compare the results.
