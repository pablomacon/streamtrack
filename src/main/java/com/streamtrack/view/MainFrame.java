package com.streamtrack.view;

import com.streamtrack.view.panels.CatalogoPanel;
import com.streamtrack.view.panels.FormularioPanel;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;

public class MainFrame extends JFrame {

    public static final String VISTA_CATALOGO = "CATALOGO";
    public static final String VISTA_FORMULARIO = "FORMULARIO";

    private final CardLayout cardLayout;
    private final JPanel panelContenedor;

    private final CatalogoPanel catalogoPanel;
    private final FormularioPanel formularioPanel;

    private final JButton btnNavCatalogo;
    private final JButton btnNavNuevo;

    public MainFrame() {
        setTitle("StreamTrack - Gestor Personal de Streaming");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 650);
        setMinimumSize(new Dimension(850, 500));
        setLocationRelativeTo(null);

        JPanel navbar = new JPanel(new BorderLayout(15, 0));
        navbar.setBorder(BorderFactory.createEmptyBorder(12, 25, 12, 25));

        JLabel lblLogo = new JLabel("STREAMTRACK");
        lblLogo.setFont(lblLogo.getFont().deriveFont(Font.BOLD, 18f));
        lblLogo.setForeground(new Color(229, 9, 20));

        JPanel navButtons = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        btnNavCatalogo = new JButton("Catálogo");
        btnNavNuevo = new JButton("+ Agregar Obra");
        btnNavNuevo.putClientProperty("JButton.buttonType", "roundRect");

        navButtons.add(btnNavCatalogo);
        navButtons.add(btnNavNuevo);

        navbar.add(lblLogo, BorderLayout.WEST);
        navbar.add(navButtons, BorderLayout.EAST);
        add(navbar, BorderLayout.NORTH);

        cardLayout = new CardLayout();
        panelContenedor = new JPanel(cardLayout);

        catalogoPanel = new CatalogoPanel();
        formularioPanel = new FormularioPanel();

        panelContenedor.add(catalogoPanel, VISTA_CATALOGO);
        panelContenedor.add(formularioPanel, VISTA_FORMULARIO);

        add(panelContenedor, BorderLayout.CENTER);
    }

    public void mostrarVista(String nombreVista) {
        cardLayout.show(panelContenedor, nombreVista);
    }

    public CatalogoPanel getCatalogoPanel() {
        return catalogoPanel;
    }

    public FormularioPanel getFormularioPanel() {
        return formularioPanel;
    }

    public void addNavCatalogoListener(ActionListener l) {
        btnNavCatalogo.addActionListener(l);
    }

    public void addNavNuevoListener(ActionListener l) {
        btnNavNuevo.addActionListener(l);
    }
}
