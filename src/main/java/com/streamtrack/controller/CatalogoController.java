package com.streamtrack.controller;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.util.ValidationException;
import com.streamtrack.view.panels.CatalogoPanel;

import javax.swing.*;
import java.util.List;
import java.util.stream.Collectors;

public class CatalogoController {

    private final CatalogoPanel vista;
    private final ContenidoService contenidoService;
    private final MainController mainController;

    private List<Contenido> cacheCatalogoCompleto;

    public CatalogoController(CatalogoPanel vista, ContenidoService contenidoService, MainController mainController) {
        this.vista = vista;
        this.contenidoService = contenidoService;
        this.mainController = mainController;

        inicializarEventos();
    }

    private void inicializarEventos() {
        vista.addFiltroTipoListener(e -> aplicarFiltros());
        vista.addFiltroEstadoListener(e -> aplicarFiltros());

        vista.addCambiarEstadoListener(e -> onCambiarEstado());
        vista.addEliminarListener(e -> onEliminar());
        vista.addNuevoContenidoListener(e -> mainController.mostrarFormulario());
    }

    public void recargarCatalogo() {
        try {
            cacheCatalogoCompleto = contenidoService.listarCatalogo();
            aplicarFiltros();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Error al cargar el catálogo desde la base de datos: " + ex.getMessage(),
                    "Error de Datos", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void aplicarFiltros() {
        if (cacheCatalogoCompleto == null) {
            return;
        }

        String filtroTipo = vista.getFiltroTipo();
        String filtroEstado = vista.getFiltroEstado();

        List<Contenido> filtrados = cacheCatalogoCompleto.stream()
                .filter(c -> {
                    if ("Películas".equalsIgnoreCase(filtroTipo)) {
                        return c.getTipo() == TipoContenido.PELICULA;
                    } else if ("Series".equalsIgnoreCase(filtroTipo)) {
                        return c.getTipo() == TipoContenido.SERIE;
                    }
                    return true;
                })
                .filter(c -> {
                    if (!"Todos".equalsIgnoreCase(filtroEstado)) {
                        return c.getEstado().getEtiqueta().equalsIgnoreCase(filtroEstado);
                    }
                    return true;
                })
                .collect(Collectors.toList());

        vista.actualizarContenidos(filtrados);
    }

    private void onCambiarEstado() {
        Integer idSeleccionado = vista.getContenidoSeleccionadoId();
        if (idSeleccionado == null) {
            JOptionPane.showMessageDialog(vista,
                    "Por favor, selecciona una obra de la lista para cambiar su estado.",
                    "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        EstadoContenido[] opciones = EstadoContenido.values();
        EstadoContenido nuevoEstado = (EstadoContenido) JOptionPane.showInputDialog(
                vista,
                "Selecciona el nuevo estado:",
                "Actualizar Estado",
                JOptionPane.QUESTION_MESSAGE,
                null,
                opciones,
                vista.getContenidoSeleccionado().getEstado()
        );

        if (nuevoEstado != null) {
            try {
                contenidoService.cambiarEstado(idSeleccionado, nuevoEstado);
                recargarCatalogo();
                JOptionPane.showMessageDialog(vista,
                        "Estado actualizado a: " + nuevoEstado.getEtiqueta(),
                        "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } catch (ValidationException ve) {
                JOptionPane.showMessageDialog(vista, ve.getMessage(), "Regla de Negocio", JOptionPane.WARNING_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(vista, "Error al actualizar estado: " + ex.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void onEliminar() {
        Integer idSeleccionado = vista.getContenidoSeleccionadoId();
        if (idSeleccionado == null) {
            JOptionPane.showMessageDialog(vista,
                    "Por favor, selecciona una obra de la lista para eliminarla.",
                    "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Contenido seleccionado = vista.getContenidoSeleccionado();
        int confirm = JOptionPane.showConfirmDialog(
                vista,
                "¿Estás seguro de que deseas eliminar '" + seleccionado.getTitulo() + "' de tu catálogo?",
                "Confirmar Eliminación",
                JOptionPane.YES_NO_OPTION,
                JOptionPane.WARNING_MESSAGE
        );

        if (confirm == JOptionPane.YES_OPTION) {
            try {
                contenidoService.eliminarContenido(idSeleccionado);
                recargarCatalogo();
                JOptionPane.showMessageDialog(vista,
                        "Obra eliminada correctamente.",
                        "Éxito", JOptionPane.INFORMATION_MESSAGE);
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(vista,
                        "Error al eliminar la obra: " + ex.getMessage(),
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
}
