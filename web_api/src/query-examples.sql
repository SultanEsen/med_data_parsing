
SELECT mnn, trade_mark_name,        
       producer, medicine_info, limit_price FROM russia_data 
       WHERE mnn ILIKE 'Калия хлорид+Натрия ацетат+Натрия хлорид' AND trade_mark_name ILIKE 'ацесоль';


-- kazakhstan sometimes has mnn, sometimes not
-- but some trade_mark_name are broken
-- also dosage_form is expected

SELECT mnn, trade_mark_name, producer FROM kazakhstan_data 
	WHERE mnn ILIKE 'левоцетиризин' AND trade_mark_name ILIKE '%L-ЦЕТ%';

SELECT * FROM kazakhstan_data 
	WHERE mnn ilike '%моксифлоксацин%' AND dosage_form ilike('%таблетки%'); 

-- TODO: remove all 'нет данных' from mnn column for kazakhstan              