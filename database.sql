CREATE TABLE Wells (
    well_id SERIAL PRIMARY KEY,
    well_name VARCHAR(50),
    location VARCHAR(100),
    capacity_per_day DECIMAL(10,2),
    current_output DECIMAL(10,2),
    pressure_level DECIMAL(10,2),
    temperature DECIMAL(10,2),
    last_inspection_date DATE
);

CREATE TABLE Shipments (
    shipment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    source_well_id BIGINT UNSIGNED,
    destination_refinery_id BIGINT UNSIGNED,
    quantity DECIMAL(10,2),
    transport_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (source_well_id) REFERENCES Wells(well_id),
    FOREIGN KEY (destination_refinery_id) REFERENCES Refineries(refinery_id)
);

CREATE TABLE Refineries (
    refinery_id SERIAL PRIMARY KEY,
    refinery_name VARCHAR(50),
    location VARCHAR(100),
    capacity DECIMAL(10,2),
    processed_today DECIMAL(10,2),
    efficiency DECIMAL(5,2)
);
CREATE TABLE Retail_Outlets (
    outlet_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    outlet_name VARCHAR(50),
    location VARCHAR(100),
    refinery_id BIGINT UNSIGNED,
    daily_sales DECIMAL(10,2),
    stock_level DECIMAL(10,2),
    FOREIGN KEY (refinery_id) REFERENCES Refineries(refinery_id)
);

CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(50),
    location VARCHAR(100),
    status VARCHAR(20),
    last_service_date DATE,
    next_service_due DATE
);

CREATE TABLE Maintenance_Logs (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INT,
    service_date DATE,
    issue_reported VARCHAR(200),
    action_taken VARCHAR(200),
    technician_name VARCHAR(100),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);
