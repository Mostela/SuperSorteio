package main

import (
	"context"
	"encoding/json"
	"errors"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"log"
	"net/http"
	"os"
)

type Profile struct {
	GuidUser string
	Email    string
	KeyGame  string
}

type ReceiveProfile struct {
	Email string
}

var ctx = context.Background()

func createKey(guidUser string) string {
	rdb := redis.NewClient(&redis.Options{
		Addr:     os.Getenv("REDIS_HOST") + ":6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})
	var keyUser string = uuid.NewString()
	err := rdb.Set(ctx, guidUser, keyUser, 0).Err()
	if err != nil {
		panic(err)
	}

	return keyUser
}

func createUser(w http.ResponseWriter, r *http.Request) {
	guidUser := uuid.New()

	decoder := json.NewDecoder(r.Body)
	var dataUser ReceiveProfile

	err := decoder.Decode(&dataUser)

	if err != nil {
		panic(err)
		return
	}

	profile := Profile{guidUser.String(), dataUser.Email, createKey(guidUser.String())}

	log.Println(profile.GuidUser)

	w.WriteHeader(http.StatusCreated)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(profile)
}

func healthcheck(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func main() {
	http.HandleFunc("/", createUser)
	http.HandleFunc("/health", healthcheck)

	err := http.ListenAndServe(":3333", nil)
	log.Println("Server start in port :3333")

	if errors.Is(err, http.ErrServerClosed) {
		log.Printf("server closed")
	} else if err != nil {
		log.Printf("error starting server: %s\n", err)
		os.Exit(1)
	}
}
