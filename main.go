package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"totalcontrolx/schemas/meet"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/grandcat/zeroconf"
)

//MQTT configuration
const (
	hostname = "localhost"
	port     = 21883
)

var allowedCommands = []string{"press", "release", "long_press", "text"}

func contains(set []string, s string) bool {
	contain := false

	for _, x := range set {
		if x == s {
			contain = true
			break
		}
	}
	return contain
}

func dispatchCommand(button int, command string) {
	err := meet.Dispatch(button, command)
	if err != nil {
		panic(err)
	}
}

func main() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)

	mqttOptions := mqtt.NewClientOptions()
	mqttOptions.AddBroker(fmt.Sprintf("tcp://%v:%v", hostname, port))

	client := mqtt.NewClient(mqttOptions)
	connectionToken := client.Connect()

	if connectionToken.Wait() && connectionToken.Error() != nil {
		log.Fatal("Connection to server failed\n")
		return
	}

	//Successful connection to server, advertise service
	server, err := zeroconf.Register(
		"TotalControlX",
		"_mqtt._tcp,_tcx-v1",
		"local.",
		port,
		nil,
		nil,
	)
	if err != nil {
		panic(err)
	}
	defer server.Shutdown()

	client.Subscribe("totalcontrolx", 0, func(client mqtt.Client, message mqtt.Message) {
		log.Printf("%s\n", message.Payload())

		decoded := string(message.Payload())
		tokens := strings.Split(decoded, " ")

		command := tokens[0]
		if !contains(allowedCommands, command) {
			log.Println("Invalid command.")
			return
		}

		if len(tokens) < 2 {
			log.Println("Command is malformed. Required at least 2 tokens")
			return
		}

		button, err := strconv.Atoi(tokens[1])
		if err != nil {
			log.Println("Invalid button number.")
			return
		}
		go dispatchCommand(button, command)
	})

	<-c
	client.Disconnect(5)
}
