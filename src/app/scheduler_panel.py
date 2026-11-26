from __future__ import annotations

import tkinter as tk
from datetime import datetime, timedelta

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, X

from src.core.profile_manager import ProfileManager
from src.core.scheduler import Scheduler


class SchedulerPanel(ttk.Frame):
    """Manage local simulated profile schedules without ECU or hardware access."""

    def __init__(self, parent, scheduler: Scheduler, logger) -> None:
        super().__init__(parent, padding=18)
        self.scheduler = scheduler
        self.logger = logger
        self.profile_manager = ProfileManager()
        self._refresh_after_id: str | None = None
        self.profile_var = tk.StringVar()
        self.run_at_var = tk.StringVar(
            value=(datetime.now() + timedelta(minutes=5)).replace(microsecond=0).isoformat()
        )
        self.status_var = tk.StringVar(value="Gestão local de agendamentos simulados.")
        self._build()
        self.refresh()
        self._queue_refresh()

    def _build(self) -> None:
        ttk.Label(
            self,
            text="SCHEDULER / GESTÃO DE AGENDAMENTOS",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 4))
        ttk.Label(
            self,
            text="Os callbacks apenas registam a execução simulada do perfil. Não existe escrita na ECU.",
            wraplength=900,
        ).pack(anchor="w", pady=(0, 16))

        editor = ttk.Frame(self)
        editor.pack(fill=X, pady=(0, 12))
        ttk.Label(editor, text="Perfil").pack(side=LEFT, padx=(0, 6))
        profiles = sorted(
            set(self.profile_manager.list_config_profiles())
            | set(self.profile_manager.list_saved_profiles())
        )
        self.profile_combo = ttk.Combobox(
            editor,
            textvariable=self.profile_var,
            values=profiles,
            state="readonly" if profiles else "disabled",
            width=26,
        )
        self.profile_combo.pack(side=LEFT, padx=(0, 14))
        if profiles:
            self.profile_combo.current(0)

        ttk.Label(editor, text="Data/hora ISO 8601").pack(side=LEFT, padx=(0, 6))
        self.run_at_entry = ttk.Entry(editor, textvariable=self.run_at_var, width=25)
        self.run_at_entry.pack(side=LEFT, padx=(0, 10))
        self.add_button = ttk.Button(
            editor,
            text="CRIAR",
            bootstyle="success",
            command=self._add_schedule,
            state="normal" if profiles else "disabled",
        )
        self.add_button.pack(side=LEFT, padx=4)
        ttk.Button(
            editor,
            text="ATUALIZAR",
            bootstyle="info",
            command=self.refresh,
        ).pack(side=LEFT, padx=4)

        self.tree = ttk.Treeview(
            self,
            columns=("profile", "run_at", "status"),
            show="headings",
            height=12,
        )
        self.tree.heading("profile", text="PERFIL")
        self.tree.heading("run_at", text="DATA / HORA")
        self.tree.heading("status", text="ESTADO")
        self.tree.column("profile", width=230, anchor="w")
        self.tree.column("run_at", width=250, anchor="w")
        self.tree.column("status", width=140, anchor="center")
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_selection_changed)

        actions = ttk.Frame(self)
        actions.pack(fill=X, pady=(10, 0))
        self.cancel_button = ttk.Button(
            actions,
            text="CANCELAR SELECIONADO",
            bootstyle="danger",
            command=self._cancel_selected,
            state="disabled",
        )
        self.cancel_button.pack(side=LEFT)
        ttk.Label(
            actions,
            textvariable=self.status_var,
            wraplength=760,
        ).pack(side=LEFT, padx=12)

    def refresh(self) -> None:
        selected = self.tree.selection() if hasattr(self, "tree") else ()
        selected_id = selected[0] if selected else None
        try:
            schedules = self.scheduler.list_schedules()
            self.tree.delete(*self.tree.get_children())
            for item in schedules:
                state = "CONCLUÍDO" if item["executed"] else "PENDENTE"
                self.tree.insert(
                    "",
                    "end",
                    iid=item["id"],
                    values=(item["profile"], item["run_at"], state),
                )
            if selected_id and self.tree.exists(selected_id):
                self.tree.selection_set(selected_id)
            self.status_var.set(f"{len(schedules)} agendamento(s) carregado(s).")
        except (OSError, ValueError, TypeError) as exc:
            self.status_var.set(f"Não foi possível ler os agendamentos: {exc}")
            self.logger.exception("Falha ao atualizar a interface do Scheduler.")
        self._on_selection_changed()

    def _add_schedule(self) -> None:
        profile = self.profile_var.get()
        try:
            run_at = datetime.fromisoformat(self.run_at_var.get().strip())
            now = datetime.now(run_at.tzinfo) if run_at.tzinfo else datetime.now()
            if run_at <= now:
                raise ValueError("Escolhe uma data/hora futura.")
            self.scheduler.add_schedule(profile, run_at.isoformat())
        except (TypeError, ValueError, OSError) as exc:
            self.status_var.set(f"Agendamento não criado: {exc}")
            return

        self.logger.info("Agendamento simulado criado para o perfil %s em %s.", profile, run_at.isoformat())
        self.status_var.set(f"Agendamento criado para {profile}.")
        self.refresh()

    def _cancel_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            self.status_var.set("Seleciona um agendamento pendente.")
            return
        try:
            cancelled = self.scheduler.cancel_schedule(selected[0])
        except (OSError, ValueError, TypeError) as exc:
            self.status_var.set(f"Não foi possível cancelar: {exc}")
            self.logger.exception("Falha ao cancelar agendamento.")
            return

        self.status_var.set(
            "Agendamento cancelado." if cancelled
            else "O agendamento já foi executado ou deixou de existir."
        )
        self.refresh()

    def _on_selection_changed(self, _event=None) -> None:
        selected = self.tree.selection() if hasattr(self, "tree") else ()
        can_cancel = False
        if selected:
            try:
                can_cancel = any(
                    item["id"] == selected[0] and not item["executed"]
                    for item in self.scheduler.list_schedules()
                )
            except (OSError, ValueError, TypeError):
                can_cancel = False
        if hasattr(self, "cancel_button"):
            self.cancel_button.configure(state="normal" if can_cancel else "disabled")

    def _queue_refresh(self) -> None:
        self._refresh_after_id = self.after(2000, self._refresh_tick)

    def _refresh_tick(self) -> None:
        self._refresh_after_id = None
        if not self.winfo_exists():
            return
        self.refresh()
        self._queue_refresh()

    def destroy(self) -> None:
        if self._refresh_after_id is not None:
            try:
                self.after_cancel(self._refresh_after_id)
            except tk.TclError:
                pass
            self._refresh_after_id = None
        super().destroy()
