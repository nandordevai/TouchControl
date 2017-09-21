# Akai MPD218 MIDI Remote Script for Ableton Live

Based on [Selected Track Control for Ableton Live](http://stc.wiffbi.com/)

Note: this is currently a work in progress.

## Features

- works without configuration
- studio and performance modes
    - studio mode maps as many controls as possible for effective work
    - performance mode is simple and safe
- easy to use and learn
- includes presets, PDF document of control mappings for both modes

## Details

This Ableton Live remote script provides two different mappings for the Akai MPD218 MIDI controller. The 'studio mode' can be used for navigating and controlling tracks, devices and for global functions (transport controls, undo/redo, etc.) The 'performance mode' is a simpler mapping for using the controller in a live context (it uses the same actions in all three controller/pad banks).

These mappings are not intended to be an easily customizable, general solution. If you need that, I suggest using [Selected Track Control](http://stc.wiffbi.com/). This is a simple, instantly usable script for producers who don’t want to edit Python scripts.

## Installation and usage

Load the preset files (MPD218 STC Studio.mpd218 and MPD218 STC Performance.mpd218) to your MPD218 controller.

Copy the folder to Ableton Live’s MIDI remote scripts folder. (On macOS it is /Applications/Ableton Live 9 Standard.app/Contents/App-Resources/MIDI Remote Scripts.) Start Ableton Live, open preferences and go to "MIDI Sync" panel. Select 'MPD218 TotalControl' as control surface and configure the MIDI ports accordingly.

The mappings use MIDI channel 1. If you want to use your controller in the default mode (eg. for Drum Racks) then create a preset with another channel.

## Feedback

Please send any feedback to mail@devainandor.com. All comments and ideas are welcome, however I cannot guarantee that I can help you with installation and usage problems. Bugs will be fixed as time permits. New features may be added.

## TODO

- [x] increase sensitivity for track/scene scroll
- [ ] printable overlays
- [ ] ~~use toggle mode for mute/solo/etc. pads~~

## _Framework documentation

<http://julienbayle.net/AbletonLiveRemoteScripts_Docs/_Framework//_Framework-module.html>
