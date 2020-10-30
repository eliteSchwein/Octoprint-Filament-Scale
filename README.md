# OctoPrint Filament Scale

This plugin allows connecting an HX711-based load cell to Octoprint to read out the current weight of the remaining filament.

You will need an HX711 breakout board and a compatible load cell. You can find these bundled together on Ebay/Aliexpress for roughly $8. Any load cell rated for more than 1kg and less than 50kg should work; I used a 5kg load cell with solid results.

See here for instructions on wiring up the load cell: https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/

This plugin assumes you connected the data pin to GPIO20, and the clock pin to GPIO21,but will soon changed to multiple sensor configuration setup.

You will also need the bracket to connect the load cell to your printer: https://www.thingiverse.com/thing:3037926

## Setup

Install manually using this URL:

    https://github.com/eliteSchwein/Octoprint-Filament-Scale/archive/master.zip


## Configuration

Once you have wired up the HX711, it must be calibrated. This is a pretty straightforward process, and all you will need is an object of known weight. Attach the load cell to your printer with the printed bracket, then follow the instructions on the plugin's settings page.

