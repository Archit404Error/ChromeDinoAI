# ChromeDinoAI
## What it does
This AI automatically generates thousands of Dinosaur players who compete with one another to get the fartherst in the Chrome Dino Game. The players automatically learn and grow over time, until they become artificially intelligent enough to beat the game. The NEAT evolutionary algorithm was used to develop this simulation, along-side pygame for the brick breaker game itself.

## Training the AI
Simply run 
> git clone github.com/Archit404Error/ChromeDinoAI

Once you've successfully cloned the repo, all you have to do is cd into the folder and run the following command:
```python
python3 main.py
```

After that, the simulation will begin to run and train automatically!

Here's an example of what this will look like:

<img src = dinotraining.png>

As can be seen, several dinos begin moving at once. Stats are displayed in the top left of the screen, and each dino must jump over the same set of obstacles(the cacti). Clouds also float in from time to time, but they are simply cosmetic.

## Adjusting the AI
Screen width and height can be found at the beginning of the main.py file and can be manually adjusted. Evolutionary parameters(number of players, number of input/output/hidden layers, etc.) can be found and adjusted in the config-feedforward.txt file.

Additionally, the formula for increasing speed can be modified by changing how and when the global gameMovement is incremented.
