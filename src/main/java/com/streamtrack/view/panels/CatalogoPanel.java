package com.streamtrack.view.panels;

import com.streamtrack.model.Contenido;
import com.streamtrack.model.enums.EstadoContenido;
import com.streamtrack.model.enums.TipoContenido;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

public class CatalogoPanel extends JPanel {

    private final JTable tablaContenidos;
    private final DefaultTableModel tableModel;
    private final JComboBox<String> comboFiltroTipo;
    private final JComboBox<String> comboFiltroEstado;
    private final JButton btnCambiarEstado;
    private final JButton btnEliminar;
    private final JButton btnNuevo;
    private final JLabel lblContador;

    private final List<Contenido> listaVisible = new ArrayList<>();

    public CatalogoPanel() {
        setLayout(new BorderLayout(15, 15));
        setBorder(BorderFactory.createEmptyBorder(20, 25, 20, 25));

        JPanel topPanel = new JPanel(new BorderLayout(10, 10));

        JPanel leftToolbar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        JLabel lblFiltroTipo = new JLabel("Tipo:");
        comboFiltroTipo = new JComboBox<>(new String[]{"Todos", "Películas", "Series"});

        JLabel lblFiltroEstado = new JLabel("Estado:");
        comboFiltroEstado = new JComboBox<>(new String[]{"Todos", "Pendiente", "Viendo", "Visto", "Abandonado"});

        leftToolbar.add(lblFiltroTipo);
        leftToolbar.add(comboFiltroTipo);
        leftToolbar.add(Box.createHorizontalStrut(10));
        leftToolbar.add(lblFiltroEstado);
        leftToolbar.add(comboFiltroEstado);

        JPanel rightToolbar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        btnCambiarEstado = new JButton("Cambiar Estado");
        btnEliminar = new JButton("Eliminar");
        btnEliminar.setForeground(new Color(230, 80, 80));
        btnNuevo = new JButton("+ Nueva Obra");
        btnNuevo.putClientProperty("JButton.buttonType", "roundRect");

        rightToolbar.add(btnCambiarEstado);
        rightToolbar.add(btnEliminar);
        rightToolbar.add(btnNuevo);

        topPanel.add(leftToolbar, BorderLayout.WEST);
        topPanel.add(rightToolbar, BorderLayout.EAST);
        add(topPanel, BorderLayout.NORTH);

        String[] columnas = {"ID", "Título", "Tipo", "Género", "Plataforma", "Año", "Duración / Progreso", "Estado"};
        tableModel = new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        tablaContenidos = new JTable(tableModel);
        tablaContenidos.setRowHeight(32);
        tablaContenidos.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        tablaContenidos.getTableHeader().setReorderingAllowed(false);
        tablaContenidos.setShowVerticalLines(false);

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(SwingConstants.CENTER);
        tablaContenidos.getColumnModel().getColumn(0).setPreferredWidth(50);
        tablaContenidos.getColumnModel().getColumn(0).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(1).setPreferredWidth(220);
        tablaContenidos.getColumnModel().getColumn(2).setPreferredWidth(80);
        tablaContenidos.getColumnModel().getColumn(2).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(5).setPreferredWidth(60);
        tablaContenidos.getColumnModel().getColumn(5).setCellRenderer(centerRenderer);
        tablaContenidos.getColumnModel().getColumn(7).setPreferredWidth(100);
        tablaContenidos.getColumnModel().getColumn(7).setCellRenderer(centerRenderer);

        JScrollPane scrollPane = new JScrollPane(tablaContenidos);
        add(scrollPane, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        lblContador = new JLabel("Mostrando 0 obras");
        lblContador.setForeground(Color.GRAY);
        bottomPanel.add(lblContador, BorderLayout.WEST);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    public void actualizarContenidos(List<Contenido> contenidos) {
        listaVisible.clear();
        tableModel.setRowCount(0);

        if (contenidos != null) {
            for (Contenido c : contenidos) {
                listaVisible.add(c);
                tableModel.addRow(new Object[]{
                        c.getId(),
                        c.getTitulo(),
                        c.getTipo().getEtiqueta(),
                        c.getGenero().getNombre(),
                        c.getPlataforma().getNombre(),
                        c.getAnioEstreno(),
                        c.getProgresoVisual(),
                        c.getEstado().getEtiqueta()
                });
            }
            lblContador.setText("Total de obras en catálogo: " + contenidos.size());
        } else {
            lblContador.setText("Total de obras en catálogo: 0");
        }
    }

    public Integer getContenidoSeleccionadoId() {
        int selectedRow = tablaContenidos.getSelectedRow();
        if (selectedRow >= 0 && selectedRow < listaVisible.size()) {
            return listaVisible.get(selectedRow).getId();
        }
        return null;
    }

    public Contenido getContenidoSeleccionado() {
        int selectedRow = tablaContenidos.getSelectedRow();
        if (selectedRow >= 0 && selectedRow < listaVisible.size()) {
            return listaVisible.get(selectedRow);
        }
        return null;
    }

    public String getFiltroTipo() {
        return (String) comboFiltroTipo.getSelectedItem();
    }

    public String getFiltroEstado() {
        return (String) comboFiltroEstado.getSelectedItem();
    }

    public void addFiltroTipoListener(ActionListener l) {
        comboFiltroTipo.addActionListener(l);
    }

    public void addFiltroEstadoListener(ActionListener l) {
        comboFiltroEstado.addActionListener(l);
    }

    public void addCambiarEstadoListener(ActionListener l) {
        btnCambiarEstado.addActionListener(l);
    }

    public void addEliminarListener(ActionListener l) {
        btnEliminar.addActionListener(l);
    }

    public void addNuevoContenidoListener(ActionListener l) {
        btnNuevo.addActionListener(l);
    }
}
