package com.streamtrack.model.enums;

public enum EstadoContenido {
    PENDIENTE("Pendiente"),
    VIENDO("Viendo"),
    VISTO("Visto"),
    ABANDONADO("Abandonado");

    private final String etiqueta;

    EstadoContenido(String etiqueta) {
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
