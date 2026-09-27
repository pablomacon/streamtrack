package com.streamtrack.service;

import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.model.Genero;
import com.streamtrack.model.Pelicula;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.Serie;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.util.ValidationException;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ContenidoServiceTest {

    private ContenidoService contenidoService;
    private Genero generoPrueba;
    private Plataforma plataformaPrueba;
    private final List<Integer> idsParaLimpiar = new ArrayList<>();

    @BeforeEach
    void setUp() throws Exception {
        contenidoService = new ContenidoService(new MySQLContenidoDAO());
        generoPrueba = new MySQLGeneroDAO().listarTodos().get(0);
        plataformaPrueba = new MySQLPlataformaDAO().listarTodos().get(0);
    }

    @AfterEach
    void tearDown() {
        for (Integer id : idsParaLimpiar) {
            try {
                contenidoService.eliminarContenido(id);
            } catch (Exception ignored) {
            }
        }
        idsParaLimpiar.clear();
    }

    @Test
    @DisplayName("Debe rechazar el registro de película con título vacío")
    void testValidacionTituloVacio() {
        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.registrarPelicula("   ", "Sinopsis", 2020, generoPrueba, plataformaPrueba, 120));
        assertTrue(ex.getMessage().contains("título"));
    }

    @Test
    @DisplayName("Debe rechazar el registro de película con año inválido")
    void testValidacionAnioInvalido() {
        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.registrarPelicula("Cine Antiguo", "Sinopsis", 1800, generoPrueba, plataformaPrueba, 120));
        assertTrue(ex.getMessage().contains("año"));
    }

    @Test
    @DisplayName("Debe rechazar calificar una obra en estado PENDIENTE")
    void testRechazoCalificarPendiente() throws Exception {
        Pelicula p = contenidoService.registrarPelicula("Interstellar Test", "Espacio", 2014, generoPrueba, plataformaPrueba, 169);
        idsParaLimpiar.add(p.getId());

        assertEquals(EstadoContenido.PENDIENTE, p.getEstado());

        ValidationException ex = assertThrows(ValidationException.class, () ->
                contenidoService.calificarContenido(p.getId(), 9));
        assertTrue(ex.getMessage().contains("Pendiente"));
    }

    @Test
    @DisplayName("Debe cambiar estado automáticamente a VISTO cuando la serie se completa")
    void testTransicionAutomaticaSerie() throws Exception {
        Serie s = contenidoService.registrarSerie("Chernobyl Test", "Drama nuclear", 2019, generoPrueba, plataformaPrueba, 1, 5);
        idsParaLimpiar.add(s.getId());

        contenidoService.registrarProgresoSerie(s.getId(), 5);

        Serie actualizada = (Serie) contenidoService.buscarPorId(s.getId());
        assertEquals(5, actualizada.getCapitulosVistos());
        assertEquals(EstadoContenido.VISTO, actualizada.getEstado());
    }
}
