#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires d'export de données
"""

import os
from datetime import datetime
from tkinter import filedialog, messagebox

def format_date(date):
    """Format a date object to French date format (DD/MM/YYYY)"""
    return date.strftime('%d/%m/%Y')

def export_historique_csv(debut, fin, data):
    """
    Exporter l'historique en CSV
    """
    try:
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"Historique_{debut.strftime('%Y%m%d')}_{fin.strftime('%Y%m%d')}.csv",
            filetypes=[("CSV", "*.csv"), ("Tous les fichiers", "*.*")]
        )
        
        if not filename:
            return None
        
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            writer.writerow(['HISTORIQUE SULTAN AHMED'])
            writer.writerow([f"Période: du {format_date(debut)} au {format_date(fin)}"])
            writer.writerow([])
            
            writer.writerow(['Date', 'Recette', 'Coût Achat', 'Bénéfice Brut', 'Dépenses', 'Bénéfice Net'])
            
            for row in data:
                writer.writerow(row)
        
        return filename
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{e}")
        return None

def exporter_bilan_pdf(bilan_controller, mois_date, quantites_data, depenses_data, totaux):
    """
    Exporter le bilan mensuel en PDF
    
    Args:
        bilan_controller: Instance du BilanController
        mois_date: Date du mois (date object)
        quantites_data: Liste des quantités vendues (du TreeView)
        depenses_data: Liste des dépenses (du TreeView)
        totaux: Dictionnaire avec les totaux financiers
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    except ImportError:
        messagebox.showerror("Erreur", 
            "Le module reportlab n'est pas installé!\n\n"
            "Installez-le avec:\npip install reportlab")
        return False
    
    from utils.formatters import format_currency
    
    # Demander où sauvegarder
    mois_nom = mois_date.strftime('%B_%Y')
    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"Bilan_{mois_nom}_Sultan_Ahmed.pdf",
        filetypes=[("PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
    )
    
    if not filename:
        return False
    
    try:
        # Créer le PDF
        doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(A4),
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=1.5*cm
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        titre_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#D97706'),
            spaceAfter=30,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        sous_titre_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=20,
            alignment=1,
            fontName='Helvetica'
        )
        
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#059669'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        
        story = []
        
        # ==================== EN-TÊTE ====================
        story.append(Paragraph("☕ SULTAN AHMED - SALON DE THÉ", titre_style))
        story.append(Paragraph(
            f"Bilan du mois de {mois_date.strftime('%B %Y')}",
            sous_titre_style
        ))
        story.append(Spacer(1, 0.5*cm))
        
        # ==================== RÉSUMÉ FINANCIER ====================
        story.append(Paragraph("💰 RÉSUMÉ FINANCIER", section_style))
        
        resume_data = [
            ['Indicateur', 'Montant'],
            ['Recette Brute Totale', format_currency(totaux['recette_totale'])],
            ['Coût d\'Achat Total', format_currency(totaux['cout_achat'])],
            ['Bénéfice Brut', format_currency(totaux['benefice_brut'])],
            ['', ''],
            ['Dépenses Journalières', format_currency(totaux['charges_jour'])],
            ['Charges Fixes', format_currency(totaux['charges_fixes'])],
            ['Salaires', format_currency(totaux['salaires'])],
            ['TOTAL DÉPENSES', format_currency(totaux['total_charges'])],
            ['', ''],
            ['BÉNÉFICE NET', format_currency(totaux['benefice_net'])],
        ]
        
        resume_table = Table(resume_data, colWidths=[12*cm, 8*cm])
        resume_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D97706')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -3), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            ('BACKGROUND', (0, -2), (-1, -2), colors.white),
            
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
            
            ('GRID', (0, 0), (-1, -3), 1, colors.grey),
            ('GRID', (0, -1), (-1, -1), 2, colors.HexColor('#047857')),
        ]))
        
        story.append(resume_table)
        story.append(Spacer(1, 1*cm))
        
        # ==================== CHARGES FIXES ====================
        story.append(Paragraph("💼 CHARGES FIXES DU MOIS", 
            ParagraphStyle('SectionCharges',
                          parent=styles['Heading2'],
                          fontSize=16,
                          textColor=colors.HexColor('#DC2626'),
                          spaceAfter=15,
                          fontName='Helvetica-Bold')
        ))
        
        charges_fixes = bilan_controller.get_charges_fixes_mois(mois_date)
        
        if charges_fixes:
            charges_data = [['Type', 'Description', 'Date', 'Montant']]
            
            types_charges = {
                'salaire': 'Salaire',
                'loyer': 'Loyer',
                'electricite': 'Électricité',
                'eau': 'Eau',
                'internet': 'Internet',
                'assurance': 'Assurance',
                'maintenance': 'Maintenance',
                'autre': 'Autre'
            }
            
            total_charges_fixes = 0
            
            for charge in charges_fixes:
                type_fr = types_charges.get(charge['type'], charge['type'].capitalize())
                charges_data.append([
                    type_fr,
                    charge['description'],
                    charge['date'].strftime('%d/%m/%Y'),
                    format_currency(charge['montant'])
                ])
                total_charges_fixes += charge['montant']
            
            charges_data.append(['', '', '', ''])
            charges_data.append([
                'TOTAL CHARGES FIXES',
                '',
                '',
                format_currency(total_charges_fixes)
            ])
            
            charges_table = Table(charges_data, colWidths=[4*cm, 8*cm, 3.5*cm, 4.5*cm])
            charges_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                ('BACKGROUND', (0, 1), (-1, -3), colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -3), [colors.white, colors.HexColor('#FEE2E2')]),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -3), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -3), 10),
                ('TOPPADDING', (0, 1), (-1, -3), 7),
                ('BOTTOMPADDING', (0, 1), (-1, -3), 7),
                
                ('BACKGROUND', (0, -2), (-1, -2), colors.white),
                
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#991B1B')),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('TOPPADDING', (0, -1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
                ('SPAN', (0, -1), (2, -1)),
                
                ('GRID', (0, 0), (-1, -3), 0.5, colors.grey),
                ('GRID', (0, -1), (-1, -1), 2, colors.HexColor('#7F1D1D')),
            ]))
            
            story.append(charges_table)
        else:
            story.append(Paragraph("Aucune charge fixe enregistrée ce mois-ci.", styles['Normal']))
        
        story.append(Spacer(1, 1*cm))
        
        # ==================== QUANTITÉS VENDUES ====================
        story.append(PageBreak())
        story.append(Paragraph("🛒 QUANTITÉS VENDUES DU MOIS", section_style))
        
        if quantites_data:
            quantites_table_data = [['Article', 'Quantité', 'Prix Unitaire', 'Total']]
            quantites_table_data.extend(quantites_data)
            
            quantites_table = Table(quantites_table_data, colWidths=[10*cm, 4*cm, 4*cm, 5*cm])
            quantites_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
                
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            story.append(quantites_table)
        else:
            story.append(Paragraph("Aucune vente ce mois-ci.", styles['Normal']))
        
        story.append(Spacer(1, 1*cm))
        
        # ==================== DÉPENSES JOURNALIÈRES ====================
        story.append(PageBreak())
        story.append(Paragraph("💸 DÉPENSES JOURNALIÈRES", 
            ParagraphStyle('SectionDepenses',
                          parent=styles['Heading2'],
                          fontSize=16,
                          textColor=colors.HexColor('#DC2626'),
                          spaceAfter=15,
                          fontName='Helvetica-Bold')
        ))
        
        if depenses_data:
            depenses_table_data = [['Date', 'Description', 'Montant (DT)']]
            depenses_table_data.extend(depenses_data)
            
            depenses_table = Table(depenses_table_data, colWidths=[4*cm, 12*cm, 4*cm])
            depenses_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FEE2E2')]),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
                
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            
            story.append(depenses_table)
        else:
            story.append(Paragraph("Aucune dépense journalière ce mois-ci.", styles['Normal']))
        
        story.append(Spacer(1, 1*cm))
        
        # ==================== PIED DE PAGE ====================
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(
            f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            ParagraphStyle('Footer',
                          parent=styles['Normal'],
                          fontSize=9,
                          textColor=colors.grey,
                          alignment=1)
        ))
        
        # Générer le PDF
        doc.build(story)
        
        messagebox.showinfo("Succès", f"Bilan exporté avec succès!\n\n{filename}")
        
        # Ouvrir le PDF
        reponse = messagebox.askyesno("Ouvrir?", "Voulez-vous ouvrir le PDF?")
        if reponse:
            import subprocess
            import platform
            
            if platform.system() == 'Windows':
                os.startfile(filename)
            elif platform.system() == 'Darwin':
                subprocess.call(['open', filename])
            else:
                subprocess.call(['xdg-open', filename])
        
        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{e}")
        return False