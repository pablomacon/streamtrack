package com.streamtrack.view.panels;

import com.streamtrack.model.Genero;
import com.streamtrack.model.Plataforma;
import com.streamtrack.model.enums.TipoContenido;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.time.LocalDate;
import java.util.List;

public class FormularioPanel extends JPanel {

    private final JRadioButton radioPelicula;
    private final JRadioButton radioSerie;
    private final JTextField txtTitulo;
    private final JTextArea txtSinopsis;
    private final JSpinner spinAnio;
    private final JComboBox<Genero> comboGenero;
    private final JComboBox<Plataforma> comboPlataforma;

    private final JSpinner spinDuracion;
    private final JSpinner spinTemporadas;
    private final JSpinner spinCapitulos;

    private final JPanel cardsEspecificas;
    private final CardLayout cardLayoutEspecifico;

    private final JButton btnGuardar;
    private final JButton btnCancelar;

    public FormularioPanel() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createEmptyBorder(20, 40, 20, 40));

        JLabel lblTituloVista = new JLabel("Registrar Nuevo Contenido");
        lblTituloVista.setFont(lblTituloVista.getFont().deriveFont(Font.BOLD, 20f));
        lblTituloVista.setBorder(BorderFactory.createEmptyBorder(0, 0, 15, 0));
        add(lblTituloVista, BorderLayout.NORTH);

        JPanel formContent = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        int row = 0;

        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Tipo de Obra:"), gbc);

        JPanel tipoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 0));
        radioPelicula = new JRadioButton("Película", true);
        radioSerie = new JRadioButton("Serie");
        ButtonGroup bgTipo = new ButtonGroup();
        bgTipo.add(radioPelicula);
        bgTipo.add(radioSerie);
        tipoPanel.add(radioPelicula);
        tipoPanel.add(radioSerie);

        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(tipoPanel, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Título:"), gbc);
        txtTitulo = new JTextField();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(txtTitulo, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Año de Estreno:"), gbc);
        int anioActual = LocalDate.now().getYear();
        spinAnio = new JSpinner(new SpinnerNumberModel(anioActual, 1895, anioActual + 2, 1));
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(spinAnio, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Género:"), gbc);
        comboGenero = new JComboBox<>();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(comboGenero, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Plataforma:"), gbc);
        comboPlataforma = new JComboBox<>();
        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(comboPlataforma, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        formContent.add(new JLabel("Detalles específicos:"), gbc);

        cardLayoutEspecifico = new CardLayout();
        cardsEspecificas = new JPanel(cardLayoutEspecifico);

        JPanel panelPelicula = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        panelPelicula.add(new JLabel("Duración (minutos):"));
        spinDuracion = new JSpinner(new SpinnerNumberModel(120, 1, 999, 5));
        panelPelicula.add(spinDuracion);

        JPanel panelSerie = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        panelSerie.add(new JLabel("Temporadas:"));
        spinTemporadas = new JSpinner(new SpinnerNumberModel(1, 1, 99, 1));
        panelSerie.add(spinTemporadas);
        panelSerie.add(Box.createHorizontalStrut(15));
        panelSerie.add(new JLabel("Capítulos Totales:"));
        spinCapitulos = new JSpinner(new SpinnerNumberModel(10, 1, 9999, 1));
        panelSerie.add(spinCapitulos);

        cardsEspecificas.add(panelPelicula, TipoContenido.PELICULA.name());
        cardsEspecificas.add(panelSerie, TipoContenido.SERIE.name());

        gbc.gridx = 1; gbc.weightx = 1.0;
        formContent.add(cardsEspecificas, gbc);

        row++;
        gbc.gridx = 0; gbc.gridy = row; gbc.weightx = 0.0;
        gbc.anchor = GridBagConstraints.NORTHWEST;
        formContent.add(new JLabel("Sinopsis:"), gbc);

        txtSinopsis = new JTextArea(4, 20);
        txtSinopsis.setLineWrap(true);
        txtSinopsis.setWrapStyleWord(true);
        JScrollPane scrollSinopsis = new JScrollPane(txtSinopsis);
        gbc.gridx = 1; gbc.weightx = 1.0;
        gbc.fill = GridBagConstraints.BOTH;
        formContent.add(scrollSinopsis, gbc);

        add(formContent, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 15, 10));
        btnCancelar = new JButton("Cancelar");
        btnGuardar = new JButton("Guardar en Mi Catálogo");
        btnGuardar.putClientProperty("JButton.buttonType", "roundRect");

        buttonPanel.add(btnCancelar);
        buttonPanel.add(btnGuardar);
        add(buttonPanel, BorderLayout.SOUTH);

        radioPelicula.addActionListener(e -> cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.PELICULA.name()));
        radioSerie.addActionListener(e -> cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.SERIE.name()));
    }

    public void cargarGeneros(List<Genero> generos) {
        comboGenero.removeAllItems();
        if (generos != null) {
            for (Genero g : generos) {
                comboGenero.addItem(g);
            }
        }
    }

    public void cargarPlataformas(List<Plataforma> plataformas) {
        comboPlataforma.removeAllItems();
        if (plataformas != null) {
            for (Plataforma p : plataformas) {
                comboPlataforma.addItem(p);
            }
        }
    }

    public void limpiarCampos() {
        txtTitulo.setText("");
        txtSinopsis.setText("");
        spinAnio.setValue(LocalDate.now().getYear());
        radioPelicula.setSelected(true);
        cardLayoutEspecifico.show(cardsEspecificas, TipoContenido.PELICULA.name());
        spinDuracion.setValue(120);
        spinTemporadas.setValue(1);
        spinCapitulos.setValue(10);
        if (comboGenero.getItemCount() > 0) comboGenero.setSelectedIndex(0);
        if (comboPlataforma.getItemCount() > 0) comboPlataforma.setSelectedIndex(0);
    }

    public TipoContenido getTipoSeleccionado() {
        return radioPelicula.isSelected() ? TipoContenido.PELICULA : TipoContenido.SERIE;
    }

    public String getTitulo() {
        return txtTitulo.getText();
    }

    public String getSinopsis() {
        return txtSinopsis.getText();
    }

    public int getAnio() {
        return (Integer) spinAnio.getValue();
    }

    public Genero getGeneroSeleccionado() {
        return (Genero) comboGenero.getSelectedItem();
    }

    public Plataforma getPlataformaSeleccionada() {
        return (Plataforma) comboPlataforma.getSelectedItem();
    }

    public int getDuracionMinutos() {
        return (Integer) spinDuracion.getValue();
    }

    public int getTotalTemporadas() {
        return (Integer) spinTemporadas.getValue();
    }

    public int getCapitulosTotales() {
        return (Integer) spinCapitulos.getValue();
    }

    public void addGuardarListener(ActionListener l) {
        btnGuardar.addActionListener(l);
    }

    public void addCancelarListener(ActionListener l) {
        btnCancelar.addActionListener(l);
    }
}
