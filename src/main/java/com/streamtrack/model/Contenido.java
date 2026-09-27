package com.streamtrack.model;

import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import java.time.LocalDate;
import java.util.Objects;

public abstract class Contenido {

    private Integer id;
    private String titulo;
    private String sinopsis;
    private int anioEstreno;
    private Genero genero;
    private Plataforma plataforma;
    private EstadoContenido estado;
    private int puntuacion;
    private LocalDate fechaRegistro;

    public Contenido() {
        this.estado = EstadoContenido.PENDIENTE;
        this.puntuacion = 0;
        this.fechaRegistro = LocalDate.now();
    }

    public Contenido(Integer id, String titulo, String sinopsis, int anioEstreno,
                     Genero genero, Plataforma plataforma, EstadoContenido estado,
                     int puntuacion, LocalDate fechaRegistro) {
        this.id = id;
        this.titulo = titulo;
        this.sinopsis = sinopsis;
        this.anioEstreno = anioEstreno;
        this.genero = genero;
        this.plataforma = plataforma;
        this.estado = (estado != null) ? estado : EstadoContenido.PENDIENTE;
        this.puntuacion = puntuacion;
        this.fechaRegistro = (fechaRegistro != null) ? fechaRegistro : LocalDate.now();
    }

    public abstract TipoContenido getTipo();
    public abstract String getProgresoVisual();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getSinopsis() {
        return sinopsis;
    }

    public void setSinopsis(String sinopsis) {
        this.sinopsis = sinopsis;
    }

    public int getAnioEstreno() {
        return anioEstreno;
    }

    public void setAnioEstreno(int anioEstreno) {
        this.anioEstreno = anioEstreno;
    }

    public Genero getGenero() {
        return genero;
    }

    public void setGenero(Genero genero) {
        this.genero = genero;
    }

    public Plataforma getPlataforma() {
        return plataforma;
    }

    public void setPlataforma(Plataforma plataforma) {
        this.plataforma = plataforma;
    }

    public EstadoContenido getEstado() {
        return estado;
    }

    public void setEstado(EstadoContenido estado) {
        this.estado = estado;
    }

    public int getPuntuacion() {
        return puntuacion;
    }

    public void setPuntuacion(int puntuacion) {
        this.puntuacion = puntuacion;
    }

    public LocalDate getFechaRegistro() {
        return fechaRegistro;
    }

    public void setFechaRegistro(LocalDate fechaRegistro) {
        this.fechaRegistro = fechaRegistro;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Contenido contenido = (Contenido) o;
        return Objects.equals(id, contenido.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return getTipo().getEtiqueta() + ": " + titulo + " (" + anioEstreno + ")";
    }
}
