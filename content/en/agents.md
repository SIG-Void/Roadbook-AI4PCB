These tools can read a KiCad board, edit a schematic, or send a board to a router.

## Read an existing design

- [KiCad Happy](https://github.com/aklofas/kicad-happy) (MIT) supplies standalone Python analyzers. The board analyzer reads a `.kicad_pcb` file. The schematic analyzer reads a `.kicad_sch` file. The authors published a review of a robot controller. Its power section follows the supply nets to a regulator and uses the feedback resistors to estimate its output voltage. [Example report](https://github.com/aklofas/kicad-happy/blob/main/example-report-1.md)
- [Backplane](https://github.com/BackplaneWorks/Backplane) (MIT for the main application) places the agent, schematic, board, and 3D view in one workspace. Select a connector pin to highlight the corresponding net on the board. During review, compare changes by sheet or layer. [Design review guide](https://github.com/BackplaneWorks/Backplane/blob/main/docs/design-review.md)

## Edit a schematic and check its records

- [Copper](https://github.com/claynicholson/copper-kicad-mcp) (MIT) connects an AI client to KiCad 10 through the Model Context Protocol (MCP). Specify a connection by reference and pin name. KiCad can then check the electrical rules and export the drawing. The client supplies the language model. The repository includes installers and board renders, including a small keypad. [Releases](https://github.com/claynicholson/copper-kicad-mcp/releases/latest)
- [Copperhead](https://github.com/copperheadhq/copperhead) (Apache-2.0) keeps requirements, KiCad files, and check results in one Git project. Start with the author's USB-C power breakout brief. Follow the checks and compare component values against the bill of materials. The authors report offline tests for the checks. Their end-to-end acceptance tests with a live model still await confirmation. [USB-C design brief](https://github.com/copperheadhq/copperhead/blob/main/examples/simple/usb-c-breakout.md)

## Send a board to a router

- [DeepPCB KiCad plugin](https://github.com/instadeepai/deeppcb-kicad-plugin) (Apache-2.0 for the plugin) submits a board from the KiCad editor and imports the routing result. The router runs on the DeepPCB cloud service. It requires an account, an API key, and service credits. Open the returned board next to the input board to compare open connections and rule violations. [Plugin releases](https://github.com/instadeepai/deeppcb-kicad-plugin/releases)

## Try the board analyzer

Download the [reference board](../../assets/examples/hole-spacing/reference.kicad_pcb) and the [modified board](../../assets/examples/hole-spacing/shifted.kicad_pcb). Put the files in the root of the KiCad Happy repository. Run each command from that directory.

```sh
python3 skills/kicad/scripts/analyze_pcb.py reference.kicad_pcb --full -o reference-analysis.json
python3 skills/kicad/scripts/analyze_pcb.py shifted.kicad_pcb --full -o shifted-analysis.json
```

We ran both commands with the same script revision. Each result shows a 40 × 20 mm outline and 10 mm of copper on the `SENSE` net. Under `footprints`, the x coordinate of H2 changes from 85 mm to 84 mm. Compare those coordinates with the [hole-spacing requirement](design-checks.md). [Tested script revision](https://github.com/aklofas/kicad-happy/blob/6b9767e19979cdef91631573753b1547efdbeab9/skills/kicad/scripts/analyze_pcb.py)

We found these projects in the [engineering agents directory](https://github.com/whut09/Awesome-AI-Engineering-Agents) maintained by whut09. Each project links to its own examples, requirements, and license.
