import csv
import logging

# establish logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# establish relevant variables
default_tariff_number = 17678

# batch size for database commits
BATCH_SIZE = 10000

try:
    # step 1: gather relevant information from csv file
    auto_to_data = {}
    with open("export_base.csv", "r", encoding='utf-8') as update_file:
        csv_reader = csv.DictReader(update_file)
        
        # check whether all required columns exist
        required_columns = [
            'auto', 'healthcare_deductible_netto', 'healthcare_deductible_brutto',
            'healthcare_total_deductible_netto', 'healthcare_total_deductible_brutto',
            'healthcare_unit_tariff_netto', 'healthcare_unit_tariff_brutto', 'name'
        ]
        if not all(col in csv_reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in csv_reader.fieldnames]
            raise ValueError(f"Fehlende Spalten in der CSV-Datei: {missing}")

        # read csv file line values as dict into collector dict
        logger.info("Reading csv file and gathering column values...")
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
        logger.info(f"Gathered: {len(auto_to_data)} unique values.")
    
    # step 2: gather records to update from relevant model
    logger.info("Searching databse for recoreds to update...")
    orderlines = env['sale.order.line'].search([('x_SUPPL_Sansoft_auto', 'in', list(auto_to_data.keys()))])
    logger.info(f"Gathered: {len(orderlines)} records.")
    
    # step 3: connect record values and csv values by matching key
    update_count = 0
    for i, orderline in enumerate(orderlines, 1):
        try:
            auto = orderline.x_SUPPL_Sansoft_auto
            if auto not in auto_to_data:
                logger.warning(f"No csv data found for x_SUPPL_Sansoft_auto={auto}.")
                continue
            
            # prepare values to be updated
            update_data = {
                'tariff_number_id': default_tariff_number
                'healthcare_is_private': 'insurance_manual',
                'healthcare_deductible_netto': auto_to_data[auto]['healthcare_deductible_netto'],
                'healthcare_deductible_brutto': auto_to_data[auto]['healthcare_deductible_brutto'],
                'healthcare_total_deductible_netto': auto_to_data[auto]['healthcare_total_deductible_netto'],
                'healthcare_total_deductible_brutto': auto_to_data[auto]['healthcare_total_deductible_brutto'],
                'healthcare_unit_tariff_netto': auto_to_data[auto]['healthcare_unit_tariff_netto'],
                'healthcare_unit_tariff_brutto': auto_to_data[auto]['healthcare_unit_tariff_brutto'],
                'name': auto_to_data[auto]['name']
            }
            
            # execute update
            orderline.write(update_data)
            update_count += 1
            
            # commit regularly to free up memory
            if i % BATCH_SIZE == 0:
                env.cr.commit()
                logger.info(f"Batch of {BATCH_SIZE} records committed (total of {i} processed).")
        
        except Exception as e:
            logger.error(f"Error while processing x_SUPPL_Sansoft_auto={auto}: {str(e)}")
            continue
    
    # final commit of residual updates
    env.cr.commit()
    logger.info(f"Processing complete: {update_count} records updated.")

except Exception as e:
    logger.error(f"Error while processing csv file: {str(e)}")
    env.cr.rollback()
