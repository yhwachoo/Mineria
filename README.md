# Minería de Datos (INFB8104)

Repositorio de tareas y proyecto del ramo **Minería de Datos** — Universidad Tecnológica Metropolitana (UTEM).

## Estructura del repositorio

```
Mineria/
├── proyecto-productividad-textil/   # Proyecto final del ramo
│   ├── proyecto_productividad_textil.ipynb   # Notebook completo (Google Colab)
│   └── Informe_Productividad_Textil.pdf      # Informe técnico-investigativo
│
├── tarea-3-pandas-profiling/        # Tarea 3: análisis exploratorio con Pandas Profiling
│   ├── 3_Pandas_Profiling..ipynb
│   ├── 3_Pandas_Profiling_.ipynb
│   └── 3_Pandas_Profiling_Tarea3.ipynb
│
├── tarea-4-clustering/             # Tarea 4: clustering en Python
│   ├── 4_Python_Clustering (1).ipynb
│   └── 4_Python_Clustering (2).ipynb
│
├── tarea-8-svm/                    # Tarea 8: máquinas de soporte vectorial (SVM)
│   ├── 8_SVM.ipynb
│   └── Tarea_8_SVM.ipynb
│
└── material-estudio/              # Material de apoyo
    └── generar_prueba.py            # Generador de prueba de práctica + solucionario
```

## Proyecto: Predicción del cumplimiento de productividad en una fábrica textil

Modelo de **clasificación binaria** que predice si un equipo de una fábrica textil
**alcanzará o no su productividad objetivo** en una jornada, usando variables operativas y el
**comportamiento temporal reciente** de cada equipo (retardos, media móvil, tendencia y antigüedad
desde el último cambio de estilo).

- **Meta:** accuracy ≥ 80 %. **Resultado:** Random Forest = **87,0 %** (Conjunto B, sin el predictor "atajo").
- **Metodología:** CRISP-DM. **Modelos:** Árbol de Decisión, Random Forest, AdaBoost, Naive Bayes, SVM.
- **Dataset:** *Productivity Prediction of Garment Employees* (UCI ML Repository, id 597).

### Cómo ejecutar el notebook del proyecto

1. Abrir `proyecto-productividad-textil/proyecto_productividad_textil.ipynb` en
   [Google Colab](https://colab.research.google.com/).
2. Ejecutar las celdas en orden. La carga de datos es automática vía `ucimlrepo`
   (con respaldo de subida manual del CSV).

## Referencia del dataset

Imran, A. A. (2020). *Productivity prediction of garment employees* [Conjunto de datos].
UCI Machine Learning Repository. https://doi.org/10.24432/C51S6D
