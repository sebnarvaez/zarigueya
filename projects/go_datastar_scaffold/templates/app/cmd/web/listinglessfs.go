package main

import (
	"net/http"
	"path/filepath"
)

type listinglessFileSystem struct {
    fs http.FileSystem
}

func (nfs listinglessFileSystem) Open(path string) (http.File, error) {
    f, err := nfs.fs.Open(path)
    if err != nil {
        return nil, err
    }

    s, err := f.Stat()
    if err != nil {
        return nil, err
    }
    
    if s.IsDir() {
        // Si existe un index.html en la carpeta, FileServe lo detecta
        // así que no hay que hacer nada más. De lo contrario, retornar nil.
        index := filepath.Join(path, "index.html")
        if _, err := nfs.fs.Open(index); err != nil {
            closeErr := f.Close()
            if closeErr != nil {
                return nil, closeErr
            }

            return nil, err
        }
    }

    return f, nil
}    
