"""
Mostly a python translation of this implementation: https://rtouti.github.io/graphics/perlin-noise-algorithm
"""

import math
from random import Random

from fastn.utilities import *

class PerlinNoise:
    
    # ================== METHODS ==================

    # ────────────────── INITS ──────────────────

    def __init__(self, seed: int, wrapSize: int = 256) -> None:
        """
        PARAMS:
            - seed: int -> seed of the perlin noise. Two perlin noise with the same seed are identical.
            - !*wrapSize: int -> the noise will wrap after each multiple of this number. !(must be a power of 2) *(defaults to 256)
        """
        
        self._wrapSize: int = wrapSize
        self._seed: int = seed
        self._rand: Random = Random(seed)
        
        self._GeneratePermTable()
        self._GenerateGradients()
        
        # GeneratePermTable() and GenerateGradients() methods use the full wrap size but Sample() does not and is called more often
        # than the previous two, so it's best not to have to recalculate it each time.
        self._wrapSize -= 1

    def _GeneratePermTable(self) -> None:
        """Generates the permutation table of the gradient vectors."""
        
        self._permTable: list[int] = list(range(self._wrapSize))
        Shuffle(self._rand, self._permTable)
        # double the list to always be in bounds when indexing whithout having to use a modulo (or the bitwise equivalent)
        # for all four corners.
        self._permTable.extend(self._permTable)

    def _GenerateGradients(self) -> None:
        """Generates the constant gradient vectors at the corners of each cell."""
        
        self._gradients: list[tuple[float, float]] = []
        for i in range(self._wrapSize):
            g = (self._rand.random() * 2 - 1, self._rand.random() * 2 - 1)
            l = math.sqrt(g[0] * g[0] + g[1] * g[1])
            self._gradients.append((g[0] / l, g[1] / l))
    
    # ────────────────── UTILITIES ──────────────────
    
    def Sample(self, x: float, y: float) -> float:
        """Returns the perlin noise value (ranging from -1 to 1) at a given position."""
        
        xF = math.floor(x)
        yF = math.floor(y)
        
        # corner coordinates
        gX = xF & self._wrapSize
        gY = yF & self._wrapSize

        # distance from the top left corner (aka: the decimal part of the position)
        xDist = x - xF
        yDist = y - yF

        # lerp between the dot products of the four corner→point vectors and the four gradient vectors
        yFade = Fade(yDist)
        return Lerp(
            Lerp(Dot((xDist, yDist), self._gradients[self._permTable[self._permTable[gX] + gY]]),
                 Dot((xDist, yDist - 1), self._gradients[self._permTable[self._permTable[gX] + gY + 1]]),
                 yFade),
            Lerp(Dot((xDist - 1, yDist), self._gradients[self._permTable[self._permTable[gX + 1] + gY]]),
                 Dot((xDist - 1, yDist - 1), self._gradients[self._permTable[self._permTable[gX + 1] + gY + 1]]),
                 yFade),
            Fade(xDist)
        )