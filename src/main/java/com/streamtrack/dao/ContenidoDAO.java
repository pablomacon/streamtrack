package com.streamtrack.dao;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;

import java.sql.SQLException;
import java.util.List;

public interface ContenidoDAO {

    List<Contenido> listarTodos() throws SQLException;

    Contenido buscarPorId(int id) throws SQLException;

    Pelicula guardarPelicula(Pelicula pelicula) throws SQLException;

    Serie guardarSerie(Serie serie) throws SQLException;

    void actualizar(Contenido contenido) throws SQLException;

    void eliminar(int id) throws SQLException;

    void actualizarEstado(int id, EstadoContenido nuevoEstado) throws SQLException;

    boolean existePorTituloYAnio(String titulo, int anio, Integer idExcluir) throws SQLException;
}
