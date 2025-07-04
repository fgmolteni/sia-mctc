# Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema Interno de Administración (SIA)! Toda ayuda es bienvenida. Esta guía te proporcionará todo lo que necesitas para empezar.

## Cómo Contribuir

### Reporte de Errores (Bugs)

Si encuentras un error, por favor, asegúrate de que no haya sido reportado previamente en la sección de "Issues" del repositorio.

Al crear un nuevo issue, por favor, incluye:

1.  **Un título claro y descriptivo.**
2.  **Pasos para reproducir el error:** Describe de la forma más detallada posible cómo podemos encontrar el mismo error.
3.  **Comportamiento esperado:** ¿Qué debería haber pasado?
4.  **Comportamiento actual:** ¿Qué pasó en realidad?
5.  **Contexto adicional:** Capturas de pantalla, logs, o cualquier otra información que pueda ser útil.

### Sugerencias de Mejoras

Si tienes una idea para una nueva funcionalidad o una mejora para una existente:

1.  **Abre un issue** con la etiqueta `enhancement`.
2.  **Describe tu idea** de la forma más clara posible, explicando el caso de uso y por qué sería útil para el proyecto.

### Proceso de Desarrollo (Pull Requests)

Si quieres contribuir con código, sigue estos pasos:

1.  **Haz un fork** del repositorio.
2.  **Crea una nueva rama** para tus cambios. Usa un nombre descriptivo (ej. `feature/agregar-calculo-combustible` o `fix/error-en-pdf`).
    ```bash
    git checkout -b nombre-de-tu-rama
    ```
3.  **Realiza tus cambios.** Asegúrate de seguir las convenciones de estilo del proyecto.
4.  **Haz commit de tus cambios.** Escribe un mensaje de commit claro y conciso.
    ```bash
    git commit -m "feat: Agrega cálculo de combustible en el reporte"
    ```
5.  **Envía tus cambios** a tu fork.
    ```bash
    git push origin nombre-de-tu-rama
    ```
6.  **Abre un Pull Request (PR)** desde tu fork a la rama principal del repositorio original.
7.  **En la descripción del PR,** enlaza cualquier issue relacionado y describe los cambios que has realizado.

¡Gracias de nuevo por tu contribución!
