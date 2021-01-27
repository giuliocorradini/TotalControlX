package meet

import (
	"log"

	"github.com/go-vgo/robotgo"
)

//Execute action for corresponding button
func Dispatch(button int, action string) error {
	log.Printf("%s for %d\n", action, button)

	if action == "press" {
		switch button {
		case 0:
			robotgo.KeyTap("d", "cmd")
			//perform a ctrl+d
		case 1:
			robotgo.KeyTap("w", "cmd")
			//perform a exit
		case 2:
			robotgo.KeyTap("e", "cmd")
			//perform a ctrl+e
		case 3:
			robotgo.KeyTap("audio_play")
		}
	}

	return nil
}
