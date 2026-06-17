package handlers
<%!
from caseconverter import camelcase, pascalcase, snakecase 
%>

import (
	"bytes"
	"${gbl['repo_name']}/${modelname_plural}/views"
	"${gbl['repo_name']}/utils"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/a-h/templ"
	"github.com/starfederation/datastar-go/datastar"
)


var currentState utils.State
var quantity int = 0

func AddProductElementToTree(w http.ResponseWriter, r *http.Request) {
	// Read arguments from URI
	fmt.Println("Manejando ruta AddProductElementToTree")
    sse := datastar.NewSSE(w, r)

	adding, err := strconv.Atoi(r.PathValue("quantity"))

	if err != nil {
		log.Fatal("No se pudo convertir la cantidad de la URL a un número.")
    	sse.ExecuteScript(`window.alert("Pusiste una cantidad invalida!")`)
	}

	quantity += adding

    // Patch elements in the DOM
	rendered := "<div id=\"elements-tree\">\n"
	for i := 0; i < quantity; i++ {
		writer := new(bytes.Buffer)
		fragments.ProductTitleSkRenderer(fmt.Sprintf("title-%d", i)).Render(r.Context(), writer)
		rendered += writer.String() + "\n"
	}
	rendered += "</div>\n"
	fmt.Println(rendered)

	sse.PatchElements(
		rendered,
		datastar.WithSelectorID("elements-tree"))
}

func HandleAdmin(w http.ResponseWriter, r *http.Request) {
	// Update state
	currentState = utils.State{
		ElementsInTree: make([]utils.UiElementBuilder, 0, 4),
		AvailableElements: fragments.ProductBuilders(),
	}
		
	component := views.Index(currentState.ElementsInTree, currentState.AvailableElements)
	templ.Handler(component).ServeHTTP(w, r)
}