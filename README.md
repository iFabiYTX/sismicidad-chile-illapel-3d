# Herramienta Interactiva de Visualización y Análisis Espaciotemporal 3D de la Sismicidad en Chile

**Asignatura:** EIN092B Visualización de Datos  
**Profesor:** Jorge Portilla  
**Autores:** Fabian Acuña (`facunaa@usm.cl`), Fernando Gutiérrez (`fgutierrezp@usm.cl`)  
**Institución:** Departamento de Electrónica e Informática, Universidad Técnica Federico Santa María, Concepción, Chile  

---

## Descripción del Proyecto
Este repositorio contiene el código fuente, el cuaderno de experimentación y las figuras asociadas al estudio del **Terremoto de Illapel del 16 de septiembre de 2015 ($M_w = 8,3$)** y su secuencia posterior de réplicas ($M \ge 3,0$).

La propuesta combina la consulta automatizada de datos desde la API pública del USGS, el agrupamiento espacial tridimensional no supervisado mediante **DBSCAN** (parametrizado con la curva *k-distance* y el método del codo) y una plataforma web interactiva desarrollada con **Streamlit** y **Plotly**.

---

## Estructura del Repositorio

* **`analisis_sismicidad_illapel.ipynb`**: Cuaderno Jupyter reproducible que documenta paso a paso la adquisición automática de datos desde la API del USGS, la limpieza del catálogo ($N = 719$ eventos), la normalización mediante puntaje $Z$ (`StandardScaler`), el ajuste de hiperparámetros ($\varepsilon = 0,45$, $MinPts = 8$), la ejecución de DBSCAN 3D y la generación de las 4 figuras en alta resolución (`300 DPI`).
* **`app.py`**: Aplicación web interactiva en Streamlit que integra:
  1. **Mapa Geoespacial 2D** sobre cartografía OpenStreetMap.
  2. **Visor Tridimensional (3D)** de hipocentros con rotación libre en $360^\circ$ del plano de subducción de la Placa de Nazca.
  3. **Evolución Temporal** de magnitudes y decaimiento de réplicas.
  4. **Filtros Dinámicos** por rango de fechas, magnitud y grupo sismológico.
* **`illapel_2015_usgs.csv`**: Catálogo sísmico descargado desde la API del USGS (15 de septiembre al 15 de octubre de 2015). *(Nota: Si este archivo no se encuentra localmente, tanto el notebook como `app.py` lo descargan automáticamente al ejecutarse).*
* **`requirements.txt`**: Lista de dependencias de Python necesarias para ejecutar el proyecto.
* **`figura1_mapa_epicentros_2d.png` a `figura4_clusters_dbscan.png`**: Figuras oficiales exportadas a 300 DPI utilizadas en el informe escrito en formato IEEE.

---

## Instrucciones de Instalación y Ejecución

### 1. Instalar dependencias
En una terminal ubicada en la carpeta del proyecto, ejecutar:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Dashboard Interactivo
Para iniciar la aplicación web en el navegador local (`http://localhost:8501`), ejecutar:
```bash
python -m streamlit run app.py
```

### 3. Ejecutar el Cuaderno Experimental
El archivo `analisis_sismicidad_illapel.ipynb` puede abrirse y ejecutarse directamente en **Google Colab**, **VS Code** o **Jupyter Notebook** sin requerir configuración manual adicional.
