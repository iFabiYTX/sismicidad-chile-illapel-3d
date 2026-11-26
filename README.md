# Herramienta Interactiva de Visualización y Análisis Espaciotemporal 3D de la Sismicidad en Chile

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/iFabiYTX/sismicidad-chile-illapel-3d/blob/main/analisis_sismicidad_illapel.ipynb)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

**Asignatura:** EIN092B Visualización de Datos  
**Profesor:** Jorge Portilla  
**Autores:** Fabian Acuña (`facunaa@usm.cl`), Fernando Gutiérrez (`fgutierrezp@usm.cl`)  
**Institución:** Departamento de Electrónica e Informática, Universidad Técnica Federico Santa María, Concepción, Chile  

---

## Descripción del Proyecto
Este repositorio contiene el código fuente, el cuaderno de experimentación y las figuras asociadas al estudio del **Terremoto de Illapel del 16 de septiembre de 2015 ($M_w = 8,3$)** y su secuencia posterior de réplicas ($M \ge 3,0$).

La propuesta articula tres componentes:
1. **Agrupamiento espacial tridimensional no supervisado (DBSCAN):** Evaluado mediante análisis de sensibilidad sobre $(\varepsilon, MinPts)$, coeficiente de silueta ($S$), validación con el modelo de subducción **Slab2** y contraste empírico frente a **K-Means**.
2. **Análisis temporal de decaimiento de réplicas:** Ajuste no lineal de la secuencia posterior al sismo principal mediante la **ley de Omori-Utsu** $n(t) = K / (t + c)^p$, obteniendo $p = 0,96$ ($R^2 = 0,990$).
3. **Entorno de visualización interactiva (Streamlit + Plotly):** Vistas múltiples coordinadas (mapa geoespacial 2D en OpenStreetMap, distribución tridimensional de hipocentros asociada a la subducción con rotación de $360^\circ$ y serie temporal con filtros dinámicos).

---

## Resultados del Análisis de Sensibilidad y Comparación de Algoritmos

| Algoritmo / Configuración | Grupos | Agrupados (%) | Ruido (%) | Prof. Máx. Cluster 0 (km) | Coef. Silueta ($S$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| DBSCAN ($\varepsilon = 0,35$, $MinPts = 6$) | 2 | 590 (82,1 %) | 129 (17,9 %) | 52,7 | 0,167 |
| DBSCAN ($\varepsilon = 0,35$, $MinPts = 8$) | 3 | 569 (79,1 %) | 150 (20,9 %) | 52,7 | -0,090 |
| **DBSCAN ($\varepsilon = 0,45$, $MinPts = 8$)** | **1** | **620 (86,2 %)** | **99 (13,8 %)** | **55,2** | **0,250** |
| DBSCAN ($\varepsilon = 0,45$, $MinPts = 10$) | 1 | 615 (85,5 %) | 104 (14,5 %) | 55,2 | 0,242 |
| DBSCAN ($\varepsilon = 0,55$, $MinPts = 8$) | 1 | 668 (92,9 %) | 51 (7,1 %) | 58,3 | 0,330 |
| K-Means ($k = 2$) | 2 | 719 (100,0 %) | 0 (0,0 %) | 116,8 | 0,383 |
| K-Means ($k = 3$) | 3 | 719 (100,0 %) | 0 (0,0 %) | 116,8 | 0,411 |

---

## Estructura del Repositorio

* **`analisis_sismicidad_illapel.ipynb`**: Cuaderno Jupyter reproducible (ejecutable directamente con el botón *Open in Colab*) con las 7 etapas del estudio.
* **`app.py`**: Aplicación web interactiva en Streamlit.
* **`illapel_2015_usgs.csv`**:Instantánea versionada del catálogo del USGS ($N = 719$ eventos entre el 15-09-2015 y el 15-10-2015). Se incluye en el repositorio para garantizar reproducibilidad exacta frente a eventuales revisiones retrospectivas del catálogo del USGS; si el archivo no está presente localmente, el código lo descarga automáticamente desde la API.
* **`requirements.txt`**: Dependencias de Python con versiones especificadas.
* **`figura1_comparativa_2d_dbscan.png`**, **`figura2_kdistance_omori.png`**, **`figura3_perfil_subduccion_3d.png`**: Figuras a 300 DPI generadas para el informe en formato IEEE.

---

## Instrucciones de Instalación y Ejecución Local

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## Licencia
Distribuido bajo licencia MIT para fines académicos y de investigación.
