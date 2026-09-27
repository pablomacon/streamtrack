package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;

public class Pelicula extends Contenido {

    private int duracionMinutos;

    public Pelicula() {
        super();
    }

    public Pelicula(Integer id, String titulo, String sinopsis, int anioEstreno,
                    Genero genero, Plataforma plataforma, EstadoContenido estado,
                    int puntuacion, LocalDate fechaRegistro, int duracionMinutos) {
        super(id, titulo, sinopsis, anioEstreno, genero, plataforma, estado, puntuacion, fechaRegistro);
        this.duracionMinutos = duracionMinutos;
    }

    public Pelicula(String titulo, String sinopsis, int anioEstreno,
                    Genero genero, Plataforma plataforma, int duracionMinutos) {
        super(null, titulo, sinopsis, anioEstreno, genero, plataforma, EstadoContenido.PENDIENTE, 0, LocalDate.now());
        this.duracionMinutos = duracionMinutos;
    }

    @Override
    public TipoContenido getTipo() {
        return TipoContenido.PELICULA;
    }

    @Override
    public String getProgresoVisual() {
        return duracionMinutos + " min";
    }

    public int getDuracionMinutos() {
        return duracionMinutos;
    }

    public void setDuracionMinutos(int duracionMinutos) {
        this.duracionMinutos = duracionMinutos;
    }
}
