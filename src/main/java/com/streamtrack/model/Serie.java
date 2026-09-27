package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;

public class Serie extends Contenido {

    private int totalTemporadas;
    private int capitulosTotales;
    private int capitulosVistos;

    public Serie() {
        super();
        this.totalTemporadas = 1;
        this.capitulosVistos = 0;
    }

    public Serie(Integer id, String titulo, String sinopsis, int anioEstreno,
                 Genero genero, Plataforma plataforma, EstadoContenido estado,
                 int puntuacion, LocalDate fechaRegistro,
                 int totalTemporadas, int capitulosTotales, int capitulosVistos) {
        super(id, titulo, sinopsis, anioEstreno, genero, plataforma, estado, puntuacion, fechaRegistro);
        this.totalTemporadas = totalTemporadas;
        this.capitulosTotales = capitulosTotales;
        this.capitulosVistos = capitulosVistos;
    }

    public Serie(String titulo, String sinopsis, int anioEstreno,
                 Genero genero, Plataforma plataforma,
                 int totalTemporadas, int capitulosTotales) {
        super(null, titulo, sinopsis, anioEstreno, genero, plataforma, EstadoContenido.PENDIENTE, 0, LocalDate.now());
        this.totalTemporadas = totalTemporadas;
        this.capitulosTotales = capitulosTotales;
        this.capitulosVistos = 0;
    }

    @Override
    public TipoContenido getTipo() {
        return TipoContenido.SERIE;
    }

    @Override
    public String getProgresoVisual() {
        return "Cap. " + capitulosVistos + "/" + capitulosTotales + " (T" + totalTemporadas + ")";
    }

    public int getTotalTemporadas() {
        return totalTemporadas;
    }

    public void setTotalTemporadas(int totalTemporadas) {
        this.totalTemporadas = totalTemporadas;
    }

    public int getCapitulosTotales() {
        return capitulosTotales;
    }

    public void setCapitulosTotales(int capitulosTotales) {
        this.capitulosTotales = capitulosTotales;
    }

    public int getCapitulosVistos() {
        return capitulosVistos;
    }

    public void setCapitulosVistos(int capitulosVistos) {
        this.capitulosVistos = capitulosVistos;
    }
}
