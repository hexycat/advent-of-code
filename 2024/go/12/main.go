package main

import (
	"fmt"
	"log"
	"os"
	"slices"
	"sort"
	"strings"
)

type AxisSide int

const (
	UpSide    AxisSide = 1
	DownSide  AxisSide = -1
	LeftSide  AxisSide = -1
	RightSide AxisSide = 1
)

type Axis int

const (
	Horizontal Axis = 0
	Vertical   Axis = 1
)

var Directions = [][2]int{
	{0, 1},  // right
	{1, 0},  // down
	{0, -1}, // left
	{-1, 0}, // up
}

type Region struct {
	crop       string
	area       int
	perimiter  int
	plots      map[Axis]map[int][]int // axis -> plot position -> list of plots along the axis at that position
	fenceSides int
}

func (region *Region) AddPlot(position [2]int) {
	if region.plots == nil {
		region.plots = map[Axis]map[int][]int{
			Horizontal: {},
			Vertical:   {},
		}
	}
	region.plots[Horizontal][position[0]] = append(region.plots[Horizontal][position[0]], position[1])
	region.plots[Vertical][position[1]] = append(region.plots[Vertical][position[1]], position[0])
}

func (region *Region) countFenceSidesAlongAxisSide(plot int, axis Axis, axisSide AxisSide) int {
	count := 0

	fences := []int{}
	neighboringPlots, neighboringPlotsExist := region.plots[axis][plot+int(axisSide)]
	if neighboringPlotsExist {
		for _, plot := range region.plots[axis][plot] {
			if !slices.Contains(neighboringPlots, plot) {
				fences = append(fences, plot)
			}
		}
	} else {
		fences = region.plots[axis][plot]
	}

	if len(fences) > 0 {
		if len(fences) == 1 {
			return 1
		}

		sort.Ints(fences)
		for i := 0; i < len(fences)-1; i++ {
			if fences[i]+1 < fences[i+1] {
				count += 1
			}
		}
		count += 1
	}

	return count
}

func (region *Region) CountFenceSides() {
	horizontalPlots, _ := region.plots[Horizontal]
	for plot := range horizontalPlots {
		region.fenceSides += region.countFenceSidesAlongAxisSide(plot, Horizontal, UpSide)
		region.fenceSides += region.countFenceSidesAlongAxisSide(plot, Horizontal, DownSide)
	}

	verticalPlots, _ := region.plots[Vertical]
	for plot := range verticalPlots {
		region.fenceSides += region.countFenceSidesAlongAxisSide(plot, Vertical, LeftSide)
		region.fenceSides += region.countFenceSidesAlongAxisSide(plot, Vertical, RightSide)
	}
}

func (region *Region) GetFencePrice() int {
	return region.area * region.perimiter
}

func (region *Region) GetDiscountedFencePrice() int {
	return region.area * region.fenceSides
}

func loadInput(filePath string) [][]string {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading the file", filePath)
	}

	gardenMap := [][]string{}
	for row := range strings.SplitSeq(string(input), "\n") {
		if row == "" {
			continue
		}
		gardenMapLine := []string{}
		if len(gardenMap) > 0 {
			gardenMapLine = make([]string, 0, len(gardenMap[0]))
		}
		for char := range strings.SplitSeq(row, "") {
			gardenMapLine = append(gardenMapLine, char)
		}
		gardenMap = append(gardenMap, gardenMapLine)
	}
	return gardenMap
}

func createVisitedMap(gardenMap [][]string) [][]bool {
	visitedMap := make([][]bool, len(gardenMap))
	for i := range visitedMap {
		visitedMap[i] = make([]bool, len(gardenMap[0]))
	}
	return visitedMap
}

func isOutOfBounds(mapSize [2]int, pos [2]int) bool {
	return pos[0] < 0 || pos[0] >= mapSize[0] || pos[1] < 0 || pos[1] >= mapSize[1]
}

func expandRegion(gardenMap *[][]string, visitedMap *[][]bool, region *Region, position [2]int) *Region {
	region.area++
	(*visitedMap)[position[0]][position[1]] = true
	region.AddPlot(position)

	for _, direction := range Directions {
		newPosition := [2]int{position[0] + direction[0], position[1] + direction[1]}
		if isOutOfBounds([2]int{len(*gardenMap), len((*gardenMap)[0])}, newPosition) {
			region.perimiter++
			continue
		}

		if (*gardenMap)[newPosition[0]][newPosition[1]] == region.crop {
			if !(*visitedMap)[newPosition[0]][newPosition[1]] {
				expandRegion(gardenMap, visitedMap, region, newPosition)
			}
		} else {
			region.perimiter++
		}
	}

	return region
}

func findRegions(gardenMap *[][]string, visitedMap *[][]bool) []Region {
	regions := []Region{}
	for i := range *gardenMap {
		for j := range (*gardenMap)[0] {
			if (*visitedMap)[i][j] {
				continue
			}

			region := Region{crop: (*gardenMap)[i][j]}
			expandRegion(gardenMap, visitedMap, &region, [2]int{i, j})
			region.CountFenceSides()

			regions = append(regions, region)
		}
	}
	return regions
}

func calculateTotalFencePrice(regions []Region) int {
	totalPrice := 0
	for _, region := range regions {
		totalPrice += region.GetFencePrice()
	}
	return totalPrice
}

func calculateTotalDiscountedFencePrice(plots []Region) int {
	totalPrice := 0
	for _, region := range plots {
		totalPrice += region.GetDiscountedFencePrice()
	}
	return totalPrice
}

func main() {
	gardenMap := loadInput("input")
	visitedMap := createVisitedMap(gardenMap)

	regions := findRegions(&gardenMap, &visitedMap)
	fmt.Println("Total fence price:", calculateTotalFencePrice(regions))
	fmt.Println("Total fence price with bulk discount applied:", calculateTotalDiscountedFencePrice(regions))

}
