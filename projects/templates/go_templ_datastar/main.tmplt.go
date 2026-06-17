package main

import (
	product_handlers "ds-live-update/products/handlers"
	"fmt"
	"net/http"
	//"ds-live-update/model"
)


func main() {
	port := "8080"

	mux := http.NewServeMux() // Creamos un nuevo Mux

	//productoSimple := model.GetProductoEjemplo(false)

	fs := http.FileServer(http.Dir("./static"))
	mux.Handle("/static/", http.StripPrefix("/static", fs)) // Y dejamos que una función se encarge de los requests a la ruta raíz

	mux.HandleFunc("/admin", product_handlers.HandleAdmin) // Y dejamos que una función se encarge de los requests a la ruta raíz
	mux.HandleFunc("/admin/products/design/add/{quantity}", product_handlers.AddProductElementToTree)

	fmt.Println("Servidor escuchando en el puerto", port)
	// Iinicia el servidor. Si solo se coloca :puerto, se asume localhost.
	http.ListenAndServe(":"+port, mux)
}

// func handleRoot(w http.ResponseWriter, r *http.Request) {
// 	fmt.Fprintf(w, "Hello World!")
// }
