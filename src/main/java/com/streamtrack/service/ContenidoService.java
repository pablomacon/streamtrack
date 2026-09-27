package com.streamtrack.service;

import com.streamtrack.dao.ContenidoDAO;
import com.streamtrack.model.*;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.util.ValidationException;

import java.sql.SQLException;
import java.time.LocalDate;
import java.util.List;

public class ContenidoService {

    private final ContenidoDAO contenidoDAO;

    public ContenidoService(ContenidoDAO contenidoDAO) {
        this.contenidoDAO = contenidoDAO;
    }

    public List<Contenido> listarCatalogo() throws SQLException {
        return contenidoDAO.listarTodos();
    }

    public Contenido buscarPorId(int id) throws SQLException {
        return contenidoDAO.buscarPorId(id);
    }

    public Pelicula registrarPelicula(String titulo, String sinopsis, int anio,
                                     Genero genero, Plataforma plataforma,
                                     int duracionMinutos) throws ValidationException, SQLException {
        validarCamposComunes(titulo, anio, genero, plataforma, null);

        if (duracionMinutos <= 0) {
            throw new ValidationException("La duración de la película debe ser mayor a 0 minutos.");
        }

        Pelicula pelicula = new Pelicula(titulo.trim(), sinopsis != null ? sinopsis.trim() : "",
                anio, genero, plataforma, duracionMinutos);
        return contenidoDAO.guardarPelicula(pelicula);
    }

    public Serie registrarSerie(String titulo, String sinopsis, int anio,
                                Genero genero, Plataforma plataforma,
                                int totalTemporadas, int capitulosTotales) throws ValidationException, SQLException {
        validarCamposComunes(titulo, anio, genero, plataforma, null);

        if (totalTemporadas <= 0) {
            throw new ValidationException("La serie debe tener al menos 1 temporada.");
        }
        if (capitulosTotales <= 0) {
            throw new ValidationException("La serie debe tener al menos 1 capítulo en total.");
        }

        Serie serie = new Serie(titulo.trim(), sinopsis != null ? sinopsis.trim() : "",
                anio, genero, plataforma, totalTemporadas, capitulosTotales);
        return contenidoDAO.guardarSerie(serie);
    }

    public void cambiarEstado(int idContenido, EstadoContenido nuevoEstado) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido que intentas actualizar no existe.");
        }
        if (nuevoEstado == null) {
            throw new ValidationException("Debes seleccionar un estado válido.");
        }

        contenidoDAO.actualizarEstado(idContenido, nuevoEstado);
    }

    public void registrarProgresoSerie(int idSerie, int nuevosCapitulosVistos) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idSerie);
        if (!(contenido instanceof Serie serie)) {
            throw new ValidationException("El contenido no existe o no corresponde a una serie.");
        }

        if (nuevosCapitulosVistos < 0) {
            throw new ValidationException("Los capítulos vistos no pueden ser negativos.");
        }
        if (nuevosCapitulosVistos > serie.getCapitulosTotales()) {
            throw new ValidationException("Los capítulos vistos (" + nuevosCapitulosVistos + 
                    ") no pueden superar el total (" + serie.getCapitulosTotales() + ").");
        }

        serie.setCapitulosVistos(nuevosCapitulosVistos);

        if (nuevosCapitulosVistos == serie.getCapitulosTotales()) {
            serie.setEstado(EstadoContenido.VISTO);
        } else if (nuevosCapitulosVistos > 0 && serie.getEstado() == EstadoContenido.PENDIENTE) {
            serie.setEstado(EstadoContenido.VIENDO);
        }

        contenidoDAO.actualizar(serie);
    }

    public void calificarContenido(int idContenido, int puntuacion) throws ValidationException, SQLException {
        if (puntuacion < 1 || puntuacion > 10) {
            throw new ValidationException("La puntuación debe estar comprendida entre 1 y 10.");
        }

        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido no existe.");
        }

        if (contenido.getEstado() == EstadoContenido.PENDIENTE) {
            throw new ValidationException("No puedes calificar una obra en estado 'Pendiente'. Debes haber comenzado a verla.");
        }

        contenido.setPuntuacion(puntuacion);
        contenidoDAO.actualizar(contenido);
    }

    public void eliminarContenido(int idContenido) throws ValidationException, SQLException {
        Contenido contenido = contenidoDAO.buscarPorId(idContenido);
        if (contenido == null) {
            throw new ValidationException("El contenido seleccionado no existe.");
        }
        contenidoDAO.eliminar(idContenido);
    }

    private void validarCamposComunes(String titulo, int anio, Genero genero, Plataforma plataforma, Integer idExcluir)
            throws ValidationException, SQLException {
        if (titulo == null || titulo.trim().isEmpty()) {
            throw new ValidationException("El título de la obra no puede estar vacío.");
        }

        int anioActual = LocalDate.now().getYear();
        if (anio < 1895 || anio > anioActual + 2) {
            throw new ValidationException("El año de estreno (" + anio + ") debe estar entre 1895 y " + (anioActual + 2) + ".");
        }

        if (genero == null || genero.getId() == null) {
            throw new ValidationException("Debes asignar un género válido a la obra.");
        }

        if (plataforma == null || plataforma.getId() == null) {
            throw new ValidationException("Debes asignar una plataforma válida a la obra.");
        }

        if (contenidoDAO.existePorTituloYAnio(titulo, anio, idExcluir)) {
            throw new ValidationException("Ya existe una obra registrada con el título '" + titulo + "' y año " + anio + ".");
        }
    }
}
