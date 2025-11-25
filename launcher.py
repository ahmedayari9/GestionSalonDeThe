#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sultan Ahmed - Lanceur automatique
Démarre XAMPP MySQL automatiquement puis lance l'application
VERSION SANS CONSOLE
"""

import sys
import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import psutil


class SultanAhmedLauncher:
    """Lanceur intelligent pour Sultan Ahmed"""
    
    def __init__(self):
        self.xampp_path = self.find_xampp()
        self.mysql_running = False
        
    def find_xampp(self):
        """Trouver l'installation de XAMPP"""
        possible_paths = [
            r"C:\xampp",
            r"D:\xampp",
            r"C:\Program Files\xampp",
            r"C:\Program Files (x86)\xampp",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def is_mysql_running(self):
        """Vérifier si MySQL est en cours d'exécution"""
        for proc in psutil.process_iter(['name']):
            try:
                if 'mysqld' in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    def start_mysql(self):
        """Démarrer MySQL via XAMPP"""
        if not self.xampp_path:
            return False, "XAMPP n'est pas installé sur ce PC!\n\nInstallez XAMPP depuis: https://www.apachefriends.org"
        
        # Vérifier si MySQL est déjà en cours
        if self.is_mysql_running():
            return True, "MySQL est déjà en cours d'exécution"
        
        # Démarrer MySQL (SANS CONSOLE)
        mysql_start = os.path.join(self.xampp_path, "mysql_start.bat")
        
        if os.path.exists(mysql_start):
            try:
                # ✅ CRÉER LE PROCESSUS SANS FENÊTRE
                subprocess.Popen([mysql_start], 
                               shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Attendre que MySQL démarre (max 15 secondes)
                for _ in range(15):
                    time.sleep(1)
                    if self.is_mysql_running():
                        return True, "MySQL démarré avec succès!"
                
                return False, "MySQL met trop de temps à démarrer..."
                
            except Exception as e:
                return False, f"Erreur lors du démarrage de MySQL: {e}"
        else:
            # Utiliser xampp-control.exe
            xampp_control = os.path.join(self.xampp_path, "xampp-control.exe")
            if os.path.exists(xampp_control):
                try:
                    # Lancer XAMPP Control Panel (SANS CONSOLE)
                    subprocess.Popen([xampp_control],
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                    return True, "XAMPP Control Panel ouvert.\n\nCliquez sur 'Start' pour MySQL, puis relancez Sultan Ahmed."
                except Exception as e:
                    return False, f"Erreur: {e}"
            
            return False, "Impossible de trouver les fichiers XAMPP"
    
    def launch_app(self):
        """Lancer l'application Sultan Ahmed (SANS CONSOLE)"""
        app_path = Path(__file__).parent / "main.py"
        
        if not app_path.exists():
            messagebox.showerror("Erreur", "Fichier main.py introuvable!")
            return
        
        # ✅ LANCER SANS CONSOLE
        if sys.platform == "win32":
            # Utiliser pythonw.exe (pas de console)
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            subprocess.Popen([pythonw, str(app_path)],
                           creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([sys.executable, str(app_path)])
    
    def run(self):
        """Processus de lancement complet"""
        # Fenêtre de chargement
        splash = tk.Tk()
        splash.title("Sultan Ahmed - Démarrage")
        splash.geometry("420x220")
        splash.resizable(False, False)
        
        # Centrer la fenêtre
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (420 // 2)
        y = (splash.winfo_screenheight() // 2) - (220 // 2)
        splash.geometry(f"420x220+{x}+{y}")
        
        # Contenu
        frame = tk.Frame(splash, bg='#D97706', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        title = tk.Label(frame, text="☕ Sultan Ahmed", 
                        font=('Arial', 22, 'bold'),
                        bg='#D97706', fg='white')
        title.pack(pady=10)
        
        status_label = tk.Label(frame, text="Démarrage en cours...", 
                               font=('Arial', 11),
                               bg='#D97706', fg='white')
        status_label.pack(pady=10)
        
        progress_label = tk.Label(frame, text="🔄 Vérification de MySQL...", 
                                 font=('Arial', 10),
                                 bg='#D97706', fg='white')
        progress_label.pack(pady=10)
        
        splash.update()
        
        # Démarrer MySQL
        success, message = self.start_mysql()
        
        if success:
            progress_label.config(text="✅ MySQL prêt!")
            splash.update()
            time.sleep(1)
            
            progress_label.config(text="🚀 Lancement de l'application...")
            splash.update()
            time.sleep(1)
            
            splash.destroy()
            self.launch_app()
        else:
            splash.destroy()
            messagebox.showerror("Erreur", message)
            
            # Proposer de réessayer
            if messagebox.askyesno("Réessayer?", 
                "Voulez-vous lancer l'application quand même?\n\n" +
                "(MySQL doit être démarré manuellement)"):
                self.launch_app()


def main():
    """Point d'entrée"""
    launcher = SultanAhmedLauncher()
    launcher.run()


if __name__ == "__main__":
    main()