package meet

import (
	"log"

	"github.com/go-vgo/robotgo"
)

//Execute action for corresponding button
func Dispatch(button int, action string) error {
	log.Printf("%s for %d\n", action, button)

	switch button {
	case 0:
		robotgo.KeyTap("command", "d")
		//perform a ctrl+d
	case 1:
		robotgo.KeyTap("command", "w")
		//perform a exit
	case 2:
		robotgo.KeyTap("command", "e")
		//perform a ctrl+e
	case 3:
		robotgo.KeyTap("audio_play")
	}

	return nil
}
