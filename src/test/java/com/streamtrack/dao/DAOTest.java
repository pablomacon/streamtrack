package com.streamtrack.dao;

import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.model.Contenido;
import com.streamtrack.model.Genero;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DAOTest {

    private ContenidoDAO contenidoDAO;
    private GeneroDAO generoDAO;
    private PlataformaDAO plataformaDAO;

    @BeforeEach
    void setUp() {
        contenidoDAO = new MySQLContenidoDAO();
        generoDAO = new MySQLGeneroDAO();
        plataformaDAO = new MySQLPlataformaDAO();
    }

    @Test
    @DisplayName("Debe listar géneros y plataformas precargados")
    void testListarGenerosYPlataformas() throws Exception {
        List<Genero> generos = generoDAO.listarTodos();
        assertFalse(generos.isEmpty(), "Debe haber géneros registrados");

        List<Plataforma> plataformas = plataformaDAO.listarTodos();
        assertFalse(plataformas.isEmpty(), "Debe haber plataformas registradas");
    }

    @Test
    @DisplayName("Debe guardar, consultar y eliminar una Película polimórficamente")
    void testCrudPelicula() throws Exception {
        Genero genero = generoDAO.listarTodos().get(0);
        Plataforma plataforma = plataformaDAO.listarTodos().get(0);

        Pelicula pelicula = new Pelicula("Test Inception", "Sueños dentro de sueños", 2010, genero, plataforma, 148);
        Pelicula guardada = contenidoDAO.guardarPelicula(pelicula);

        assertNotNull(guardada.getId(), "El ID debe ser generado");

        Contenido encontrado = contenidoDAO.buscarPorId(guardada.getId());
        assertNotNull(encontrado);
        assertInstanceOf(Pelicula.class, encontrado);
        assertEquals(TipoContenido.PELICULA, encontrado.getTipo());
        assertEquals("148 min", encontrado.getProgresoVisual());

        contenidoDAO.eliminar(guardada.getId());
        assertNull(contenidoDAO.buscarPorId(guardada.getId()));
    }

    @Test
    @DisplayName("Debe guardar y actualizar estado de una Serie")
    void testCrudSerie() throws Exception {
        Genero genero = generoDAO.listarTodos().get(0);
        Plataforma plataforma = plataformaDAO.listarTodos().get(0);

        Serie serie = new Serie("Test Dark", "Viajes en el tiempo", 2017, genero, plataforma, 3, 26);
        Serie guardada = contenidoDAO.guardarSerie(serie);

        assertNotNull(guardada.getId());

        contenidoDAO.actualizarEstado(guardada.getId(), EstadoContenido.VIENDO);
        Contenido actualizada = contenidoDAO.buscarPorId(guardada.getId());
        assertEquals(EstadoContenido.VIENDO, actualizada.getEstado());

        contenidoDAO.eliminar(guardada.getId());
        assertNull(contenidoDAO.buscarPorId(guardada.getId()));
    }
}
