## Connectors and mechanical fit

- [Framework Expansion Cards](https://github.com/FrameworkComputer/ExpansionCards) provides electrical and mechanical references for laptop expansion cards. Open the KiCad template. Use the mechanical drawings to check the connector position and board outline against the enclosure. [KiCad templates](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Electrical/KiCad_templates) · [Mechanical drawings](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Mechanical)

## Power and Ethernet

- [Olimex ESP32-PoE](https://github.com/OLIMEX/ESP32-POE) receives power over Ethernet. Open the revision M2 schematic and trace the power path from the Ethernet connector. Use the reference designators to find those parts in the matching KiCad board file. [Revision M2 design files](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2)

## A carrier board with multiple interfaces

- [Antmicro Jetson Nano Baseboard](https://github.com/antmicro/jetson-nano-baseboard) provides KiCad design files from revision 1.5 onward. Open `supply.kicad_sch`, `interfaces.kicad_sch`, or `csi.kicad_sch` for the power, peripheral, or camera circuits. Find Ethernet jack `J3` in the interface schematic. In the matching board file, pads 2 and 3 connect to `ENET_TRD0_P` and `ENET_TRD0_N`. Highlight either net to follow its copper tracks. [Interface schematic](https://github.com/antmicro/jetson-nano-baseboard/blob/d8d0b2d71ab4cc4bcdb204a09f78be40d4c8cda3/interfaces.kicad_sch) · [Matching board](https://github.com/antmicro/jetson-nano-baseboard/blob/d8d0b2d71ab4cc4bcdb204a09f78be40d4c8cda3/jetson-nano-baseboard.kicad_pcb)

See the [KiCad tutorial](https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html) for the steps to update a board from a schematic, place parts, and check the design rules.

## A minimal microcontroller board

The [Raspberry Pi RP2040 Minimal Viable Board](https://pip.raspberrypi.com/documents/RP-008296-DS) R3-S1 package contains the schematic, layout, BOM, and matching PDF. Locate pin 45 of U3, then highlight `+1V1` on the board. Follow the output of the internal regulator to the core supply pins. Raspberry Pi lists the Pico and Pico W Allegro designs separately. [Official design files](https://pip.raspberrypi.com/categories/814-rp2040) · [Worked netlist check](rp2040-power.md)
