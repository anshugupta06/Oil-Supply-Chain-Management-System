-- -----------------------------------
-- Table to hold the calculated logistics status
-- -----------------------------------
CREATE TABLE LogisticsStatus (
    outlet_id BIGINT UNSIGNED PRIMARY KEY,
    outlet_name VARCHAR(100),
    refinery_name VARCHAR(100),
    days_of_stock_remaining DECIMAL(8, 2),
    stock_status ENUM('HEALTHY', 'CRITICAL') NOT NULL,
    FOREIGN KEY (outlet_id) REFERENCES Retail_Outlets(outlet_id)
);

-- -----------------------------------
-- TRIGGER: Update Logistics Status on Stock Change
-- -----------------------------------
DELIMITER //

CREATE TRIGGER after_retail_outlet_update
AFTER UPDATE ON Retail_Outlets
FOR EACH ROW
BEGIN
    DECLARE days_remaining DECIMAL(8, 2);
    DECLARE refinery_name_val VARCHAR(100);

    -- 1️⃣ Calculate Days of Stock Remaining
    IF NEW.daily_sales > 0 THEN
        SET days_remaining = NEW.stock_level / NEW.daily_sales;
    ELSE
        SET days_remaining = 999.0;
    END IF;

    -- 2️⃣ Get Refinery Name
    SELECT refinery_name INTO refinery_name_val
    FROM Refineries
    WHERE refinery_id = NEW.refinery_id;

    -- 3️⃣ Insert or Update the LogisticsStatus table
    INSERT INTO LogisticsStatus (
        outlet_id, 
        outlet_name, 
        refinery_name, 
        days_of_stock_remaining, 
        stock_status
    )
    VALUES (
        NEW.outlet_id,
        NEW.outlet_name,
        refinery_name_val,
        days_remaining,
        CASE 
            WHEN days_remaining <= 3.0 THEN 'CRITICAL'
            ELSE 'HEALTHY'
        END
    )
    ON DUPLICATE KEY UPDATE
        days_of_stock_remaining = days_remaining,
        stock_status = CASE 
            WHEN days_remaining <= 3.0 THEN 'CRITICAL'
            ELSE 'HEALTHY'
        END;
END;
//
DELIMITER ;

/* example

SET SQL_SAFE_UPDATES = 0;
UPDATE Retail_Outlets
SET stock_level = 300
WHERE outlet_name = 'Test Outlet';
 
*/