# FLEM Tool - Framework Light Emitting Matrix Tool
[![Pylint](https://github.com/jwilkins88/flem_tool/actions/workflows/build.yml/badge.svg)](https://github.com/jwilkins88/flem_tool/actions/workflows/build.yml)

<img src="docs/images/logo.jpeg" height="400px" />

##### Disclaimer: This is only somewhat tested, somewhat optimized, and somewhat incomplete. It works on my machine though


## What is FLEM

When I got my LED Matrices from Framework, my head was spinning with the possibilities. As I implemented things that I wanted, I realized that what I really wanted was a utility that could manage all these different pieces that I wanted in a sane way. Managing the layout of the matrices was a bit painful. Having to keep track of what LEDs were lit by what piece was painful, so I started writing a utility that would help manage that.

Enter the FLEM Tool. FLEM Tool is a config based renderer that renders modules (more on that later) for [Framework's LED Matrix panels](https://frame.work/products/16-led-matrix) asynchronously (i.e., each module updates independently). Each module manages its own space, its own content, refresh rate, etc...

I hope you find it as useful as I have!

<img src="docs/images/flem_action.jpg" height="400" />

## Table of Contents
- [Key Features](#key-features)
- [Basic Information](#basic-information)
- [Setup](#setup)
- [Customizing](#customizing)
  - [Config Reference](#config-reference)
  - [Existing Modules](#existing-modules)
  - [Adding Custom Modules (WIP)](#adding-custom-modules-wip)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Key Features

- **Modular, Asynchronous Design**  
  FLEM's architecture allows each module to update independently, ensuring smooth operation and flexible configurations.

- **Scene Management**  
  Display multiple modules in rotating scenes, maximizing the limited matrix real estate. Scenes are fully customizable and support automatic transitions.

- **Prebuilt Modules**  
  Comes with a variety of ready-to-use modules, including:
  - **CPU and GPU Usage**: Minimalist and full modules available, with optional temperature monitoring.
  - **Clock Modules**: Standard digital clock, binary clock, and more.
  - **RAM Usage**: Displays current memory usage.
  - **Weather Module**: Displays real-time weather conditions, temperature, and optional humidity/wind details.
  - **Animator Module**: Supports animated frames or static graphics for custom visuals.

- **Custom Configuration**  
  Easily customize layouts and behavior using a JSON-based config file. Add modules, adjust positions, refresh intervals, and more.

- **Open API Integration**  
  Modules like the Weather Module support external APIs for live data, with configurable endpoints and data mapping.

- **Support for Multi-Device Setup**  
  Manage multiple LED matrices with a single configuration, enabling cohesive displays across devices.

- **Lightweight and Efficient**  
  Designed to run seamlessly on Linux (tested on Linux Mint/Ubuntu), ensuring low resource usage and high performance.

- **Built for Tinkerers**  
  Encourages customization and user-driven development, with a roadmap for features like trigger configs and multi-threading.

### Scene Transition + Animator Module

![alt text](docs/images/action.gif)

## Basic Information

FLEM Tool is a way to easily manage your LED Matrix Panels from Framework. It takes a modular, asynchronous approach to updating and managing the panels. This means that you can have many modules updating on their own schedule, and you only have to worry about what's in your config file. The plan is to ship this with some prebuilt modules and give users the tools they need to build whatever they want.

As of the latest update, Scenes are supported, and this makes the tool even more useful. Scenes automatically rotate through a pre-defined list of modules at a set interval, giving users the ability to show more information on the same screen. Think of it like those obnoxious digital billboards that are everywhere now.

### Modules

Modules are the core of FLEM. Each module is self-contained, and is only concerned about rendering its own information to the matrix. Each module runs in isolation, and isn't affected by other modules that are also running (well, sort of... more on that in [limitations](#limitations)).

Currently, I have:

- CPU
  - [Minimalist CPU Module](#cpu-module)
  - [Full CPU Module (includes CPU temp)](#horizontal-cpu-module)
- GPU***
  - [Minimalist GPU Module](#gpu-module)
  - [Full GPU Module (include GPU temp)](#horizontal-gpu-module)
- Clocks
  - [Clock Module](#clock-module)
  - [Binary Clock Module](#binary-clock-module)
- [RAM Module](#ram-module)
- [Battery Module](#battery-module)
- [Weather Module](#weather-module)
- [Animator Module](#animator-module)
- [Line Module (more of a building block)](#line-module)

*** The GPU module **will not** work out of the box. It requires a custom built version of NVTOP (can be found on my github). I'm hoping that my changes will make it to the stable version of NVTOP, but, for now, there's a bit of monkeying required to get the GPU modules working. See [the GPU module](#gpu-module) section for more information

### Scenes

Scenes add power to FLEM. Scenes are exactly what they sound like. It's the ability to have a rotating selection of modules display on your matrix(s). Scenes show for a preset amount of time before loading the next set of modules and refreshing the display. Right now, the scene transition is a bit clunky and jarring, but I have plans of adding animated scene changes in the future. 

Scenes are set up independently from modules. What that means is that you define your modules (per matrix), and then scenes just reference the module configuration by name. This way, you don't have to set up the same module multiple times if its reused across scenes (i.e., always show clock module, but rotate GPU/CPU).

Scenes provides the foundation work for [trigger configs](#add-trigger-configs--in-progress). I'm excited to get to that one, but I'm working out all the basics and fundamentals before I start trying to get fancy.

## Setup

This is still a work in progress. The end goal is to have this be a package that you can install with either pip or a package manager on your favorite OS. For now, you're going to have to clone the repo and run it manually. When you clone the repository, it won't just fire up. without installing a couple dependencies.

### Before you get started

This is untested on anything except my system with my environment. Eventually, I'll add more robust testing, but I'm not going to bother with that until I feel like I'm in a pretty good place with the tool (or people start wanting to use it)

**Python versions**: 
- 3.13
- 3.12
- 3.11
- 3.10
- 3.9

If you want to check your Python version, just type `python --version` in your terminal. I have done rudimentary testing Python versions 3.9+. I haven't gotten around to doing thorough testing in anything but 3.13. Your mileage may vary

### Installing

```bash
pip install flem-tool
```

### Running Flem

FLEM comes with a default layout that's very, very basic. If you want to customize it, you'll have to create your own config. The default config is buried in the python directory, and I don't recommend messing around in there too much. See [Customizing](#customizing) for more details on how you can configure flem

```bash
flem
```

Once that's done, your terminal should be spitting out logs, and you should see things happening on your matrix(s)!

## Customizing

### Config Location

FLEM creates a config file at `~/.flem/config.json` on its first run. If this ever gets deleted, it'll create it again with the default config

### Config Reference

Simple Config. This is a pretty bare bones example of a config that will show the CPU module in the top left corner of the matrix. As of now, we have to add at least one scene. Scenes are what really unlock the power and flexibility of FLEM, but more on that later

```json
{
  "devices": [
    {
      "name": "left",
      "device_address": "/dev/ttyACM1",
      "speed": 115200,
      "brightness": 3,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "cpu",
          "module_type": "CpuHModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000
        }
      ],
      "scenes": [
        {
          "name": "Scene 1",
          "show_for": 0,
          "scene_order": 0,
          "modules": [
            "cpu"
          ]
        }
      ]
    }
  ]
}
```

Here's the full structure of the config and all the allowed properties

```json
{
  // An array of devices
  "devices": [
    {
      //Just a string. Any value is fine here
      "name": "left",

      /**
      This value does matter. Please refer to Framework's documentation
      for what this should be.

      For Linux, this is usually "/dev/ttyACM0" or "/dev/ttyACM1"

      For Windows, ????
      **/
      "device_address": "/dev/ttyACM1",

      // This is the baud rate for the device. The default is 115200
      "speed": 115200,

      /**
      This is a value between 0 and 255. 255 is extremely bright.

      I usually run mine between 3 and 10
      **/
      "brightness": 10,

      /**
      The following two fields probably aren't necessary, but I figure
      it can't hurt.

      I'll probably make these optional at some point, and add a "device_type"
      field that will inform what these values should be
      **/
      "on_bytes": 1,
      "off_bytes": 0,

      /**
      This is an array of the modules that we want to load.
      This is where the magic happens. These modules are defined once per device
      and then referenced in the scenes. This way, we don't have to duplicate 
      modules if we have multiple scenes with the same module.
      (i.e., we want to show clock and CPU in scene 1 and Clock and GPU in Scene 2)
      **/
      "modules": [
        {
          /**
          The name is how the scenes will reference the module. This way, we can 
          have multiple of the same module, but referenced differently in scenes.
          (i.e., When I implement trigger configs, we might want to define two CPU
          Modules, but have them displayed at different coordinates)
          **/
          "name": "my_module_1",

          /**
          Module Type has a list of values. Refer to the "Existing Modules"
          section for a rundown on what their values are as well as a list
          of options for the modules.

          This will break if it doesn't match the module
          **/
          "module_type": "MyModule",

          /**
          This is an object that defines the physical location (start column, start row)
          of the module on the display. It is important to note that most of
          my stock modules have a required width and height. I suspect that most
          modules will probably have the same requirement.

          This is important to get right because it will crash the tool (for now) if
          a module gets too big for its britches
          **/
          "position": {
            // Valid values: 0-8
            "x": 0,

            // Value values: 0-33
            "y": 0
          },

          /**
          Refresh interval defines how often the module will update its value (in ms).

          I haven't done a lot of testing around how frequently these updates
          can happen before things start breaking, but just try to keep this sane

          As an example, there's not really much of a reason the clock needs to
          update more than once a second.

          When you're dealing with threading in Python, we really only have one thread,
          so, if we have 6 modules updating every 1 ms, this is probably going to
          result in havoc for everything. Feel free to experiment with this, but I
          may end up introducing a lower limit for this value as I test things

          A sane default for this is 1000
          **/
          "refresh_interval": 1000,

          /**
          This is a freeform object. As I was developing modules, I realized that we're
          going to have some modules that need a little bit more configurability than
          others. I didn't want to make specific module configs for every module, but
          I did want to provide flexibility. For the values that the individual module
          requires, see the module's documentation. The values below are just examples
          **/
          "arguments": {
            "clock_timezone": "CDT",
            "file_path": "~/my_file.txt"
            // etc...
          }
        }
      ],
      /**
      Scenes is how we can display a ton of information on a small display. Scenes are
      simply a collection of modules that rotate on an interval. I haven't tested an 
      upper limit on the number of scenes, but theoretically, you can have as many as you
      want
      **/
      "scenes": [
        {
          /**
          This doesn't have any special functionality around it. This can really be whatever
          you want, but it'll be easier to troubleshoot if all the scene names are unique. It
          could be anything: "Clock+GPU", "Clock+Weather", "Clock+CPU+GPU". This really only
          shows up in the logs
          **/
          "name": "Scene 1",

          /**
          How long this scene shows before changing (in ms). This can be different for every 
          scene or the same. It's really up to you on how you want the info to display

          NOTE: 0 means that the scene never changes
          **/
          "show_for": 20000,

          /**
          Not currently implemented, but it will be very soon. This was added as more of a 
          convenience than anything else. Rather than having to futz with reordering the json
          array, you can set the order, and it will be reflected
          **/
          "scene_order": 0,

          /**
            This array determines what modules will show in this scene.

            IMPORTANT!!! These values **MUST** match the name of a module defined in the 
            modules section above. If it doesn't, it will error
          **/
          "modules": [
            "my_module_1"
          ]
        }
      ]
    }
  ]
}
```

### Existing Modules

#### CPU Module

My first creation! This module simply displays the current CPU usage. As of this writing, I'm using [psutil](https://github.com/giampaolo/psutil)

**Module Type**: CpuModule

**Dimensions (width x height)**: 3x18

**Custom Arguments**: N/A

**Sample Module Config**

```json
{
  "module_type": "CpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000
}
```

Example:

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Horizontal CPU Module

Reading top to bottom is hard for those of us who are used to reading left to right. I initially created the CPU module thinking about how I could display the most information in the smallest space, but, variety is the spice of life. For when maximalism is the order of the day, consider the horizontal CPU module. It's capable of displaying both the utilization and temperature, and it's a bit easier on the eyes.

Top number shows utilization. Bottom shows temperature (celsius only for now)

This, once again, utilizes [psutil](https://github.com/giampaolo/psutil). This time, I'm using a function that only works on linux ([per the documentation](https://psutil.readthedocs.io/en/latest/#sensors)). If you're on Windows, well, I don't know that any of this will work for you.

**Module Type**: CpuHModule

**Dimensions (width x height)**: 9x12 (without temperature); 9x19 (with temperature)

**Custom Arguments**:

| Argument     | Type                                                            | Description                                                                                                                                                                      |
| :----------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show_temp`      | true                                                         | Whether we're going to show the temperature or not. If this is set to true, `temp_sensor` and `temp_sensor_index` are required |
| `temp_sensor` | string | **If `show_temp` is true, this is required**. There's a few ways you can find your sensor name. One of the easiest is to install lm-sensors and find you sensor in the list. It's not always obvious. For my AMD processor it's `k10temp`                                                       |
| `temp_sensor_index` | int | **If `show_temp` is true, this is required** For my AMD processor, I have one sensor. When you have more than one sensor, you'll need to specify which one you want to see. Most the time, this is individual core temperature |
| `use_bar_graph` | bool | Show the CPU utilization (and, optionally, temp) as a bar graph. Slightly more compact. It uses a 2x9 grid that lights up sequentially. For both temp and utilization, I'm setting a max of 100. For now, that's hardcoded as it seems reasonable. I may make that value adjustable in case you're targeting specific temps and want to keep track of a specific threshold.<br><br>It looks pretty cool. Thanks to [Kitsunebi](https://community.frame.work/u/kitsunebi/summary) from the Framework community for the idea! |

**Sample Module Config**

```json
{
    "module_type": "CpuHModule",
    "position": {
        "x": 0,
        "y": 14
    },
    "refresh_interval": 1000,
    "arguments": {
        "show_temp": true,
        "temp_sensor": "k10temp",
        "temp_sensor_index": 0,
        "use_bar_graph": true
    }
}
```

**"use_bar_graph": false**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

**"use_bar_graph": true**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### GPU Module

This command is a little bit more complex because it relies on an OS utility to get the GPU utilization. This is currently only tested on Linux Mint (should work fine on Ubuntu as well). I haven't tested this on Windows or any other Linux flavor. The theory is that it should work. The tool that I'm using to get the GPU info is called [NVTOP](https://github.com/Syllo/nvtop). It's a super neat utility that works with both AMD and NVIDIA (and a whole lot of other stuff). Can't say enough good things about it.

To make things even more complicated, this uses a custom version that I modified to suit my needs. I have a [PR open to get those changes into the main version](https://github.com/Syllo/nvtop/pull/358), but until that's merged and published, you're going to need to build your own version of this utility from [my fork](https://github.com/jwilkins88/nvtop/tree/master). The build instructions are really good, and I promise it's not too hard.

**Module Type**: GpuModule

**Dimensions (width x height)**: 3x18

**Custom Arguments**:

| Argument                   | Type                           | Description                                                                                                                                                                                                                                                                                                                                                      |
| :------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpu_index`                | integer                        | In the case that you have multiple GPUs (iGPU and discrete GPU), you need to select your index. `0` Is a pretty safe bet for most use cases, but check the output of your command of choice (no reason this _has_ to be nvtop)                                                                                                                                   |
| `gpu_command`              | string                         | This is the command to run to get the GPU info. In my case, this is `/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop`. Again, this can be whatever you want it to be so long as it outputs json                                                                                                                                                                       |
| `gpu_command_arguments`    | array[string] | If you need to specify arguments for your command, this is how you'll need to do it                                                                                                                        |
| `gpu_util_output_property` | string                         | This is the property that we're going to read from the JSON. Keep in mind that, as of now, I don't have any validation around this. I'll add that as a part of [improving error handling](#improved-error-handling), but, for now, this is fairly brittle. It can only handle digits, and I don't do any sanitization. My value for this is typically `gpu_util` |

**Sample Module Config**

```json
{
  "module_type": "GpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "gpu_index": 0,
    "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
    "gpu_command_arguments": "-s",
    "gpu_util_output_property": "gpu_util"
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Horizontal GPU Module

Just like the [Horizontal CPU Module](#horizontal-cpu-module), this module can show temp and utilization in a left-to-right fashion. Other than that, it's exactly the same as the [GPU module](#gpu-module). All the same things apply. It's still using my custom version of [NVTOP](https://github.com/Syllo/nvtop), and you'll need that if you want to use it. The nice thing about NVTOP is that it gives me all the information I want in one go, so I don't need to worry about making multiple calls to get the utilization and then the temperature. 

**Module Type**: GpuHModule

**Dimensions (width x height)**: 9x12 (without temperature); 9x19 (with temperature)

**Custom Arguments**:

| Argument                   | Type                           | Description                                                                                                                                                                                                                                                                                                                                                      |
| :------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpu_index`                | integer                        | In the case that you have multiple GPUs (iGPU and discrete GPU), you need to select your index. `0` Is a pretty safe bet for most use cases, but check the output of your command of choice (no reason this _has_ to be nvtop)                                                                                                                                   |
| `gpu_command`              | string                         | This is the command to run to get the GPU info. In my case, this is `/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop`. Again, this can be whatever you want it to be so long as it outputs json                                                                                                                                                                       |
| `gpu_command_arguments`    | array[string] | If you need to specify arguments for your command, this is how you'll need to do it                                                                                                               |
| `gpu_util_output_property` | string                         | This is the property that we're going to read from the JSON. Keep in mind that, as of now, I don't have any validation around this. I'll add that as a part of [improving error handling](#improved-error-handling), but, for now, this is fairly brittle. It can only handle digits, and I don't do any sanitization. My value for this is typically `gpu_util` |
| `show_temp` | bool | Unlike the cpu temp module, this one doesn't require any extra config. Set this to true, and you can see your GPU temperature live. It's handy dandy |
| `use_bar_graph` | bool | Show the GPU utilization (and, optionally, temp) as a bar graph. Slightly more compact. It uses a 2x9 grid that lights up sequentially. For both temp and utilization, I'm setting a max of 100. For now, that's hardcoded as it seems reasonable. I may make that value adjustable in case you're targeting specific temps and want to keep track of a specific threshold.<br><br>It looks pretty cool. Thanks to [Kitsunebi](https://community.frame.work/u/kitsunebi/summary) from the Framework community for the idea! |

**Sample Module Config**

```json
{
  "module_type": "GpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "gpu_index": 1,
    "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
    "gpu_command_arguments": "-s",
    "gpu_util_output_property": "gpu_util",
    "show_temp": true
  }
}
```

**"use_bar_graph": false**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

**"use_bar_graph": true**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Line Module

This is most useful as a "sub-module". I use it in both the [CPU Module](#cpu-module) and the [GPU Module](#gpu-module), but it also has more uses. Currently, this is my only "static" module (i.e., it doesn't run a thread, and it never updates - unless there's a config update). Currently only supports horizontal lines.

**Module Type**: LineModule

**Dimensions (width x height)**: \[width\]x1

**Custom Arguments**:

| Argument     | Type                                                            | Description                                                                                                                                                                      |
| :----------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `width`      | integer                                                         | Specifies how many pixels the line will span. I have no validation around this, but I will plan on adding some as a part of [improving error handling](#improved-error-handling) |
| `line_style` | string<br>Allowed values: `solid`, `dashed`<br>Default: `solid` | Specifies whether the line is solid or separate by one pixel set to off. Very naive implementation and needs to be improved                                                      |

**Sample Module Config**

```json
{
  "module_type": "LineModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "line_style": "dashed",
    "width": 9
  }
},
{
  "module_type": "LineModule",
  "position": {
    "x": 0,
    "y": 2
  },
  "refresh_interval": 1000,
  "arguments": {
    "line_style": "solid",
    "width": 9
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛  DASHED
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛  SOLID
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Clock Module

This is a simple clock module that shows the current system time. Why use a module when you have a clock on your computer? Because it's dope. There's no other reason you need. Optionally, displays an indicator showing the progression of seconds until the next minute (think of it like a seconds hand, but with far less precision). The seconds indicator blinks, giving another indicator of seconds passing. One full cycle of blinks (blink on, blink off) represents 2 seconds. I might add support for custom timezones.

**Module Type**: ClockModule

**Dimensions (width x height)**: 9x11

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `clock_mode`             | string<br>Allowed values: `12h`, `24h`<br>Default: `12h` | Specifies whether you want to show 12 hour time, or 24 hour time (i.e., 03:30 vs 15:30)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `show_seconds_indicator` | boolean                                                  | Display the seconds indicator. This is a little bit complicated, but I realized that, with the style I have for the clock, I'd always have 10 pixels to spare (5 to the right of the hours, 5 to the left of the minutes). In order to capitalize on that space, I came up with a way to show the progression through the minute, but at a lower precision than we're typically used to. This also blinks. I might add an option to disable the blink if people think it's annoying, but I think it's cool |

**Sample Module Config**

```json
{
  "module_type": "ClockModule",
  "position": {
    "x": 0,
    "y": 1
  },
  "refresh_interval": 1000,
  "arguments": {
    "clock_mode": "24h",
    "show_seconds_indicator": true
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Binary Clock Module

Another cool idea from [Kitsunebi](https://community.frame.work/u/kitsunebi/summary). Based off the KDE Plasma binary clock, this tracks time using the magic of binary! For users who are comfortable reading binary, this module saves a lot of precious real estate. It also just looks super cool. It's really lively with the seconds column constantly changing, so it'a a really neat module to have on your display. The one thing that doesn't work great is that it's 6 pixels wide, and our display is 9 pixels wide. That means that it can't be centered. Not a big deal, though, and maybe I'll come up with some sort of a companion for it to fill in the 3 pixel gap. I'll think on it.

In a binary clock, each row represents a bit (on/off). In order to read the column value, you transpose the digits into a standard binary string. From my example below:

```
8️⃣⚪
4️⃣⚫
2️⃣⚫
1️⃣⚫
```

Would be transposed as:

```
⚪⚫⚫⚫ = 1000
```

Which equals 8. If we do that for the rest of the grid below,

```
8️⃣⚫ ⚪ ⚫ ⚫ ⚫ ⚪
4️⃣⚫ ⚫ ⚫ ⚪ ⚫ ⚫
2️⃣⚫ ⚫ ⚫ ⚪ ⚫ ⚫
1️⃣⚪ ⚪ ⚪ ⚫ ⚪ ⚫
```

We get `19:16:18` as the current time

Pretty cool stuff. Try it out!

**Module Type**: BinaryClockModule

**Dimensions (width x height)**: 6x4

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `clock_mode`             | string<br>Allowed values: `12h`, `24h`<br>Default: `12h` | Specifies whether you want to show 12 hour time, or 24 hour time (i.e., 03:30 vs 15:30)                                                                                                                                                                                                                                                                                                                                                                                                                    |
```json
{
  "name": "binary_clock",
  "module_type": "BinaryClockModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "clock_mode": "24h"
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### RAM Module

Shows current RAM usage. Once again, this uses psutil. Should work on Windows, but I'm not going to be testing on Windows for a little while. This currently only shows RAM usage rounded to the nearest gigabyte. I did add an indicator (similar to the [clock module](#clock-module)) that shows little pips for each 1/9th of a gigabyte. In the sample output below, I'm using ~9.1GB of RAM.

**Module Type**: RamModule

**Dimensions (width x height)**: 9x11

**Custom Arguments**: N/A

**Sample Module Config**

```json
{
  "name": "ram",
  "module_type": "RamModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Animator Module

This one is big. I can see this being the bread and butter of most setups. Allows arbitrary "animations" through config. It can also display static drawings if you only have one frame and set the frame duration to 0. The frame duration overrides the module level `refresh_interval`. For this specific type of module, the refresh interval is irrelevant, but for now it'll need to be set to some arbitrary value. I'll fix that in the future

See examples animations that I've made (poorly) in the [weather animation directory](src/flem/animator_files/)

**Module Type**: AnimatorModule

**Dimensions (width x height)**: *no set size. specify in config*

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frames`             | array[Frame]  | This is what sets all the individual frames for the module. I'll define the frames object below |
| `width` | int | Necessary to let the module know how many columns it will span |
| `height` | int | Necessary to let the module know how many rows it will span |
| `animation_file` | string | This can be a path to anywhere on your system, but it has to be an absolute path (for now). I.E., `/home/blah/.flem/animator_files/my_animation/animation.json`. I recommend sticking this in flem's home directory just so they're all in the same place. I provide this because animations can get lengthy and bloat your config. See examples in the [animator_files directory](src/flem/animator_files/) |

<br>

**Frame Object**

| Property                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frame` | array[array[int]] | This defines a single frame for the animation. If there's only one animation, it'll just be a static drawing
| `frame_duration` | int | This is how long the frame should display (in milliseconds). If this is set to 0, it is considered a static frame, and no frame changes will happen. |

**Full Module Config**

```json
{
  "name": "animator",
  "module_type": "AnimatorModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "frames": [
      {
          "frame": [
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0 ,0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
          ],
          "frame_duration": 1000
      },
      {
          "frame": [
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1 ,0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0]
          ],
          "frame_duration": 1000
      }
    ],
    "width": 9,
    "height": 6
  }
}
```

**File Module Config**

```json
{
  "name": "animator",
  "module_type": "AnimatorModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "animation_file": "/home/myuser/.flem/animator_files/weather/fog.json",
    "width": 9,
    "height": 6
  }
}
```

```
FRAME 1

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

FRAME 2

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

```

#### Weather Module

The weather module is one of the more complex modules that I've built to date. It's mostly complicated because it relies on something other than easily obtained system data. I've set it up so that it can *theoretically* use most APIs that return the weather with a simple `get` request, but I recommend setting it up with `OpenWeatherMap`, since that's what I've done my testing with. If you'd like to use a different service, reach out, and I'll see what I can do to make it happen.

In its most basic form, the weather module shows the current conditions (via an animated header) and the temperature (you choose between `imperial`, `standard`, or `metric`). It has an option to show the humidity as well as an option to show wind speed and direction.

This is a **BIG** module. Big as in, it'll take up a lot of the panel. I highly recommend swapping this one in via scenes or not enabling all the stats and just using the temperature if you're concerned about real estate.

Because this makes an external API call, I wanted to keep performance in mind and I'm using a cached file in the `~/.flem` directory. The module will make one API call every 10 minutes to update the cache file, and the module will load the results from that file when it refreshes. I'm considering making an option to have that update parameterized, but, for now, it's set statically at 10 minutes.

I'll make some instructions for how to set up your API key in a future update, but it's a pretty straight forward process. In brief:

1. Head to https://openweathermap.org/
2. Sign up for an account
3. Go to your user profile and find `My API Keys`
4. Generate a new key
5. Stick it in the config
6. Find your city id by searching for your city and copying it from the URL
   1. example: `https://openweathermap.org/city/4997787` - Copy 4997787

For the URL string, it's important that you note that there are some key placeholders that have to be there (especially if you're trying some service other than `openweathermap`). Those are:

1. `{city_id}` - This is just a string, so if your service goes by string rather than an integer id, that should be fine
2. `{api_key}` - This is obviously your api key. Very important
3. `{temperature_unit}` - This is probably the most optional, but for now it's still required or my code will break

If you want to use this and make it as simple as possible, copy the example config below and pop your API key in. It'll work right out of the box.


**Module Type**: WeatherModule

**Dimensions (width x height)**: 

* Just temperature
  * 9x14
* With Humidity or Wind Speed
  * 9x22
* With all
  * 9x30

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api_url`             | string  | The API endpoint to make the request to. For now, I recommend sticking with what I know will work, and that value is: `"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&cnt=5&units={temperature_unit}"` |
| `api_key` | string | This is the api key that you'll create for your service. Absolutely required |
| `city_id` | string | For openweathermap, this is an integer, but I'm using a string to make this as compatible as possible with other services that folks may want to use |
| `response_temperature_property` | string | This is a json selector. If you're using `openweathermap`, this will be `main.temp`. If you're using anything else, you'll have to inspect the response object and set accordingly |
| `response_icon_property` | string | This is a json selector. If you're using `openweathermap`, this will be `weather.[0].main`. If you're using anything else, you'll have to inspect the response object and set accordingly. This is the current condition. I support all of the statuses [specified by OpenWeatherMap](https://openweathermap.org/weather-conditions). I don't support the sub-conditions right now, just the main groups |
| `show_wind_speed` | bool | Whether or not to show the wind speed information along with the weather. If this is specified, **you must** also specify `response_wind_direction_property` and `response_wind_speed_property` |
| `response_wind_speed_property` | string | This is a json selector. If you're using `openweathermap`, the value will be `wind.speed`. If you're using anything else, you'll have to inspect the json response and adjust accordingly |
| `response_wind_direction_property` | string | This is a json selector. If you're using `openweathermap`, the value will be `wind.deg`. If you're using anything else, you'll have to inspect the json response and adjust accordingly. <br>**NOTE**: The module code is expecting this to be in degrees (i.e., 0 degrees == North). If your API returns cardinal directions, **it will not work** |
| `show_humidity`| bool | Shows the humidity in percent. If this is set to `true`, **you must** also specify `response_humidity_property`
| `response_humidity_property` | string | This is a json selector. If you're using `openweathermap`, this will be `main.humidity`. If you're using anything else, you'll have to inspect the json response and adjust accordingly.

**Sample Module Config**

```json
{
  "name": "weather",
  "module_type": "WeatherModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 10000,
  "arguments": {
    "api_url": "https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&cnt=5&units={temperature_unit}",
    "api_key": "<my api key>",
    "city_id": "4997787",
    "show_wind_speed": true,
    "show_humidity": true,
    "temperature_unit": "imperial",
    "response_temperature_property": "main.temp",
    "response_icon_property": "weather.0.main",
    "response_wind_speed_property": "wind.speed",
    "response_wind_direction_property": "wind.deg",
    "response_humidity_property": "main.humidity"
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛  ANIMATED CONDITION INDICATOR
⬛ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛  TEMPERATURE
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛  HUMIDITY
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛  WIND SPEED
⬛ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⬛  WIND DIRECTION INDICATOR (showing southwest here) 
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

#### Battery Module

The battery module is a compact display that can show just the battery icon or, optionally, the numeric percentage. This module uses `psutil` to retrieve the battery information. The battery module has a few different states:

**Unplugged**

In this state, the current percentage "pip" blinks on and off to indicate a discharge state

**Plugged in**

In this state, an animation shows the battery filling from the current percentage "pip" to full. It follows the same sequence as all the other bars that I've implemented with pips. After the full battery animation finished, it resets to the current charge for 2 seconds

**Critical**

This is set to show when the battery reaches a minimum (configurable) threshold. In this state, all the battery pips will blink

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show_percentage`             | bool  | Whether or not the numeric percentage shows below the battery icon |
| `critical_threshold` | int | The battery percentage where the pips start blinking to indicate it's time to charge your laptop |


**Battery Module Config**

```json
{
  "name": "battery",
  "module_type": "BatteryModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "show_percentage": true,
    "critical_threshold": 20
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

### Adding Custom Modules (WIP)

Currently, I don't have a way for you to do this locally, so you'll have to clone this repo and work inside of it. Eventually, I want to be able to have you plug in modules that aren't a part of this tool itself. I'd recommend starting with the line module as a template and build out from there.

There's no real gotchas at this point except that it's just a bit whacky working with a 9x34 display. Math is hard. Most my bugs have been because I suck at math.

## Limitations

This is largely untested. I've only tested it on Linux Mint. Eventually I'll get around to testing it on Windows and other distros, but for now, I can only guarantee it'll work on what's running on my laptop. Ubuntu should be fine, but if you're on any other distro, I can't guarantee anything. I'm working toward it though!

### About Modules

The dream and hope for this is that we can run completely sandboxed modules that have no impact on any other modules. This is partially true in FLEM's current state. While modules don't care about anything but doing their job, it is possible that modules can collide and render on top of each other. It's fully on the end user right now to make sure this doesn't happen. I'm planning on putting in guard rails and true sandboxing for modules in a future update, but it's just not there right now. I'm focused on core functionality (with some fun stuff), and then I'll go back and get around to hardening the application

## Roadmap

In no specific order, here's a list of things that I'm still working on getting to

#### Modify LED matrix firmware to allow for atomic "pixel" updates

Currently, the firmware only allows you to write an entire matrix at once. This works fine, but I'd prefer to have fewer shared resources between the modules. As your number of modules increases, so, too, does contention between threads for updates. The ideal end state is to have each module (and its thread) completely decoupled from the state of the matrix. As far as each module is concerned, it's living in its own sandbox

This would be a bit of an overhaul for all the existing code, and, when (if) this happens, I'll make sure I bake in backward compatibility and feature detection so this doesn't stop working if your matrix doesn't have the custom firmware. Backward compatibility is essential

#### Create a C# version of FLEM

This is mostly because I'm a Microsoft fan boy. I'm a .NET developer by day, and C# will always be my first love. But also:

Managing threads in Python is gross. I want true multi-threading for all sorts of reasons. The overhead will be lower in a compiled language, and I'll have a lot more flexibility in how I manage and prioritize the threads.

When (if) this happens, I will try to maintain feature parity between the two versions (python and C#). I'm also thinking about making a core functions library in C++ so that I can make most my updates in one place. I'm not a C++ developer, so that will be a long way down the road. My goal is to keep this light and fairly unopinionated, so there shouldn't be too much in the "core" functionality anyway

#### Add "trigger configs" * In Progress!

I'm not great at naming things, but, essentially, I want to add the ability to change the display dynamically in response to system changes. Examples:

- Dim or brighten LEDs in response to power saving mode or screen brightness changing
- When you start a game, change the clock module to a FPS module

I don't know how feasible this is, and I think it'll be very OS specific when I get here

~~As a part of this, I also want to add "rotating" layouts. Since our real estate is so small, we can't fit a lot of information onto the matrix. For things like the horizontal cpu module, it takes up over half the matrix. To get around this, I might "rotate" the modules on an interval. As an example, every 10 seconds, I swap the horizontal CPU module for network information, or you swap the clock for weather. That continues in a constant cycle, displaying as many rotating modules as you want.~~

~~Maybe every minute, you swap in an animation that lasts for 5 seconds before rotating back through the information. It gives you a lot of power and flexibility to display more information with the limited real estate~~

#### More modules * In Progress

I want to keep this light, but there's a few more modules that I want to figure out:

1. ~~RAM Module~~ Done!
2. ~~CPU Temp Module~~ Done! (kinda) - I still want to find a minimalist way to display temp in the vertical cpu module
3. ~~GPU Temp Module~~ Done! (kinda) - Same as the CPU Temp
4. ~~Weather Module~~ Done!
5. Battery Module
6. ~~Binary Clock~~
7. ~~CPU Bar~~ Done!
8. ~~GPU Bar~~ Done!
9. RAM Bar

For the GPU and CPU temp modules, I'm trying to think of a way that I can bake that into the existing module, but space is extremely limited. ~~I might end up making "combo" modules that are essentially double wide. If you have two matrices, you can then display the double wide CPU Module on one matrix and the double wide GPU Module on the other~~ I've made some double wide modules. That said, I'm trying to come up with minimalist ways to display information (see the seconds indicator on the clock module) where possible, so stay tuned. I'll probably also end up making stand alone and minimalist versions of most of the modules as time allows. I want to have a fairly robust library of modules that ships with the framework, but I'm focused on things that I want for the time being. If you want something custom, feel free to reach out, and I'll try my best to make it happen (or, [make it yourself](#adding-custom-modules-wip))

#### Mega Matrix

Again, I'm bad at naming things, but I've had the idea that if I could join both my matrices (currently one on the left and one on the right) into a single screen, I'd have so much more room for activities. With the current architecture, this just isn't possible. It's something I definitely want to consider at some point though (reading text top to bottom just isn't great). This might be more of a gimmick, but it's something I want to look into

#### Add a test suite

I don't like writing tests, so this will probably hang out for a while until I know more people are using it. For now, I'm moving fast and breaking things, and it'll probably stay that way for a little while

#### ~~Improved error handling~~ - Mostly done!

Right now, it's very easy to break this. It's a bit brittle. As an example, each of the modules is naive and assumes that it will always have exactly the width and height that it needs in order to render. That would be incorrect. There's nothing stopping a module from trying to render itself off the matrix. This creates an error, and it'll crash the module.

This is just one of the many examples of a way that you could break this on accident. I want add some more robust checking and error handling to the tool in order to make it a bit more user friendly. Apple isn't successful because they make the best stuff. They're successful because their stuff is hard to break.

#### ~~Improved logging/debugging~~ * Done!

~~Right now, I don't have much in the way of logging. I'm not a Python guy typically, so I don't even know what the standards are around logging. I definitely want to add some better logging in for debugging issues. Once this is out into the wild, it's going to be very difficult to troubleshoot in its current state~~

#### ~~Convert into PIP Package~~ Done!

~~This makes it easier for people to use~~

## Contributing

I'd love to see the community excited about this project and wanting to make it better. If you've got something to add (or just want to make it your own), please do! I'm open to feature requests, but even better than that, I'd love to see your ideas in the form of a PR.

I don't really have any guidelines right now, but if you want to build something on top of this, I'd love to see it. If you have a module you want to contribute, please see my [guide on making modules](#adding-custom-modules-wip).

If you make something, I'd love to give you a shout out. If you want to make your own module (but don't want to contribute it back to the tool), I'll happily add a link and a gallery showing off your awesome work.

## My current configuration

```
            LEFT                                        RIGHT
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛           ⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛           ⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛           ⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

```json
{
  "devices": [
    {
      "name": "left",
      "device_address": "/dev/ttyACM1",
      "speed": 115200,
      "brightness": 100,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "cpu",
          "module_type": "CpuHModule",
          "position": {
            "x": 0,
            "y": 12
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "temp_sensor": "k10temp",
            "temp_sensor_index": 0,
            "use_bar_graph": true
          }
        },
        {
          "name": "clock",
          "module_type": "ClockModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000,
          "arguments": {
            "clock_mode": "24h",
            "show_seconds_indicator": true
          }
        },
        {
          "name": "weather",
          "module_type": "WeatherModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 10000,
          "arguments": {
            "api_url": "https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&cnt=5&units={temperature_unit}",
            "api_key": "api_key",
            "city_id": "123467",
            "show_wind_speed": true,
            "show_humidity": true,
            "temperature_unit": "imperial",
            "response_temperature_property": "main.temp",
            "response_icon_property": "weather.0.main",
            "response_wind_speed_property": "wind.speed",
            "response_wind_direction_property": "wind.deg",
            "response_humidity_property": "main.humidity"
          }
        }
      ],
      "scenes": [
        {
          "name": "scene 1",
          "show_for": 10000,
          "scene_order": 0,
          "modules": [
            "clock",
            "cpu"
          ]
        },
        {
          "name": "scene 2",
          "show_for": 10000,
          "scene_order": 1,
          "modules": [
            "weather"
          ]
        }
      ]
    },
    {
      "name": "right",
      "device_address": "/dev/ttyACM0",
      "speed": 115200,
      "brightness": 100,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "gpu_0",
          "module_type": "GpuHModule",
          "position": {
            "x": 0,
            "y": 11
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "gpu_index": 0,
            "gpu_command": "/home/xxxxx/nvtop-dev/usr/local/bin/nvtop",
            "gpu_command_arguments": [
              "-s"
            ],
            "gpu_util_property": "gpu_util",
            "gpu_temp_property": "temp",
            "use_bar_graph": true
          }
        },
        {
          "name": "gpu_1",
          "module_type": "GpuHModule",
          "position": {
            "x": 0,
            "y": 11
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "gpu_index": 1,
            "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
            "gpu_command_arguments": [
              "-s"
            ],
            "gpu_util_property": "gpu_util",
            "gpu_temp_property": "temp",
            "use_bar_graph": true
          }
        },
        {
          "name": "ram",
          "module_type": "RamModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000
        }
      ],
      "scenes": [
        {
          "name": "scene 1",
          "show_for": 10000,
          "scene_order": 0,
          "modules": [
            "gpu_0",
            "ram"
          ]
        },
        {
          "name": "scene 2",
          "show_for": 10000,
          "scene_order": 1,
          "modules": [
            "gpu_1",
            "ram"
          ]
        }
      ]
    }
  ]
}
```