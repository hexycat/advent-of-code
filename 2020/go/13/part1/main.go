package main

import (
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Bus struct {
	Id int
}

func (b *Bus) ArrivalToStation(time int) int {
	at := int(math.Ceil(float64(time)/float64(b.Id))) * b.Id
	return at
}

func (b *Bus) ArrivalToStationDelta(time int) int {
	return b.ArrivalToStation(time) - time
}

type BusSchedule []Bus

type SeaportPassenger struct {
	Time int
}

func (p *SeaportPassenger) findNearestBus(s BusSchedule) (b Bus, wt int) {
	wt = int(math.MaxInt64)
	for _, bus := range s {
		delta := bus.ArrivalToStationDelta(p.Time)
		if delta < wt {
			wt = delta
			b = bus
		}
	}
	return b, wt
}

func main() {
	input := loadInput(getFilePath())
	p := loadSeaportPassenger(input[0])
	s := loadOperatingBuses(input[1])
	b, wt := p.findNearestBus(s)
	log.Println("Nearest bus", b.Id, "arrives at", p.Time+wt, "( delta", wt, ") ")
	log.Println("Answer (BusId * WaitingTime):", b.Id*wt)
}

func getFilePath() string {
	if len(os.Args) < 2 {
		return "input"
	}
	return os.Args[1]
}

func loadInput(file string) []string {
	input, err := os.ReadFile(file)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

func loadSeaportPassenger(time string) SeaportPassenger {
	intT, err := strconv.Atoi(time)
	if err != nil {
		log.Fatalln("Error on converting initial timestamp", time, "to int", err)
	}
	p := SeaportPassenger{Time: intT}
	log.Println("Passenger appearance time at station:", p.Time)
	return p
}

func loadOperatingBuses(schedule string) []Bus {
	operatingBuses := BusSchedule{}
	buses := strings.Split(schedule, ",")
	for _, busStr := range buses {
		if busStr != "x" {
			busId, err := strconv.Atoi(busStr)
			if err != nil {
				log.Println("Unable to load bus", busStr+":", err)
			}
			operatingBuses = append(operatingBuses, Bus{Id: busId})
		}
	}
	log.Println("Operating buses:", operatingBuses)
	return operatingBuses
}
