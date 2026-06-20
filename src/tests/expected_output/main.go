package templates

import (
	"net/http"
)

func main() {
	// La dirección raiz se trata con la función handleHome
	http.HandleFunc("/task", handleTask)
	http.HandleFunc("/contact", handleContact)
}

func handleTask(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Hello from the tasks handler"))
}

func handleContact(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Hello from the contacts handler"))
}

