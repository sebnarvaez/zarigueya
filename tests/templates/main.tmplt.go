package templates

import (
	"net/http"
)

func main() {
	// La dirección raiz se trata con la función handleHome
	% for model in models:
	http.HandleFunc("/${model['name']}", handle${titlec(model['name'])})
	% endfor 
}

% for model in models:
func handle${titlec(model['name'])}(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Hello from the ${model['namep']} handler"))
}

% endfor