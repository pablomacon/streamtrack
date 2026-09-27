package com.streamtrack.controller;

import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.view.MainFrame;

public class MainController {

    private final MainFrame mainFrame;
    private final CatalogoController catalogoController;
    private final FormularioController formularioController;

    public MainController(MainFrame mainFrame,
                          ContenidoService contenidoService,
                          GeneroService generoService,
                          PlataformaService plataformaService) {
        this.mainFrame = mainFrame;

        this.catalogoController = new CatalogoController(
                mainFrame.getCatalogoPanel(),
                contenidoService,
                this
        );

        this.formularioController = new FormularioController(
                mainFrame.getFormularioPanel(),
                contenidoService,
                generoService,
                plataformaService,
                this
        );

        inicializarNavegacion();
    }

    private void inicializarNavegacion() {
        mainFrame.addNavCatalogoListener(e -> mostrarCatalogo());
        mainFrame.addNavNuevoListener(e -> mostrarFormulario());
    }

    public void iniciar() {
        mostrarCatalogo();
        mainFrame.setVisible(true);
    }

    public void mostrarCatalogo() {
        catalogoController.recargarCatalogo();
        mainFrame.mostrarVista(MainFrame.VISTA_CATALOGO);
    }

    public void mostrarFormulario() {
        formularioController.prepararFormulario();
        mainFrame.mostrarVista(MainFrame.VISTA_FORMULARIO);
    }
}
