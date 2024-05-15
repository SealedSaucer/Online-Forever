package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/gorilla/websocket"
)

const (
	discordBaseURL = "https://canary.discordapp.com/api/v9"
	gatewayURL     = "wss://gateway.discord.gg/?v=9&encoding=json"
)

type Config struct {
	Token        string
	Status       string
	CustomStatus string
	EmojiName    string
	EmojiID      string
	UseEmoji     bool
}

type DiscordUser struct {
	Username      string
	Discriminator string
	UserID        string
}

func main() {
	cfg := getConfig()
	user := DiscordUser{}

	if err := user.fetchUserInfo(cfg.Token); err != nil {
		log.Fatalf("Failed to fetch user info: %v", err)
	}

	runOnliner(cfg, user)
}

func getConfig() Config {
	reader := bufio.NewReader(os.Stdin)

	cfg := Config{
		Token:        prompt(reader, "Enter your Discord token: "),
		Status:       prompt(reader, "Enter your desired status (online, dnd, idle): "),
		CustomStatus: prompt(reader, "Enter your custom status (or type 'none' for no custom status): "),
	}

	if cfg.Token == "" {
		log.Fatal("Error: A valid token is required.")
	}

	if strings.ToLower(prompt(reader, "Would you like to use an emoji in your custom status? (y/n): ")) == "y" {
		cfg.UseEmoji = true
		cfg.EmojiName = prompt(reader, "Enter the emoji name: ")
		cfg.EmojiID = prompt(reader, "Enter the emoji ID: ")
	}

	return cfg
}

func prompt(reader *bufio.Reader, message string) string {
	fmt.Print(message)
	input, _ := reader.ReadString('\n')
	return strings.TrimSpace(input)
}

func (u *DiscordUser) fetchUserInfo(token string) error {
	req, err := http.NewRequest("GET", discordBaseURL+"/users/@me", nil)
	if err != nil {
		return err
	}
	req.Header.Set("Authorization", token)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("invalid token provided")
	}

	var userInfo struct {
		Username      string `json:"username"`
		Discriminator string `json:"discriminator"`
		ID            string `json:"id"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&userInfo); err != nil {
		return err
	}

	u.Username = userInfo.Username
	u.Discriminator = userInfo.Discriminator
	u.UserID = userInfo.ID

	return nil
}

func onliner(cfg Config) {
	conn, _, err := websocket.DefaultDialer.Dial(gatewayURL, nil)
	if err != nil {
		log.Fatalf("Error connecting to the Discord gateway: %v", err)
	}
	defer conn.Close()

	var hello struct {
		HeartbeatInterval float64 `json:"heartbeat_interval"`
	}
	if err := conn.ReadJSON(&hello); err != nil {
		log.Fatalf("Error reading hello message from gateway: %v", err)
	}

	if hello.HeartbeatInterval <= 0 {
		hello.HeartbeatInterval = 45000
	}

	auth := struct {
		Op int `json:"op"`
		D  struct {
			Token      string `json:"token"`
			Properties struct {
				OS      string `json:"$os"`
				Browser string `json:"$browser"`
				Device  string `json:"$device"`
			} `json:"properties"`
			Presence struct {
				Status string `json:"status"`
				AFK    bool   `json:"afk"`
			} `json:"presence"`
		} `json:"d"`
	}{
		Op: 2,
		D: struct {
			Token      string `json:"token"`
			Properties struct {
				OS      string `json:"$os"`
				Browser string `json:"$browser"`
				Device  string `json:"$device"`
			} `json:"properties"`
			Presence struct {
				Status string `json:"status"`
				AFK    bool   `json:"afk"`
			} `json:"presence"`
		}{
			Token: cfg.Token,
			Properties: struct {
				OS      string `json:"$os"`
				Browser string `json:"$browser"`
				Device  string `json:"$device"`
			}{
				OS:      "Windows 10",
				Browser: "Google Chrome",
				Device:  "Windows",
			},
			Presence: struct {
				Status string `json:"status"`
				AFK    bool   `json:"afk"`
			}{
				Status: cfg.Status,
				AFK:    false,
			},
		},
	}

	if err := conn.WriteJSON(auth); err != nil {
		log.Fatalf("Error sending authentication message to gateway: %v", err)
	}

	cstatus := struct {
		Op int `json:"op"`
		D  struct {
			Since      int `json:"since"`
			Activities []struct {
				Type  int    `json:"type"`
				State string `json:"state"`
				Name  string `json:"name"`
				ID    string `json:"id"`
				Emoji *struct {
					Name     string `json:"name"`
					ID       string `json:"id"`
					Animated bool   `json:"animated"`
				} `json:"emoji,omitempty"`
			} `json:"activities"`
			Status string `json:"status"`
			AFK    bool   `json:"afk"`
		} `json:"d"`
	}{
		Op: 3,
		D: struct {
			Since      int `json:"since"`
			Activities []struct {
				Type  int    `json:"type"`
				State string `json:"state"`
				Name  string `json:"name"`
				ID    string `json:"id"`
				Emoji *struct {
					Name     string `json:"name"`
					ID       string `json:"id"`
					Animated bool   `json:"animated"`
				} `json:"emoji,omitempty"`
			} `json:"activities"`
			Status string `json:"status"`
			AFK    bool   `json:"afk"`
		}{
			Since: 0,
			Activities: []struct {
				Type  int    `json:"type"`
				State string `json:"state"`
				Name  string `json:"name"`
				ID    string `json:"id"`
				Emoji *struct {
					Name     string `json:"name"`
					ID       string `json:"id"`
					Animated bool   `json:"animated"`
				} `json:"emoji,omitempty"`
			}{},
			Status: cfg.Status,
			AFK:    false,
		},
	}

	if cfg.CustomStatus != "none" {
		activity := struct {
			Type  int    `json:"type"`
			State string `json:"state"`
			Name  string `json:"name"`
			ID    string `json:"id"`
			Emoji *struct {
				Name     string `json:"name"`
				ID       string `json:"id"`
				Animated bool   `json:"animated"`
			} `json:"emoji,omitempty"`
		}{
			Type:  4,
			State: cfg.CustomStatus,
			Name:  "Custom Status",
			ID:    "custom",
		}

		if cfg.UseEmoji {
			activity.Emoji = &struct {
				Name     string `json:"name"`
				ID       string `json:"id"`
				Animated bool   `json:"animated"`
			}{
				Name:     cfg.EmojiName,
				ID:       cfg.EmojiID,
				Animated: false,
			}
		}

		cstatus.D.Activities = append(cstatus.D.Activities, activity)
	}

	if err := conn.WriteJSON(cstatus); err != nil {
		log.Fatalf("Error sending custom status to gateway: %v", err)
	}

	heartbeatTicker := time.NewTicker(time.Duration(hello.HeartbeatInterval) * time.Millisecond)
	defer heartbeatTicker.Stop()

	for range heartbeatTicker.C {
		if err := conn.WriteMessage(websocket.TextMessage, []byte(`{"op":1,"d":null}`)); err != nil {
			log.Fatalf("Error sending heartbeat to gateway: %v", err)
		}
	}
}

func runOnliner(cfg Config, user DiscordUser) {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()

	fmt.Printf("Successfully logged in as %s#%s (%s).\n", user.Username, user.Discriminator, user.UserID)
	onliner(cfg)
}
