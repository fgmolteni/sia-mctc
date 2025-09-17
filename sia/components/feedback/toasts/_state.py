"""
Estado y gestión de toasts del sistema SIA.

Este módulo implementa el estado global ToastState que maneja
la lista de toasts activos y proporciona métodos para CRUD.
"""

import reflex as rx
from typing import List
from dataclasses import dataclass, field
import uuid
import time
from ._types import ToastType


@dataclass
class ToastItem:
    """
    Elemento individual de toast.

    Attributes:
        id: Identificador único del toast
        message: Mensaje a mostrar
        toast_type: Tipo de toast (SUCCESS, ERROR, WARNING, INFO)
        auto_dismiss: Si debe cerrarse automáticamente
        dismiss_timeout: Tiempo en ms para auto-dismiss
        timestamp: Timestamp de creación
    """

    id: str
    message: str
    toast_type: ToastType
    auto_dismiss: bool = True
    dismiss_timeout: int = 4000
    timestamp: float = field(default_factory=time.time)


class ToastState(rx.State):
    """
    Estado global para gestión de toasts.

    Maneja la lista de toasts activos, límite máximo,
    auto-dismiss y métodos de conveniencia.
    """

    toasts: List[ToastItem] = []
    max_toasts: int = 5

    def add_toast(
        self,
        message: str,
        toast_type: ToastType = ToastType.INFO,
        auto_dismiss: bool = True,
        dismiss_timeout: int = 4000,
    ) -> str:
        """
        Añade un nuevo toast al contenedor.

        Args:
            message: Mensaje a mostrar
            toast_type: Tipo de toast
            auto_dismiss: Si debe cerrarse automáticamente
            dismiss_timeout: Tiempo en ms para auto-dismiss

        Returns:
            str: ID del toast creado
        """

        toast_id = str(uuid.uuid4())
        new_toast = ToastItem(
            id=toast_id,
            message=message,
            toast_type=toast_type,
            auto_dismiss=auto_dismiss,
            dismiss_timeout=dismiss_timeout,
        )

        # Mantener máximo de toasts (FIFO)
        if len(self.toasts) >= self.max_toasts:
            self.toasts = self.toasts[1:]

        self.toasts = [*self.toasts, new_toast]

        # Auto-dismiss si está habilitado - se maneja del lado del cliente
        # No necesitamos manejar timers aquí, el componente toast lo manejará

        return toast_id

    def dismiss_toast(self, toast_id: str):
        """
        Elimina un toast específico.

        Args:
            toast_id: ID del toast a eliminar
        """
        self.toasts = [t for t in self.toasts if t.id != toast_id]

    def dismiss_all_toasts(self):
        """Elimina todos los toasts activos."""
        self.toasts = []

    # Métodos de conveniencia
    def show_success(self, message: str, auto_dismiss: bool = True):
        """
        Muestra un toast de éxito.

        Args:
            message: Mensaje a mostrar
            auto_dismiss: Si debe cerrarse automáticamente
        """
        self.add_toast(message, ToastType.SUCCESS, auto_dismiss)

    def show_error(self, message: str, auto_dismiss: bool = False):
        """
        Muestra un toast de error.

        Args:
            message: Mensaje a mostrar
            auto_dismiss: Si debe cerrarse automáticamente (False por defecto)
        """
        self.add_toast(message, ToastType.ERROR, auto_dismiss)

    def show_warning(self, message: str, auto_dismiss: bool = True):
        """
        Muestra un toast de advertencia.

        Args:
            message: Mensaje a mostrar
            auto_dismiss: Si debe cerrarse automáticamente
        """
        self.add_toast(message, ToastType.WARNING, auto_dismiss)

    def show_info(self, message: str, auto_dismiss: bool = True):
        """
        Muestra un toast informativo.

        Args:
            message: Mensaje a mostrar
            auto_dismiss: Si debe cerrarse automáticamente
        """
        self.add_toast(message, ToastType.INFO, auto_dismiss)
