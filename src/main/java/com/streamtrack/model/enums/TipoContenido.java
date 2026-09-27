package com.streamtrack.model.enums;

public enum TipoContenido {
    PELICULA("Película"),
    SERIE("Serie");

    private final String etiqueta;

    TipoContenido(String etiqueta) {
        this.etiqueta = etiqueta;
    }

    public String getEtiqueta() {
        return etiqueta;
    }

    @Override
    public String toString() {
        return etiqueta;
    }
}
