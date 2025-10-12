package main

import (
	"log"
	"os"
	"strings"
)

type Position [2]int

type AntinodeLocationsFunc func(antennaLocations []Position, mapSize [2]int) []Position

func loadInput(filePath string) (antennaLocations map[string][]Position, mapSize [2]int) {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading input file")
	}

	mapWidth := 0
	mapHeight := 0
	antennaLocations = map[string][]Position{}
	for row, rowStr := range strings.Split(string(input), "\n") {
		if rowStr == "" {
			continue
		}

		mapWidth = len(rowStr)
		for col, char := range strings.Split(rowStr, "") {
			if char != "." {
				if _, exists := antennaLocations[char]; !exists {
					antennaLocations[char] = []Position{}
				}
				antennaLocations[char] = append(antennaLocations[char], Position{row, col})
			}
		}
		mapHeight = row + 1
	}

	return antennaLocations, [2]int{mapHeight, mapWidth}
}

func isOutOfBounds(location Position, mapSize [2]int) bool {
	return location[0] < 0 || location[0] >= mapSize[0] || location[1] < 0 || location[1] >= mapSize[1]
}

func locateOneDeltaAntinodes(antennaLocations []Position, mapSize [2]int) []Position {
	locations := []Position{}
	for first := 0; first < len(antennaLocations)-1; first++ {
		for second := first + 1; second < len(antennaLocations); second++ {
			antenna1 := antennaLocations[first]
			antenna2 := antennaLocations[second]

			dy := antenna2[0] - antenna1[0]
			dx := antenna2[1] - antenna1[1]

			location1 := Position{antenna1[0] - dy, antenna1[1] - dx}
			if !isOutOfBounds(location1, mapSize) {
				locations = append(locations, location1)
			}

			location2 := Position{antenna2[0] + dy, antenna2[1] + dx}
			if !isOutOfBounds(location2, mapSize) {
				locations = append(locations, location2)
			}

		}
	}

	return locations
}

func locateInlineAntinodes(antennaLocations []Position, mapSize [2]int) []Position {
	locations := []Position{}
	for first := 0; first < len(antennaLocations)-1; first++ {
		for second := first + 1; second < len(antennaLocations); second++ {
			antenna1 := antennaLocations[first]
			antenna2 := antennaLocations[second]

			locations = append(locations, antenna1, antenna2)

			dy := antenna2[0] - antenna1[0]
			dx := antenna2[1] - antenna1[1]

			step := 1
			for {
				location1 := Position{antenna1[0] - step*dy, antenna1[1] - step*dx}
				if isOutOfBounds(location1, mapSize) {
					break
				}
				locations = append(locations, location1)
				step++
			}

			step = 1
			for {
				location2 := Position{antenna2[0] + step*dy, antenna2[1] + step*dx}
				if isOutOfBounds(location2, mapSize) {
					break
				}
				locations = append(locations, location2)
				step++
			}
		}
	}

	return locations
}

func calculateUniqueAntinodeLocations(
	antinodeLocationsFunc AntinodeLocationsFunc, antennaLocations map[string][]Position, mapSize [2]int,
) int {
	uniqueAntinodeLocations := map[Position]bool{}
	for _, antennas := range antennaLocations {
		for _, location := range antinodeLocationsFunc(antennas, mapSize) {
			uniqueAntinodeLocations[location] = true
		}
	}
	return len(uniqueAntinodeLocations)
}

func main() {
	antennaLocations, mapSize := loadInput("input")

	nOneDeltaAntinodes := calculateUniqueAntinodeLocations(locateOneDeltaAntinodes, antennaLocations, mapSize)
	log.Println("Number of unique one delta antinode locations:", nOneDeltaAntinodes)

	nInlineAntinodes := calculateUniqueAntinodeLocations(locateInlineAntinodes, antennaLocations, mapSize)
	log.Println("Number of unique inline antinode locations:", nInlineAntinodes)
}
