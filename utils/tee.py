# -*- coding: utf-8 -*-
"""
Tee :: Redirección militar de salida estándar
Duplica la salida estándar (stdout) hacia un archivo y la consola simultáneamente.
Usado en EvoAI para trazabilidad crítica de logs simbólicos en tiempo real.
"""

import sys
import os
import threading

class Tee:
    def __init__(self, filepath, mode='a', stream=sys.stdout):
        self.lock = threading.Lock()
        self.filepath = filepath
        self.mode = mode
        self.stream = stream

        # Asegurar directorio del log
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            self.file = open(filepath, mode, buffering=1, encoding='utf-8', errors='replace')
            self._print_internal(f"[🔐 TEE INIT] Redirección activa → {filepath}")
        except Exception as e:
            self.file = None
            self._print_internal(f"[❌ TEE ERROR] No se pudo abrir archivo de log: {e}")

    def write(self, data):
        with self.lock:
            if self.stream:
                try:
                    self.stream.write(data)
                    self.stream.flush()
                except Exception as e:
                    self._print_internal(f"[⚠️ STDOUT ERROR] {e}")
            if self.file:
                try:
                    self.file.write(data)
                    self.file.flush()
                except Exception as e:
                    self._print_internal(f"[⚠️ FILE WRITE ERROR] {e}")

    def flush(self):
        with self.lock:
            if self.stream:
                try:
                    self.stream.flush()
                except:
                    pass
            if self.file:
                try:
                    self.file.flush()
                except:
                    pass

    def close(self):
        with self.lock:
            try:
                if self.file:
                    self.file.close()
                if self.stream:
                    self.stream.flush()
            except:
                pass

    def _print_internal(self, message):
        try:
            sys.__stdout__.write(f"{message}\n")
            sys.__stdout__.flush()
        except:
            pass

    def __del__(self):
        self.close()
