#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installeur Sultan Ahmed - VERSION FINALE CORRIGÉE
"""

import os
import sys
import subprocess
from pathlib import Path

# Vérifier que tkinter est disponible
try:
    import tkinter as tk
    from tkinter import messagebox, filedialog
except ImportError:
    print("ERREUR: tkinter n'est pas installé!")
    print("Réinstallez Python avec l'option 'tcl/tk'")
    input("Appuyez sur Entrée...")
    sys.exit(1)


class InstallerComplet:
    def __init__(self):
        self.app_path = Path(__file__).parent.absolute()
        self.launcher_path = self.app_path / "launcher.py"
        self.icon_path = self.app_path / "sultan_ahmed.png"
        self.logo_path = None
        
        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title("Installation - Sultan Ahmed")
        
        width = 550
        height = 520
        
        # Centrer la fenêtre
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg='white')
        
        self.create_ui()
    
    def create_ui(self):
        """Interface graphique"""
        
        # En-tête
        header = tk.Frame(self.root, bg='#D97706', height=90)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, 
                text="☕ Sultan Ahmed", 
                font=('Arial', 24, 'bold'),
                bg='#D97706', 
                fg='white').pack(expand=True)
        
        # Corps
        body = tk.Frame(self.root, bg='white', padx=30, pady=20)
        body.pack(fill='both', expand=True)
        
        # Titre
        tk.Label(body, 
                text="Installation de l'Application",
                font=('Arial', 14, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        # Info
        info_text = "Cette installation va créer:\n\n" \
                   "✅ Raccourci sur le bureau\n" \
                   "✅ Icône personnalisée avec votre logo\n" \
                   "✅ Menu Démarrer\n" \
                   "✅ Démarrage automatique MySQL"
        
        tk.Label(body, 
                text=info_text,
                font=('Arial', 10),
                justify='left',
                bg='white').pack(pady=(0, 15))
        
        # Séparateur
        separator = tk.Frame(body, height=2, bg='#E5E7EB')
        separator.pack(fill='x', pady=15)
        
        # Section Logo
        logo_frame = tk.Frame(body, bg='white')
        logo_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(logo_frame, 
                text="🎨 Logo de l'application:",
                font=('Arial', 11, 'bold'),
                bg='white').pack(anchor='w')
        
        self.logo_label = tk.Label(logo_frame,
                                   text="Aucun logo sélectionné",
                                   font=('Arial', 9, 'italic'),
                                   fg='#6B7280',
                                   bg='white')
        self.logo_label.pack(anchor='w', pady=(5, 10))
        
        tk.Button(logo_frame,
                 text="📂 Choisir le logo",
                 command=self.choisir_logo,
                 font=('Arial', 10),
                 bg='#2563EB',
                 fg='white',
                 padx=15,
                 pady=8,
                 cursor='hand2').pack(anchor='w')
        
        # Status
        self.status = tk.Label(body, 
                              text="Prêt à installer",
                              font=('Arial', 9),
                              fg='#059669',
                              bg='white')
        self.status.pack(pady=(15, 10))
        
        # Boutons
        btn_container = tk.Frame(body, bg='white')
        btn_container.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Bouton INSTALLER
        self.btn_install = tk.Button(btn_container,
                                     text="🚀 INSTALLER",
                                     command=self.installer,
                                     font=('Arial', 12, 'bold'),
                                     bg='#059669',
                                     fg='white',
                                     width=14,
                                     height=2,
                                     cursor='hand2')
        self.btn_install.pack(side='left', padx=(20, 10), expand=True)
        
        # Bouton QUITTER
        tk.Button(btn_container,
                 text="❌ QUITTER",
                 command=self.quitter,
                 font=('Arial', 12, 'bold'),
                 bg='#DC2626',
                 fg='white',
                 width=14,
                 height=2,
                 cursor='hand2').pack(side='right', padx=(10, 20), expand=True)
    
    def quitter(self):
        """Quitter l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'installation?"):
            self.root.destroy()
    
    def choisir_logo(self):
        """Sélectionner le logo"""
        try:
            logo_path = filedialog.askopenfilename(
                title="Sélectionnez votre logo Sultan Ahmed",
                initialdir=self.app_path,
                filetypes=[
                    ("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg;*.jpeg"),
                    ("Tous les fichiers", "*.*")
                ]
            )
            
            if logo_path:
                self.logo_path = Path(logo_path)
                self.logo_label.config(
                    text=f"✅ {self.logo_path.name}",
                    fg='#059669',
                    font=('Arial', 9, 'bold')
                )
                self.status.config(text="Logo sélectionné! Cliquez sur INSTALLER")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sélection:\n{e}")
    
    def creer_icone_depuis_logo(self):
        """Créer l'icône depuis le logo"""
        self.status.config(text="Création de l'icône depuis votre logo...")
        self.root.update()
        
        try:
            from PIL import Image
        except ImportError:
            messagebox.showerror("Erreur", "Pillow n'est pas installé!\nRelancez le BAT.")
            return False
        
        try:
            img = Image.open(self.logo_path)
            
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            size = max(img.size)
            square_img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            
            x = (size - img.size[0]) // 2
            y = (size - img.size[1]) // 2
            square_img.paste(img, (x, y), img)
            
            square_img.save(
                str(self.icon_path),
                format='ICO',
                sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            )
            return True
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur création icône:\n{e}")
            return False
    
    def creer_icone_par_defaut(self):
        """Créer icône par défaut"""
        self.status.config(text="Création de l'icône par défaut...")
        self.root.update()
        
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            messagebox.showerror("Erreur", "Pillow n'est pas installé!")
            return False
        
        try:
            size = 256
            img = Image.new('RGB', (size, size), color='#D97706')
            draw = ImageDraw.Draw(img)
            
            margin = 20
            draw.ellipse([margin, margin, size-margin, size-margin], fill='white')
            
            try:
                font = ImageFont.truetype("seguiemj.ttf", 120)
                text = "☕"
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 80)
                    text = "SA"
                except:
                    font = ImageFont.load_default()
                    text = "SA"
            
            bbox = draw.textbbox((0, 0), text, font=font)
            x = (size - (bbox[2] - bbox[0])) // 2
            y = (size - (bbox[3] - bbox[1])) // 2
            draw.text((x, y), text, fill='#D97706', font=font)
            
            img.save(str(self.icon_path), format='ICO', 
                    sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            return True
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur création icône:\n{e}")
            return False
    
    def installer(self):
        """Installation"""
        try:
            self.btn_install.config(state='disabled', text="⏳ Installation...")
            self.status.config(text="Vérification des modules...")
            self.root.update()
            
            # Vérifier winshell
            try:
                import winshell
                from win32com.client import Dispatch
            except ImportError:
                messagebox.showerror("Erreur", 
                    "Les modules pywin32 ou winshell ne sont pas installés!\n\n" +
                    "Relancez le fichier BAT pour les installer.")
                self.btn_install.config(state='normal', text="🚀 INSTALLER")
                return
            
            # Créer l'icône
            icone_creee = False
            if self.logo_path and self.logo_path.exists():
                icone_creee = self.creer_icone_depuis_logo()
            else:
                reponse = messagebox.askyesno("Logo manquant", 
                    "Aucun logo sélectionné.\n\n" +
                    "Voulez-vous en choisir un maintenant?\n\n" +
                    "(Sinon, icône par défaut ☕)")
                if reponse:
                    self.choisir_logo()
                    if self.logo_path:
                        icone_creee = self.creer_icone_depuis_logo()
                    else:
                        icone_creee = self.creer_icone_par_defaut()
                else:
                    icone_creee = self.creer_icone_par_defaut()
            
            if not icone_creee:
                self.btn_install.config(state='normal', text="🚀 INSTALLER")
                return
            
            # Créer raccourci bureau
            self.status.config(text="Création du raccourci bureau...")
            self.root.update()
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Sultan Ahmed.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            
            pythonw = sys.executable.replace("python.exe", "pythonw.exe")
            if not Path(pythonw).exists():
                pythonw = sys.executable
            
            shortcut.Targetpath = pythonw
            shortcut.Arguments = f'"{self.launcher_path}"'
            shortcut.WorkingDirectory = str(self.app_path)
            shortcut.Description = "Sultan Ahmed - Gestion Salon de Thé"
            shortcut.IconLocation = str(self.icon_path)
            shortcut.save()
            
            # Menu démarrer
            self.status.config(text="Création du menu démarrer...")
            self.root.update()
            
            start_menu = winshell.start_menu()
            sultan_folder = os.path.join(start_menu, "Sultan Ahmed")
            os.makedirs(sultan_folder, exist_ok=True)
            shortcut_start = os.path.join(sultan_folder, "Sultan Ahmed.lnk")
            
            shortcut2 = shell.CreateShortCut(shortcut_start)
            shortcut2.Targetpath = pythonw
            shortcut2.Arguments = f'"{self.launcher_path}"'
            shortcut2.WorkingDirectory = str(self.app_path)
            shortcut2.Description = "Sultan Ahmed - Gestion Salon de Thé"
            shortcut2.IconLocation = str(self.icon_path)
            shortcut2.save()
            
            self.status.config(text="✅ Installation terminée!")
            
            logo_info = f"Avec votre logo: {self.logo_path.name}" if self.logo_path else "Avec icône par défaut ☕"
            
            messagebox.showinfo("Installation réussie!", 
                f"🎉 Installation terminée avec succès!\n\n" +
                f"✅ {logo_info}\n\n" +
                f"Raccourcis créés:\n" +
                f"  📂 Bureau: Sultan Ahmed\n" +
                f"  📂 Menu Démarrer: Sultan Ahmed\n\n" +
                f"🚀 Double-cliquez sur l'icône\n" +
                f"    'Sultan Ahmed' sur votre bureau!")
            
            if messagebox.askyesno("Lancer maintenant?", 
                "Voulez-vous lancer Sultan Ahmed maintenant?"):
                try:
                    subprocess.Popen([pythonw, str(self.launcher_path)], 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                except:
                    subprocess.Popen([pythonw, str(self.launcher_path)])
            
            self.root.destroy()
            
        except Exception as e:
            self.status.config(text="❌ Erreur!", fg='red')
            self.btn_install.config(state='normal', text="🚀 INSTALLER")
            messagebox.showerror("Erreur d'installation", 
                f"Une erreur est survenue:\n\n{e}\n\n" +
                f"Chemin: {self.app_path}")
    
    def run(self):
        """Lancer l'installeur"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()


def main():
    """Point d'entrée"""
    try:
        if sys.platform != "win32":
            print("❌ Cette application fonctionne uniquement sur Windows!")
            input("Appuyez sur Entrée...")
            sys.exit(1)
        
        app = InstallerComplet()
        app.run()
    except Exception as e:
        print(f"ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée...")
        sys.exit(1)


if __name__ == "__main__":
    main()