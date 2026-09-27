package com.streamtrack;

import com.formdev.flatlaf.FlatDarkLaf;
import com.streamtrack.controller.MainController;
import com.streamtrack.dao.ContenidoDAO;
import com.streamtrack.dao.GeneroDAO;
import com.streamtrack.dao.PlataformaDAO;
import com.streamtrack.dao.mysql.MySQLContenidoDAO;
import com.streamtrack.dao.mysql.MySQLGeneroDAO;
import com.streamtrack.dao.mysql.MySQLPlataformaDAO;
import com.streamtrack.service.ContenidoService;
import com.streamtrack.service.GeneroService;
import com.streamtrack.service.PlataformaService;
import com.streamtrack.view.MainFrame;

import javax.swing.*;

public class Main {

    public static void main(String[] args) {
        try {
            UIManager.put("Button.arc", 10);
            UIManager.put("Component.arc", 8);
            UIManager.put("ProgressBar.arc", 8);
            UIManager.put("TextComponent.arc", 8);
            FlatDarkLaf.setup();
        } catch (Exception ex) {
            System.err.println("No se pudo inicializar FlatLaf: " + ex.getMessage());
        }

        SwingUtilities.invokeLater(() -> {
            try {
                GeneroDAO generoDAO = new MySQLGeneroDAO();
                PlataformaDAO plataformaDAO = new MySQLPlataformaDAO();
                ContenidoDAO contenidoDAO = new MySQLContenidoDAO();

                GeneroService generoService = new GeneroService(generoDAO);
                PlataformaService plataformaService = new PlataformaService(plataformaDAO);
                ContenidoService contenidoService = new ContenidoService(contenidoDAO);

                MainFrame mainFrame = new MainFrame();

                MainController mainController = new MainController(
                        mainFrame,
                        contenidoService,
                        generoService,
                        plataformaService
                );

                mainController.iniciar();

            } catch (Exception e) {
                JOptionPane.showMessageDialog(null,
                        "Error crítico al iniciar la aplicación:\n" + e.getMessage(),
                        "Error Fatal", JOptionPane.ERROR_MESSAGE);
                e.printStackTrace();
            }
        });
    }
}
