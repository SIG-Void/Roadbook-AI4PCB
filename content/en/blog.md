Each note links to board files, measurements, or evaluation data. You can check dimensions and connections on a layout or recalculate a routing score from published results.

<h2 id="follow-the-board-into-manufacturing">Check dimensions and placement before fabrication and assembly</h2>

[Do the mounting holes match the enclosure?](design-checks.md) The enclosure drawing specifies 30 mm between the centers of the two mounting holes. On a practice board, moving the right hole 1 mm closer still produces zero design rule violations. [Measure the layout in KiCad](design-checks.md#start-with-the-enclosure-dimension) or [check the drill coordinates in a text editor](design-checks.md#where-will-the-drill-hit-h2).

[Did the part move, or did its coordinates change?](assembly-origin.md) An assembly shop uses a placement file to locate parts. A bottom-side capacitor has a positive X coordinate in one export and a negative value in another. Use a top-side part to check for a change of origin or a mirrored axis.

<h2 id="follow-a-schematic-onto-the-board">Trace power connections and check voltage readings</h2>

[Do pins on the same net have a copper connection?](rp2040-power.md) Find the 1.1 V supply on the RP2040 schematic. Follow it onto the board, remove a short trace on a copy, and see which check finds the gap.

[Why does the voltage reading change?](revision-task.md) The Glasgow board measures the voltage at its ports. An engineer added interference to a known voltage and compared the readings. Trace the decision to fit a capacitor and change a resistor back to those measurements.

<h2 id="read-training-data-and-evaluation-results">Read AI routing results and check test data</h2>

[At 94.9% average completion, how many boards passed?](routing-scores.md) Calculate two scores from the same results. First check what fraction of the connections each board completes. Then count boards with every connection complete and zero error-level violations.

[Can two revisions of one board test a model on a new design?](board-family-split.md) One board file has an extra resistor. Both files still export the same 142 placement rows. If a model trains on the older placement table, which positions in the newer table can test it on unseen data?
