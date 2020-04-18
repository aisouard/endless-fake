# endless-fake

[![Build Status](https://travis-ci.org/aisouard/endless-fake.svg?branch=master)](https://travis-ci.org/aisouard/endless-fake)

Helpers for building and evaluating artificial intelligence agents playing the
Endless Lake video game.

![endless-fake heading](docs/header.png)

## Pre-requisites

* Google Chrome with the [chromedriver] binary
* Python 3.6 (not tested under prior versions yet)

## Installation

```
$ pip install endless-fake
```

Copy the chromedriver binary in your current working directory. It should be
fine if your system can already find it through the PATH environment variable.

## Getting Started

First, let's download a copy of the Endless Lake video game.

```
$ endless-fake fetch ./game
```

Patch the game files to make an offline version.

```
$ endless-fake patch ./game
```

Start recording a gameplay video, in order to become independent of the web
browser. Be careful as the video might become heavy since it will keep
uncompressed frames!

```
$ endless-fake record --output video.avi ./game
```

Run the included scanner, to make sure the video has been well written and our
scanner is working fine.

```
$ endless-fake playback video.avi
```

Get some data by recording your actions corresponding to the inputs.

```
$ endless-fake teach --output data.csv ./game
```

Train the included neural network agent with the previously collected data.

```
$ endless-fake train --output brain.dat data.csv
```

Evaluate the neural network we've just generated.

```
$ endless-fake evaluate --input brain.dat ./game
```

You can also just let your computer learn how to play by itself.

```
$ endless-fake genetics ./game
```

[chromedriver]: https://chromedriver.chromium.org/downloads