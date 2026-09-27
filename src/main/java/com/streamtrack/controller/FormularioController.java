package com.streamtrack.controller;

import com.streamtrack.model.Genero;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.enums.TipoContenido;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.util.ValidationException;
import com.streamtrack.view.panels.FormularioPanel;

import javax.swing.*;
import java.util.List;

public class FormularioController {

    private final FormularioPanel vista;
    private final ContenidoService contenidoService;
    private final GeneroService generoService;
    private final PlataformaService plataformaService;
    private final MainController mainController;

    public FormularioController(FormularioPanel vista,
                                ContenidoService contenidoService,
                                GeneroService generoService,
                                PlataformaService plataformaService,
                                MainController mainController) {
        this.vista = vista;
        this.contenidoService = contenidoService;
        this.generoService = generoService;
        this.plataformaService = plataformaService;
        this.mainController = mainController;

        inicializarEventos();
    }

    private void inicializarEventos() {
        vista.addGuardarListener(e -> onGuardar());
        vista.addCancelarListener(e -> onCancelar());
    }

    public void prepararFormulario() {
        try {
            List<Genero> generos = generoService.listarTodos();
            List<Plataforma> plataformas = plataformaService.listarTodas();

            vista.cargarGeneros(generos);
            vista.cargarPlataformas(plataformas);
            vista.limpiarCampos();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Error al cargar catálogos de géneros y plataformas: " + ex.getMessage(),
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void onGuardar() {
        TipoContenido tipo = vista.getTipoSeleccionado();
        String titulo = vista.getTitulo();
        String sinopsis = vista.getSinopsis();
        int anio = vista.getAnio();
        Genero genero = vista.getGeneroSeleccionado();
        Plataforma plataforma = vista.getPlataformaSeleccionada();

        try {
            if (tipo == TipoContenido.PELICULA) {
                int duracion = vista.getDuracionMinutos();
                contenidoService.registrarPelicula(titulo, sinopsis, anio, genero, plataforma, duracion);
            } else {
                int temporadas = vista.getTotalTemporadas();
                int capitulos = vista.getCapitulosTotales();
                contenidoService.registrarSerie(titulo, sinopsis, anio, genero, plataforma, temporadas, capitulos);
            }

            JOptionPane.showMessageDialog(vista,
                    "¡Obra registrada exitosamente en tu catálogo!",
                    "Guardado", JOptionPane.INFORMATION_MESSAGE);

            vista.limpiarCampos();
            mainController.mostrarCatalogo();

        } catch (ValidationException ve) {
            JOptionPane.showMessageDialog(vista,
                    ve.getMessage(),
                    "Validación", JOptionPane.WARNING_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(vista,
                    "Ocurrió un error inesperado al registrar la obra: " + ex.getMessage(),
                    "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void onCancelar() {
        vista.limpiarCampos();
        mainController.mostrarCatalogo();
    }
}
