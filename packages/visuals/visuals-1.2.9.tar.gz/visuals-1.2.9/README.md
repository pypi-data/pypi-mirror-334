<h1 align="center">visuals</h1>
<br>
<img alt="Version" src="https://img.shields.io/badge/version-1.2.9-blue.svg" />
<a href="https://pypi.org/project/visuals" target="_blank">
  <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
</a>
<a href="https://pypi.org/project/visuals" target="_blank">
  <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
</a>
<a href="https://pypi.org/project/visuals" target="_blank">
  <img alt="License: Apache-2.0" src="https://img.shields.io/pypi/l/visuals" />
</a>
<a href="https://pypi.org/project/visuals" target="_blank">
  <img alt="Downloads" src="https://static.pepy.tech/personalized-badge/pystyle?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads" />
</a>

> **visuals** is a Python library used for implementing beautiful, colorful styling into your terminal applications.
> <br>It is based on **pystyle**, **pyfade**, **pycenter** and **pybanner**.

## Install

```sh
pip install visuals
```

# Features

  - Colored text ✔️
  - Colored text with a fade effect ✔️
  - Writing effects ✔️
  - Centered text ✔️
  - Adding banners ✔️
  - Make boxes ✔️
  - Hide and show cursor ✔️
  - Change window title ✔️
  - System functions ✔️

<br>

## Colored text
<p><i><strong>Color some text easily.</strong></i></p>
<br>

```python
from visuals import Colors, Colorate
text = "Hello world!"
print(Colors.blue + text)
# or
print(Colorate.Color(Colors.blue, text, True))
```

<br>

`Colors.blue` = color<br>
`text` = text to be colored<br>
`True` = reset color after (otherwise it will continue printing characters in the specified color)

<br>

Available functions are:
  - Color (simply color some text)
  - Error (make an error effect)


<br>

## Colored text with fade effect    
<p><i><strong>Make a fade effect.</strong></i></p>
<br>

```python
from visuals import Colors, Fade
print(Fade.Horizontal(Colors.yellow_to_red, "Hello, Welcome to visuals.", 1))
```

<br>

`Colors.yellow_to_red` = color<br>
`Fade.Vertical` = mode<br>
`1` = intensity (default=1)

<br>

Available effects are:
  - Vertical
  - Horizontal
  - Diagonal
  - DiagonalBackwards

<br>

## Writing text with fade effect

<br>

To print a text using writing and fade effect you can use the `visuals.Write` function.

```python
from visuals import Write, Colors

name = Write.Input("Enter your name -> ", Colors.red_to_purple, interval=0.0025)
Write.Print(f"Nice to meet you, {name}!", Colors.blue_to_green, interval=0.05)
```
<br>


There are 2 functions:<br>


`Write.Print`: prints the text to the terminal with chosen effects<br>
`Write.Input`: same as `Write.Print` but adds an input at the end<br>


<br>


There are 6 arguments:<br>


`text`: the text to be written to the terminal<br>
`color`: the color you want for the text<br>
`interval`: the interval of the writing effect<br>
`hide_cursor`: whether you want the cursor to be hidden or not<br>
`end`: the end color, the default is white<br>
`input_color` (only for `Write.Input`): the color of the input<br>


<br>
<br>


## Center text
<br>
<p><i><strong>Center a text in the terminal.</strong></i></p>

```python
from visuals import Center
print(Center.XCenter("Hello, Welcome to visuals."))
```
<br>
<p>Output:</p>
<br>

```
                                            Hello, Welcome to visuals.                                
```


<br>

Available modes are:
  - Center (Center the banner/text on both axis)
  - XCenter (Center the banner/text on X axis)
  - YCenter (Center the banner/text on Y axis)

<br><br>

## Adding banners
<p><i><strong>Add text to a banner easily.</strong></i></p>

```python
from visuals import Add
banner1 = '''
    .--.
  .'_\/_'.
  '. /\ .'
    "||"
     || /\
  /\ ||//\)
 (/\\||/
____\||/____'''

text = "This is a beautiful banner\nmade with visuals"

print(Add.Add(banner1, text, 4))
```

Output:

```
    .--.
  .'_\/_'.
  '. /\ .'
    "||"    This is a beautiful banner
     || /\  made with visuals
  /\ ||//\)
 (/\||/
____\||/____
```
<br>

`banner1` = first banner<br>
`text` = second banner<br>
`4` = blank lines before adding the smallest banner to the biggest banner (default=0). Set to `True` to center it<br>

## Make boxes
<p><i><strong>Make beautiful boxes easily!</strong></i></p>
<br>

```python
from visuals import Box
print(Box.Lines("Hello, Welcome to visuals."))
print(Box.DoubleCube("Hello, Welcome to visuals."))
```

Output:

```
─══════════════════════════☆☆══════════════════════════─
               Hello, Welcome to visuals.
─══════════════════════════☆☆══════════════════════════─
╔════════════════════════════╗
║ Hello, Welcome to visuals. ║
╚════════════════════════════╝
```

Available modes are:
  - Lines
  - SimpleCube
  - DoubleCube

## Cursor
Show cursor!

```python
from visuals import Cursor

Cursor.ShowCursor()
```

Hide cursor!

```python
from visuals import Cursor

Cursor.HideCursor()
```

## System functions
### Check if the terminal supports colors
```python
from visuals import System

System.Init()
```
### Clear the terminal screen
```python
from visuals import System

System.Clear()
```
### Change the terminal title (Windows-only)
```python
from visuals import System

System.Title("The title")
```
### Change terminal size (Windows-only)

```python
from visuals import System

System.Size(12,12)
```
### Run a shell command
```python
from visuals import System

System.Command("echo hello")
```

<br>
<br>

Contributions, issues and feature requests are welcome!<br />

***
