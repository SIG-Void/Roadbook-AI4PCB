# How to check the quality of PCB design files

Pick one pin on the schematic. Find where it should connect. Then open the board layout from the same revision and follow the copper to that connection.

## Four checks for one board

| What to check | What good records show | Signs of a problem |
| --- | --- | --- |
| Editable files | You can select a pin in the schematic and a pad or trace in the layout. | A folder labeled “complete project” contains only a PDF, Gerber files, and drill files. The editable design files are missing. |
| Matching revisions | Both files come from the same release. A pin on a component such as U3 has the same net name as its pad on the board. | The schematic shows a new connector. The layout still has the old connector with a different pad count. |
| Routing status | A layout in progress identifies the connections that still need routing. On a fully routed board, the connectivity check confirms that copper connects the pads that share each net. | The layout is marked “fully routed,” but a connectivity check finds a power pad with no copper connection. |
| Hardware tests | A test record identifies the board revision. For a power supply, it gives the test point, load, and measured voltage. | The notes claim a measured output of 3.3 V. The only record is a 3.3 V label on the schematic. |

For a collection, count **board designs and revisions** separately. If only the connector changes on a product, count **one board design and two revisions**.

## A power connection on the RP2040 board

The Raspberry Pi R3-S1 schematic shows a 1.1 V supply from pin 45 of U3 to pins 23 and 50. Use Highlight Net on pad 45 in the board layout. All three pads light up and belong to `+1V1`. The adjacent pad 44 belongs to `+3V3`. [Download the original board and schematic](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008296-DS-2-Minimal-KiCAD.zip)

We removed one trace leading to pad 50 on a copy. All three pads kept the same net name. In the KiCad PCB Editor, run the Design Rules Checker. Open the Unconnected Items tab. The original had **zero items**. The copy had **one**, next to pad 50. [See the gap and the check results](rp2040-power.md)
