import csv
import logging
# from collections import defaultdict

# Logger einrichten
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Batch-Größe für Updates und Commits
BATCH_SIZE = 10000

try:
    # Schritt 1: Sammle alle x_SUPPL_Sansoft_auto-Werte aus der CSV-Datei
    auto_to_data = {}
    with open("export_base.csv", "r", encoding='utf-8') as update_file:
        csv_reader = csv.DictReader(update_file)
        
        # Prüfen, ob alle erwarteten Spalten vorhanden sind
        required_columns = [
            'auto', 'healthcare_deductible_netto', 'healthcare_deductible_brutto',
            'healthcare_total_deductible_netto', 'healthcare_total_deductible_brutto',
            'healthcare_unit_tariff_netto', 'healthcare_unit_tariff_brutto', 'name'
        ]
        if not all(col in csv_reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in csv_reader.fieldnames]
            raise ValueError(f"Fehlende Spalten in der CSV-Datei: {missing}")
        
        logger.info("Lese CSV-Datei und sammle x_SUPPL_Sansoft_auto-Werte...")
        for line in csv_reader:
            auto_to_data[line['auto']] = {
                'healthcare_deductible_netto': float(line['healthcare_deductible_netto'] or 0.0),
                'healthcare_deductible_brutto': float(line['healthcare_deductible_brutto'] or 0.0),
                'healthcare_total_deductible_netto': float(line['healthcare_total_deductible_netto'] or 0.0),
                'healthcare_total_deductible_brutto': float(line['healthcare_total_deductible_brutto'] or 0.0),
                'healthcare_unit_tariff_netto': float(line['healthcare_unit_tariff_netto'] or 0.0),
                'healthcare_unit_tariff_brutto': float(line['healthcare_unit_tariff_brutto'] or 0.0),
                'name': line['name'],
            }
        logger.info(f"Gesammelt: {len(auto_to_data)} eindeutige x_SUPPL_Sansoft_auto-Werte.")
    
    # Schritt 2: Einmalige Suche nach allen Verkaufszeilen
    logger.info("Suche nach Verkaufszeilen in der Datenbank...")
    orderlines = env['sale.order.line'].search([('x_SUPPL_Sansoft_auto', 'in', list(auto_to_data.keys()))])
    logger.info(f"Gefunden: {len(orderlines)} Verkaufszeilen.")
    
    # Schritt 3: Verkaufszeilen mit CSV-Daten abgleichen und in Batches aktualisieren
    update_count = 0
    for i, orderline in enumerate(orderlines, 1):
        try:
            auto = orderline.x_SUPPL_Sansoft_auto
            if auto not in auto_to_data:
                logger.warning(f"Keine CSV-Daten für x_SUPPL_Sansoft_auto={auto} gefunden.")
                continue
            
            # Update-Daten vorbereiten
            update_data = {
                #'tariff_number_id': 17678
                'healthcare_is_private': 'insurance_manual',
                'healthcare_deductible_netto': auto_to_data[auto]['healthcare_deductible_netto'],
                'healthcare_deductible_brutto': auto_to_data[auto]['healthcare_deductible_brutto'],
                'healthcare_total_deductible_netto': auto_to_data[auto]['healthcare_total_deductible_netto'],
                'healthcare_total_deductible_brutto': auto_to_data[auto]['healthcare_total_deductible_brutto'],
                'healthcare_unit_tariff_netto': auto_to_data[auto]['healthcare_unit_tariff_netto'],
                'healthcare_unit_tariff_brutto': auto_to_data[auto]['healthcare_unit_tariff_brutto'],
                'name': auto_to_data[auto]['name']
            }
            
            # Update durchführen
            orderline.write(update_data)
            update_count += 1
            
            # Regelmäßig committen, um Speicher freizugeben
            if i % BATCH_SIZE == 0:
                env.cr.commit()
                logger.info(f"Batch von {BATCH_SIZE} Zeilen committed (insgesamt {i} verarbeitet).")
        
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung von x_SUPPL_Sansoft_auto={auto}: {str(e)}")
            continue
    
    # Finaler Commit
    env.cr.commit()
    logger.info(f"Verarbeitung abgeschlossen: {update_count} Verkaufszeilen aktualisiert.")

except Exception as e:
    logger.error(f"Fehler beim Verarbeiten der CSV-Datei: {str(e)}")
    env.cr.rollback()
